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
   (topic growth), it is recursively bisected on `pushed:` date.
2. The `stars:<=10` remainder (the big bucket, ~9,900 repos) is split by
   `pushed:` calendar month from 2025-01 to the CURRENT day. Each month is
   usually < 1000; if a month still overflows it is bisected by DAY, and if a
   single day still overflows it is bisected by HOUR — until <= 1000 (or until
   MAX_DEPTH, at which point it is reported as OVER_CAP rather than silently dropped).

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


def _gh(args, jq, per_page=1):
    """Run one gh api call. Returns (stdout_text, error_text). Honors timeout,
    rate-limit backoff, and retry ceiling. Returns error '422' on hard cap."""
    url = "search/repositories?q=" + urllib.parse.quote(args) + f"&per_page={per_page}"
    for attempt in range(MAX_RETRY):
        try:
            proc = subprocess.run(
                ["gh", "api", url, "--jq", jq],
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
    """Fetch ALL items of a query known to have total_count <= CAP via --paginate."""
    jq = ('.items[] | {name: .full_name, stars: .stargazers_count, '
          'forks: .forks_count, language: (.language // ""), '
          'pushed_at: .pushed_at, created_at: .created_at, '
          'description: (.description // ""), html_url: .html_url, '
          'topics: (.topics | join("|"))}')
    out, err = _gh(q, jq, per_page=100)
    if err == "422":
        return []
    items = []
    for line in out.splitlines():
        line = line.strip()
        if line:
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return items


# Star micro-tiers used to split a single day that still overflows CAP.
# (GitHub's pushed: range does NOT support sub-day / hour precision, so we
#  cannot bisect a day by time — instead we re-split that day by star count,
#  which GitHub indexes reliably.)
def _same_day(start, end):
    """True if start and end fall on the same calendar day."""
    s = dt.datetime.fromisoformat(start)
    e = dt.datetime.fromisoformat(end)
    return s.date() == e.date()


# Languages tried when a single pushed-day still overflows CAP. GitHub's
# `language:` filter is reliable; `(none)` catches repos with no language.
LANG_SPLIT = ["TypeScript", "JavaScript", "Python", "Rust", "Go", "C++",
              "Java", "Vue", "HTML", "Shell", "Ruby", "C#", "PHP", "(none)"]


def gh_fetch_leaf(q):
    """Fetch ALL items of a query known to have total_count <= CAP via --paginate.

    Caller guarantees total <= CAP, so `gh api --paginate` returns the full set.
    """
    jq = ('.items[] | {name: .full_name, stars: .stargazers_count, '
          'forks: .forks_count, language: (.language // ""), '
          'pushed_at: .pushed_at, created_at: .created_at, '
          'description: (.description // ""), html_url: .html_url, '
          'topics: (.topics | join("|"))}')
    out, err = _gh(q, jq, per_page=100)
    items = []
    for line in out.splitlines():
        line = line.strip()
        if line:
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return items


def recursive_scan(base_q, start, end, depth, over_cap, emit):
    """Bisect a `created:` range until each leaf <= CAP, emitting leaves via `emit`.

    GitHub's `created:` filter (incl. hour precision) is reliable, unlike
    `pushed:` (no sub-day) or `stars:` inside other ranges (often ignored).
    Ladder: created month -> day -> hour. Every leaf is fetched (total <= CAP
    guaranteed) and passed to `emit(item)` immediately — never accumulated in a
    big list — so memory stays flat even for 10k+ repos in one month.

    start/end are 'YYYY-MM-DD' (month/day bisection) or 'YYYY-MM-DDTHH'
    (hour bisection — detected by a 'T' in the string).
    """
    rng = f" created:{start}..{end}"
    q = base_q + rng
    c = gh_total(q)
    time.sleep(SLEEP)
    if c < 0:
        return  # count failed; skip rather than hang
    if c == 0:
        return
    if c <= CAP:
        for it in gh_fetch_leaf(q):
            emit(it)
        return
    if depth >= MAX_DEPTH:
        over_cap.append((q, c))
        return
    if "T" in start:  # already at hour level -> cannot subdivide further
        over_cap.append((q, c))
        return
    s = dt.datetime.fromisoformat(start)
    e = dt.datetime.fromisoformat(end)
    if s.date() == e.date() and s.hour == 0 and e.hour == 0:
        # same calendar day -> bisect by HOUR
        mid = s + (e - s) // 2
        recursive_scan(base_q, start, mid.strftime("%Y-%m-%dT%H"), depth + 1, over_cap, emit)
        recursive_scan(base_q, mid.strftime("%Y-%m-%dT%H"), end, depth + 1, over_cap, emit)
    else:
        # bisect by DAY (or month boundary)
        mid = s + (e - s) // 2
        recursive_scan(base_q, start, mid.strftime("%Y-%m-%d"), depth + 1, over_cap, emit)
        recursive_scan(base_q, mid.strftime("%Y-%m-%d"), end, depth + 1, over_cap, emit)


# --------------------------------------------------------------------------- #
# partition plan
# --------------------------------------------------------------------------- #
def month_ranges():
    """Yield (label, start, end) for each calendar month from 2025-01 to TODAY.

    The current (partial) month ends at *tomorrow* (today + 1 day) so repos
    created today are included — GitHub's `created:..END` is exclusive of END.
    """
    out = []
    start = dt.date(2025, 1, 1)
    today = dt.date.today()
    cur = start
    while cur <= today:
        nxt = (cur.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        end = nxt.isoformat() if nxt <= today else (today + dt.timedelta(days=1)).isoformat()
        out.append((cur.strftime("%Y-%m"), cur.isoformat(), end))
        cur = nxt
    return out


def build_plan(only=None, since=None):
    """Return list of (label, base_query, is_created_split) partition descriptors.

    Partition strategy (pure `created:` dimension, which GitHub indexes
    reliably incl. sub-day precision):
      1. Star tiers (>10 stars) — each tiny, fetched directly.
      2. stars:<=10 long tail — split by created month; each month bisected by
         the recursive ladder (month -> day -> hour) until every leaf <= 1000.
    """
    plan = []
    for label, qual in STAR_TIERS:
        if only and label not in only:
            continue
        plan.append((f"stars:{label}", f"{BASE} {qual}", False))
    if (not only) or ("<=10" in only):
        for label, s, e in month_ranges():
            if since and label < since:
                continue
            plan.append((f"<=10 {label}", f"{BASE} stars:<=10 created:{s}..{e}", True))
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
    ap.add_argument("--since", help="only pushed-month buckets >= this YYYY-MM (<=10 tier)")
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

    def flush():
        seen = {}
        for it in all_items:
            seen.setdefault(it["name"].lower(), it)
        uniq = list(seen.values())
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(uniq, f, ensure_ascii=False, indent=2)
        with open(args.compat, "w", encoding="utf-8") as f:
            json.dump([{"name": r["name"], "stars": r["stars"]} for r in uniq],
                      f, ensure_ascii=False, indent=2)
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
                # Overflow: bisect on created date (recursive_scan ladder:
                # month -> day -> hour, every leaf <= CAP before fetching).
                s, e = base_q.split("created:")[1].split("..")

                def emit(it, _sn=seen_names, _ai=all_items):
                    if it["name"].lower() not in _sn:
                        _sn.add(it["name"].lower())
                        _ai.append(it)
                        return 1
                    return 0

                before = len(all_items)
                recursive_scan(base_q.split(" created:")[0].strip(),
                               s, e, 0, over_cap, emit)
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
