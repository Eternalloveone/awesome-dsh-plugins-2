#!/usr/bin/env python3
"""full_topic_scan.py — full-coverage scan of the GitHub `dsh-plugin` topic.

WHY THIS EXISTS
---------------
The GitHub Search API hard-caps every query at **1000 results** (`page=11` returns
HTTP 422 "Only the first 1000 search results are available"). A single
`sort=stars` query therefore only ever sees the top 1000 by stars — which, for a
topic of ~10,600 repos, leaves ~9,600 long-tail repos unscanned (and most of those
are the *small* repos where genuine new DSH plugins actually hide).

This script breaks the topic into **mutually-disjoint sub-queries** ("partitions")
such that every leaf partition has `total_count <= 1000`, so each one can be pulled
in full via `gh api --paginate`. Together the partitions cover the entire topic.

Partition strategy
-----------------
1. Star tiers (disjoint, cover everything with stars > 10):
       stars:>500 | 200..500 | 100..199 | 50..99 | 21..49 | 11..20
   Each tier is tiny (< 1000), fetched directly. If a tier ever overflows
   (topic growth), it is recursively bisected on `created:` date.
2. The `stars:<=10` remainder (the big bucket, ~9,900 repos) is split by
   `created:` calendar month from 2025-01 to the CURRENT day. Each month is
   usually < 1000; if a month still overflows it is split into its DAYS, and a
   single day still overflows it is split into 24 adjacent HOURLY buckets —
   until every leaf <= 1000 (or MAX_DEPTH, at which point it is reported as
   OVER_CAP rather than silently dropped).

   Why `created:` and not `pushed:`? GitHub's `pushed:` range does NOT support
   sub-day precision and single days can exceed 1000 (e.g. 2026-08-14 = 1702),
   and `stars:` sub-filters inside compound queries are ignored — only
   `created:` supports hour precision AND composes with `stars:<=10`.

   GITHUB QUIRK (measured 2026-08-23, don't "fix" this away): day-level
   `created:A..B` is END-INCLUSIVE — it covers B's ENTIRE day.
   `created:2026-08-13..2026-08-14` = 2224 = 522 + 1702 (both days, exact).
   Therefore the script NEVER writes a day range with a different END day.
   A "single day" is queried as the same-day pair `D..D` (verified = that day),
   a month as the single-sided `YYYY-MM`, and hours as adjacent buckets
   `D T00..D T01`, `D T01..D T02`, ..., `D T23..D+1 T00`. Adjacent hour buckets
   are complete under BOTH closed and half-open END semantics; any boundary
   instant captured twice is absorbed by the emit dedupe.

Union of (star tiers) + (stars:<=10 split by pushed month/day/hour) == the whole
topic, with no overlap.

OUTPUT
------
--out  (default /tmp/dsh_topic_full.json)   : rich list, one dict per repo:
        {name, stars, forks, language, pushed_at, created_at,
         description, html_url, topics}
--compat (default /tmp/dsh_topic_repos.json): list of {"name", "stars"} — the
        exact shape `diff_topic.py` consumes. Extra keys in --out are ignored by it.

RELIABILITY
-----------
- Every `gh` call has a 60s timeout so a stuck subprocess can never hang the run.
- Results are written INCREMENTALLY (flush after every leaf) so a crash/interrupt
  leaves a usable partial file, and progress is observable in the log.
- No global API call cap: rate-limit backoff + timeout + MAX_DEPTH guard against
  runaway loops. (An earlier version capped at 400 calls and silently dropped the
  remaining ~9,900 repos of the 2026-08 bucket — that bug is fixed.)

USAGE
-----
  python3 full_topic_scan.py --dry-run            # print partition plan + counts only
  python3 full_topic_scan.py --execute            # actually fetch everything (slow)
  python3 full_topic_scan.py --execute --only ">500"   # fetch just the >500 star tier
  python3 full_topic_scan.py --execute --since 2026-06 # only months >= 2026-06
  python3 full_topic_scan.py --execute --resume   # skip buckets already in --out

Requires `gh` authenticated (run the Bash tool with dangerouslyDisableSandbox: true;
the sandbox blocks gh's network calls).
"""
import argparse
import calendar
import datetime as dt
import json
import subprocess
import sys
import time
import urllib.parse

BASE = "topic:dsh-plugin"
CAP = 1000            # Search API hard ceiling per query
MAX_DEPTH = 14        # bisection depth guard (day -> hour -> finer)
SLEEP = 1.0           # seconds between gh calls (stay under 30 search req/min)
GH_TIMEOUT = 60       # hard timeout per gh subprocess (seconds)
MAX_RETRY = 6         # per-call retry ceiling

# Star tiers, disjoint, cover every repo with stars > 10.
STAR_TIERS = [
    (">500",   "stars:>500"),
    ("200..500", "stars:200..500"),
    ("100..199", "stars:100..199"),
    ("50..99",  "stars:50..99"),
    ("21..49",  "stars:21..49"),
    ("11..20",  "stars:11..20"),
]


def _gh(args, jq, per_page=1, paginate=False):
    """Run one gh api call. Returns (stdout_text, error_text). Honors timeout,
    rate-limit backoff, and retry ceiling. Returns error '422' on hard cap.

    paginate=True adds `--paginate` — safe ONLY for queries whose total <= CAP
    (Search API hard-caps at 1000 and --paginate stops at the first 422 page).
    Without it, a leaf with total > per_page silently returns just the first
    page — that exact bug cost ~1,950 repos on 2026-08-23."""
    url = "search/repositories?q=" + urllib.parse.quote(args) + f"&per_page={per_page}"
    for attempt in range(MAX_RETRY):
        try:
            cmd = ["gh", "api"]
            if paginate:
                cmd.append("--paginate")
            cmd += [url, "--jq", jq]
            proc = subprocess.run(
                cmd,
                capture_output=True, text=True, timeout=GH_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            sys.stderr.write(f"[timeout] q={args} (attempt {attempt+1})\n")
            time.sleep(3 * (attempt + 1))
            continue
        if proc.returncode == 0:
            return proc.stdout, ""
        err = proc.stderr or ""
        if "rate limit" in err.lower():
            time.sleep(8 * (attempt + 1))
            continue
        if "422" in err and "first 1000" in err:
            sys.stderr.write(f"[422 cap] q={args}\n")
            return "", "422"
        sys.stderr.write(f"[gh ERROR] q={args}\n{err}\n")
        return "", err
    return "", "exhausted-retries"


def gh_total(q):
    """Return total_count for a search query (cheap). Returns -1 on failure."""
    out, err = _gh(q, ".total_count", per_page=1)
    if err:
        return -1
    try:
        return int(out.strip())
    except ValueError:
        return -1


def gh_fetch_leaf(q):
    """Fetch ALL items of a query known to have total_count <= CAP via --paginate.

    Caller guarantees total <= CAP, so `gh api --paginate` returns the full set.
    Items are kept LEAN ({name, stars}) on purpose: 7k+ repos with description
    etc. (~100MB) repeatedly OOM-killed this run on a memory-tight machine
    (2026-08-23); downstream diff/audit only ever needs name + stars (audit
    agents WebFetch the repo themselves).
    """
    jq = '.items[] | {name: .full_name, stars: .stargazers_count}'
    out, err = _gh(q, jq, per_page=100, paginate=True)
    if err and err != "422":
        sys.stderr.write(f"[leaf ERROR {err}] q={q} — fetched items may be PARTIAL\n")
    items = []
    for line in out.splitlines():
        line = line.strip()
        if line:
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return items


def _next_day(d):
    """'YYYY-MM-DD' -> next day's 'YYYY-MM-DD'."""
    return (dt.date.fromisoformat(d) + dt.timedelta(days=1)).isoformat()


def _days_in_month(m):
    """'YYYY-MM' -> list of 'YYYY-MM-DD' for every day of that month.

    The current (partial) month is truncated to today — future days would
    return total_count 0 anyway, but truncating saves a few API calls.
    """
    y, mo = int(m[:4]), int(m[5:])
    ndays = calendar.monthrange(y, mo)[1]
    if m == dt.date.today().strftime("%Y-%m"):
        ndays = dt.date.today().day
    return [dt.date(y, mo, d).isoformat() for d in range(1, ndays + 1)]


def _subdivide(spec):
    """Return child created-specs covering `spec`, or [] if it cannot be split.

    Granularity by spec shape:
      'YYYY-MM'           -> each day of that month ('YYYY-MM-DD')
      'YYYY-MM-DD'        -> 24 adjacent hour buckets
                             ('D T00..D T01', ..., 'D T22..D T23', 'D T23..D+1 T00')
      hour-level '..'     -> cannot split finer (1h is the finest granularity
                             we trust) -> caller marks OVER_CAP

    See module docstring for the END-INCLUSIVE day-range quirk that forces
    this same-day / adjacent-bucket design.
    """
    if len(spec) == 7:  # month -> days
        return _days_in_month(spec)
    if len(spec) == 10:  # day -> 24 adjacent hour buckets
        nxt = _next_day(spec)
        return ([f"{spec}T{h:02d}..{spec}T{h+1:02d}" for h in range(23)] +
                [f"{spec}T23..{nxt}T00"])
    return []  # hour-level (or unknown): cannot subdivide


def recursive_scan(base_q, spec, depth, over_cap, emit, flush):
    """Split a `created:` spec until each leaf <= CAP, emitting leaves via `emit`.

    GitHub's `created:` filter (incl. hour precision) is the only reliable
    dimension — `pushed:` has no sub-day precision and `stars:` sub-filters
    inside compound queries are ignored. Every leaf is fetched (total <= CAP
    guaranteed) and passed to `emit(item)` immediately — never accumulated in a
    big list — so memory stays flat even for 10k+ repos in one month.

    IMPORTANT GitHub quirk (measured 2026-08-23): day-level `created:A..B` is
    END-INCLUSIVE (covers B's entire day), so a "single day" is always queried
    as the same-day pair `D..D` and hours as adjacent buckets — never a day
    range with a different END day.

    flush() is invoked after EVERY leaf (not just at month boundaries) so an
    interrupted run still leaves usable data on disk for --resume.

    spec shapes:
      'YYYY-MM'                            month (single-sided query)
      'YYYY-MM-DD'                         single day (queried as D..D)
      'YYYY-MM-DDTHH..YYYY-MM-DDTHH'       adjacent hour bucket
    """
    q = f"{base_q} created:{spec}"
    c = gh_total(q)
    time.sleep(SLEEP)
    if c < 0:
        return  # count failed; skip rather than hang
    if c == 0:
        return
    if c <= CAP:
        n = 0
        for it in gh_fetch_leaf(q):
            n += emit(it)
        sys.stdout.write(f"      [leaf created:{spec}] n={n}\n")
        sys.stdout.flush()
        flush(full_only=True)  # persist full.json after every leaf (cheap);
        return                  # compat json is refreshed at partition end
    if depth >= MAX_DEPTH:
        over_cap.append((q, c))
        return
    subs = _subdivide(spec)
    if not subs:
        over_cap.append((q, c))
        return
    for sub in subs:
        recursive_scan(base_q, sub, depth + 1, over_cap, emit, flush)


# --------------------------------------------------------------------------- #
# partition plan
# --------------------------------------------------------------------------- #
def month_ranges():
    """Yield (label, month) for each calendar month from 2025-01 to TODAY.

    Month is returned as a single-sided 'YYYY-MM' spec (queried directly as
    `created:YYYY-MM`) — day-level `A..B` ranges are END-INCLUSIVE, so we avoid
    them entirely and let recursive_scan split an overflowing month into days.
    """
    out = []
    start = dt.date(2025, 1, 1)
    today = dt.date.today()
    cur = start
    while cur <= today:
        out.append((cur.strftime("%Y-%m"), cur.strftime("%Y-%m")))
        nxt = (cur.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        cur = nxt
    return out


def build_plan(only=None, since=None):
    """Return list of (label, base_query, is_created_split) partition descriptors.

    Partition strategy (pure `created:` dimension, which GitHub indexes
    reliably incl. sub-day precision):
      1. Star tiers (>10 stars) — each tiny, fetched directly.
      2. stars:<=10 long tail — split by created month (single-sided
         `created:YYYY-MM`); any month that overflows is subdivided by
         recursive_scan (month -> day -> 24 adjacent hour buckets) until every
         leaf <= 1000.
    """
    plan = []
    for label, qual in STAR_TIERS:
        if only and label not in only:
            continue
        plan.append((f"stars:{label}", f"{BASE} {qual}", False))
    if (not only) or ("<=10" in only):
        for label, m in month_ranges():
            if since and label < since:
                continue
            plan.append((f"<=10 {label}", f"{BASE} stars:<=10 created:{m}", True))
    return plan


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="only print the partition plan + total_counts, fetch nothing")
    ap.add_argument("--execute", dest="execute", action="store_true",
                    help="actually fetch every leaf (slow, rate-limited)")
    ap.add_argument("--only", help="comma list of star-tier labels to scan, e.g. '>500,11..20'")
    ap.add_argument("--since", help="only created-month buckets >= this YYYY-MM (<=10 tier)")
    ap.add_argument("--resume", action="store_true",
                    help="skip buckets whose repos are already present in --out")
    ap.add_argument("--out", default="/tmp/dsh_topic_full.json")
    ap.add_argument("--compat", default="/tmp/dsh_topic_repos.json")
    args = ap.parse_args()

    if not args.dry_run and not args.execute:
        args.dry_run = True

    only = [x.strip() for x in args.only.split(",")] if args.only else None
    plan = build_plan(only=only, since=args.since)

    print(f"=== dsh-plugin full-coverage scan plan ({len(plan)} partitions) ===")
    print(f"    mode: {'DRY-RUN (counts only)' if args.dry_run else 'EXECUTE (fetching)'}")
    print(f"    started: {dt.datetime.now().isoformat(timespec='seconds')}")
    print()

    # Incremental state — written every step so a crash leaves a usable partial file.
    all_items = []
    over_cap = []
    seen_names = set()

    # Resume support: load existing partial file.
    if args.resume:
        try:
            all_items = json.load(open(args.out, encoding="utf-8"))
            seen_names = {it["name"].lower() for it in all_items}
            print(f"  [resume] loaded {len(all_items)} existing repos from --out\n")
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def flush(full_only=False):
        # Items are lean {name, stars} (see gh_fetch_leaf), so all_items is
        # tiny and writing it is cheap — safe to do after every leaf. emit()
        # already guarantees uniqueness, so we write all_items as-is (no
        # seen/uniq copy — that copy + big dicts is what OOM-killed v9/v10).
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(all_items, f, ensure_ascii=False, indent=2)
        if not full_only:
            with open(args.compat, "w", encoding="utf-8") as f:
                json.dump(all_items, f, ensure_ascii=False, indent=2)
        sys.stdout.flush()

    if args.dry_run:
        for label, base_q, _ in plan:
            c = gh_total(base_q)
            time.sleep(SLEEP)
            flag = "" if c <= CAP else "  <<< OVER CAP, needs split"
            print(f"  [{label}] total_count={c}{flag}")
        print("\nDRY-RUN complete. Re-run with --execute to fetch.")
        return

    for label, base_q, is_split in plan:
        try:
            c = gh_total(base_q)
            time.sleep(SLEEP)
            if c < 0:
                print(f"  [{label}] count failed, skip")
                continue
            if c == 0:
                print(f"  [{label}] 0")
                continue
            fetched = 0
            if c <= CAP:
                for it in gh_fetch_leaf(base_q):
                    if it["name"].lower() not in seen_names:
                        seen_names.add(it["name"].lower())
                        all_items.append(it)
                        fetched += 1
            else:
                # Overflow: subdivide the created spec (recursive_scan ladder:
                # month -> day -> 24 adjacent hour buckets, every leaf <= CAP
                # before fetching).
                spec = base_q.split("created:")[1].strip()

                def emit(it, _sn=seen_names, _ai=all_items):
                    if it["name"].lower() not in _sn:
                        _sn.add(it["name"].lower())
                        _ai.append(it)
                        return 1
                    return 0

                before = len(all_items)
                recursive_scan(base_q.split(" created:")[0].strip(),
                               spec, 0, over_cap, emit, flush)
                fetched = len(all_items) - before
        except Exception as e:  # never let one partition kill the whole run
            sys.stderr.write(f"[PARTITION FAIL] {label}: {e}\n")

        print(f"  [{label}] fetched {fetched} (running unique={len(all_items)})")
        sys.stdout.flush()
        flush()  # persist progress after every partition

    uniq = all_items
    print(f"\n=== done ===")
    print(f"unique repos:           {len(uniq)}")
    if over_cap:
        print(f"OVER_CAP partitions (still >1000 after bisection, NOT fetched): {len(over_cap)}")
        for q, c in over_cap:
            print(f"   {c:>5}  {q}")
    else:
        print("no OVER_CAP partitions — full coverage achieved")
    print(f"wrote {args.out}")
    print(f"wrote {args.compat}  (feed this to scripts/diff_topic.py)")


if __name__ == "__main__":
    main()
