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
2. The `stars:<=10` remainder is split by `created:` year through 2024 and
   calendar month from 2025 to the CURRENT day. Overflowing periods recurse to
   days and then adjacent hourly buckets until every leaf <= 1000 (or
   MAX_DEPTH, at which point it is reported as OVER_CAP rather than silently
   dropped).

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

Union of (star tiers) + (stars:<=10 split by created year/month/day/hour) == the whole
topic, with no overlap.

OUTPUT
------
--out  (default /tmp/dsh_topic_full.json)   : lean list of {name, stars}
--compat (default /tmp/dsh_topic_repos.json): list of {"name", "stars"} — the
        exact shape `diff_topic.py` consumes. Extra keys in --out are ignored by it.
--summary (default /tmp/dsh_topic_scan_summary.json): machine-readable status,
        partition counts, failures, and over-cap partitions.

RELIABILITY
-----------
- Every `gh` call has a 60s timeout so a stuck subprocess can never hang the run.
- Results are written INCREMENTALLY (flush after every leaf) so a crash/interrupt
  leaves a usable partial file, and progress is observable in the log.
- Partial output is never considered success: count, fetch, parse, or partition
  failures produce a non-zero exit code and `coverage_ok: false`.
- No global API call cap: rate-limit backoff + timeout + MAX_DEPTH guard against
  runaway loops. (An earlier version capped at 400 calls and silently dropped the
  remaining ~9,900 repos of the 2026-08 bucket — that bug is fixed.)

USAGE
-----
  python3 full_topic_scan.py --dry-run            # print partition plan + counts only
  python3 full_topic_scan.py --execute            # actually fetch everything (slow)
  python3 full_topic_scan.py --execute --actionable-only # only stars > 10
  python3 full_topic_scan.py --execute --only ">500"   # fetch just the >500 star tier
  python3 full_topic_scan.py --execute --since 2026-06 # only months >= 2026-06
  python3 full_topic_scan.py --execute --resume   # reuse output for dedupe; recheck buckets

Requires `gh` authenticated (run the Bash tool with dangerouslyDisableSandbox: true;
the sandbox blocks gh's network calls).
"""
import argparse
import calendar
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
from zoneinfo import ZoneInfo

BASE = "topic:dsh-plugin"
CAP = 1000            # Search API hard ceiling per query
MAX_DEPTH = 14        # bisection depth guard (day -> hour -> finer)
SLEEP = 1.0           # seconds between gh calls (stay under 30 search req/min)
GH_TIMEOUT = 60       # hard timeout per gh subprocess (seconds)
MAX_RETRY = 6         # per-call retry ceiling
FIRST_GITHUB_YEAR = 2008
MONTH_BUCKET_START_YEAR = 2025
SHANGHAI = ZoneInfo("Asia/Shanghai")

RETRYABLE_ERROR_MARKERS = (
    "eof", "connection reset", "connection refused", "connection aborted",
    "temporary failure", "timed out", "timeout", "tls", "network is unreachable",
    "rate limit", "secondary rate limit", "http 429", "http 502", "http 503",
    "http 504",
)

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
    last_error = "unknown gh failure"
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
            err = f"timeout after {GH_TIMEOUT}s"
        except OSError as exc:
            err = f"{type(exc).__name__}: {exc}"
        else:
            if proc.returncode == 0:
                return proc.stdout, ""
            err = (proc.stderr or "").strip()
            if not err:
                err = f"gh exited with status {proc.returncode}"
            if "422" in err and "first 1000" in err:
                sys.stderr.write(f"[422 cap] q={args}\n")
                return "", "search cap exceeded (HTTP 422)"

        last_error = err
        retryable = any(marker in err.lower() for marker in RETRYABLE_ERROR_MARKERS)
        if retryable and attempt + 1 < MAX_RETRY:
            delay = min(30, 2 ** attempt)
            sys.stderr.write(
                f"[gh retry] q={args} attempt={attempt + 1}/{MAX_RETRY}; "
                f"retrying in {delay}s: {err}\n"
            )
            time.sleep(delay)
            continue
        if retryable:
            err = f"exhausted retries: {err}"
        sys.stderr.write(f"[gh ERROR] q={args}\n{err}\n")
        return "", err
    return "", f"exhausted retries: {last_error}"


def gh_total(q):
    """Return ``(total_count, error)`` for a search query."""
    out, err = _gh(q, ".total_count", per_page=1)
    if err:
        return -1, err
    try:
        return int(out.strip()), ""
    except ValueError:
        return -1, f"invalid total_count output: {out.strip()!r}"


def gh_fetch_leaf(q, expected_count):
    """Fetch a complete leaf and compare it with its count query.

    Caller guarantees total <= CAP, so `gh api --paginate` returns the full set.
    Items are kept LEAN ({name, stars}) on purpose: 7k+ repos with description
    etc. (~100MB) repeatedly OOM-killed this run on a memory-tight machine
    (2026-08-23); downstream diff/audit only ever needs name + stars (audit
    agents WebFetch the repo themselves).
    """
    jq = '.items[] | {name: .full_name, stars: .stargazers_count}'
    out, err = _gh(q, jq, per_page=100, paginate=True)
    if err:
        return [], err
    items = []
    parse_errors = 0
    for line in out.splitlines():
        line = line.strip()
        if line:
            try:
                item = json.loads(line)
                if not isinstance(item, dict) or not item.get("name"):
                    parse_errors += 1
                else:
                    items.append(item)
            except json.JSONDecodeError:
                parse_errors += 1
    if parse_errors:
        return [], f"{parse_errors} invalid JSON item(s) in gh output"
    if len(items) < expected_count:
        return [], f"count mismatch: expected at least {expected_count}, fetched {len(items)}"
    return items, ""


def _today_shanghai():
    return dt.datetime.now(SHANGHAI).date()


def _record_failure(failures, stage, query, error):
    failures.append({"stage": stage, "query": query, "error": str(error)})


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
    today = _today_shanghai()
    if m == today.strftime("%Y-%m"):
        ndays = today.day
    return [dt.date(y, mo, d).isoformat() for d in range(1, ndays + 1)]


def _subdivide(spec):
    """Return child created-specs covering `spec`, or [] if it cannot be split.

    Granularity by spec shape:
      'YYYY'              -> each month of that year ('YYYY-MM')
      'YYYY-MM'           -> each day of that month ('YYYY-MM-DD')
      'YYYY-MM-DD'        -> 24 adjacent hour buckets
                             ('D T00..D T01', ..., 'D T22..D T23', 'D T23..D+1 T00')
      hour-level '..'     -> cannot split finer (1h is the finest granularity
                             we trust) -> caller marks OVER_CAP

    See module docstring for the END-INCLUSIVE day-range quirk that forces
    this same-day / adjacent-bucket design.
    """
    if len(spec) == 4:  # year -> months
        year = int(spec)
        today = _today_shanghai()
        last_month = today.month if year == today.year else 12
        return [f"{year:04d}-{month:02d}" for month in range(1, last_month + 1)]
    if len(spec) == 7:  # month -> days
        return _days_in_month(spec)
    if len(spec) == 10:  # day -> 24 adjacent hour buckets
        nxt = _next_day(spec)
        return ([f"{spec}T{h:02d}..{spec}T{h+1:02d}" for h in range(23)] +
                [f"{spec}T23..{nxt}T00"])
    return []  # hour-level (or unknown): cannot subdivide


def recursive_scan(base_q, spec, depth, over_cap, failures, emit, flush, stats):
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
      'YYYY'                              year (single year)
      'YYYY-MM'                            month (single-sided query)
      'YYYY-MM-DD'                         single day (queried as D..D)
      'YYYY-MM-DDTHH..YYYY-MM-DDTHH'       adjacent hour bucket
    """
    q = f"{base_q} created:{spec}"
    c, err = gh_total(q)
    stats["count_queries"] += 1
    time.sleep(SLEEP)
    if err:
        _record_failure(failures, "count", q, err)
        return
    if c == 0:
        return
    if c <= CAP:
        items, fetch_error = gh_fetch_leaf(q, c)
        stats["fetch_queries"] += 1
        if fetch_error:
            _record_failure(failures, "fetch", q, fetch_error)
            return
        n = 0
        for it in items:
            n += emit(it)
        stats["leaves"] += 1
        sys.stdout.write(f"      [leaf created:{spec}] n={n}\n")
        sys.stdout.flush()
        flush(full_only=True)  # persist full.json after every leaf (cheap);
        return                  # compat json is refreshed at partition end
    if depth >= MAX_DEPTH:
        over_cap.append({"query": q, "count": c})
        return
    subs = _subdivide(spec)
    if not subs:
        over_cap.append({"query": q, "count": c})
        return
    for sub in subs:
        recursive_scan(base_q, sub, depth + 1, over_cap, failures,
                       emit, flush, stats)


# --------------------------------------------------------------------------- #
# partition plan
# --------------------------------------------------------------------------- #
def created_periods():
    """Yield disjoint created-time periods from GitHub's launch through today.

    Older history is sparse enough for year buckets. Recent history uses months,
    with recursive day/hour splitting only when a bucket exceeds the API cap.
    """
    out = []
    today = _today_shanghai()
    for year in range(FIRST_GITHUB_YEAR, min(MONTH_BUCKET_START_YEAR, today.year + 1)):
        out.append((f"{year:04d}", f"{year:04d}"))
    cur = dt.date(MONTH_BUCKET_START_YEAR, 1, 1)
    while cur <= today:
        out.append((cur.strftime("%Y-%m"), cur.strftime("%Y-%m")))
        nxt = (cur.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        cur = nxt
    return out


def build_plan(only=None, since=None, actionable_only=False):
    """Return list of (label, base_query, is_created_split) partition descriptors.

    Partition strategy (pure `created:` dimension, which GitHub indexes
    reliably incl. sub-day precision):
      1. Star tiers (>10 stars) — each tiny, fetched directly.
      2. stars:<=10 long tail — split by created year before 2025 and month
         afterward. Any overflowing period recurses to day/hour leaves.

    ``actionable_only`` excludes the <=10-star remainder used by the daily run.
    """
    plan = []
    for label, qual in STAR_TIERS:
        if only and label not in only:
            continue
        plan.append((f"stars:{label}", f"{BASE} {qual}", False))
    if not actionable_only and ((not only) or ("<=10" in only)):
        for label, period in created_periods():
            if since and label < since:
                continue
            plan.append((f"<=10 {label}",
                         f"{BASE} stars:<=10 created:{period}", True))
    return plan


def write_json_atomic(path, payload):
    """Atomically publish a JSON artifact so readers never see a half-write."""
    target = os.path.abspath(os.fspath(path))
    directory = os.path.dirname(target) or "."
    fd, temporary = tempfile.mkstemp(
        prefix=f".{os.path.basename(target)}.", suffix=".tmp", dir=directory
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--dry-run", action="store_true",
                    help="only print the partition plan + total_counts, fetch nothing")
    ap.add_argument("--execute", dest="execute", action="store_true",
                    help="actually fetch every leaf (slow, rate-limited)")
    ap.add_argument("--actionable-only", action="store_true",
                    help="scan only the disjoint stars > 10 tiers (daily mode)")
    ap.add_argument("--only", help="comma list of star-tier labels to scan, e.g. '>500,11..20'")
    ap.add_argument("--since", help="only created buckets >= this YYYY-MM (<=10 tier)")
    ap.add_argument("--resume", action="store_true",
                    help="load --out for dedupe while rechecking every selected bucket")
    ap.add_argument("--out", default="/tmp/dsh_topic_full.json")
    ap.add_argument("--compat", default="/tmp/dsh_topic_repos.json")
    ap.add_argument("--summary", default="/tmp/dsh_topic_scan_summary.json",
                    help="write the machine-readable run gate here")
    args = ap.parse_args(argv)

    if args.dry_run and args.execute:
        ap.error("--dry-run and --execute are mutually exclusive")
    if not args.dry_run and not args.execute:
        args.dry_run = True
    if args.actionable_only and args.only:
        ap.error("--actionable-only and --only are mutually exclusive")
    if args.actionable_only and args.since:
        ap.error("--actionable-only and --since are mutually exclusive")
    if args.since:
        try:
            dt.datetime.strptime(args.since, "%Y-%m")
        except ValueError:
            ap.error("--since must use a valid YYYY-MM month")

    only = [label for label, _ in STAR_TIERS] if args.actionable_only else (
        [x.strip() for x in args.only.split(",") if x.strip()]
        if args.only else None
    )
    valid_labels = {label for label, _ in STAR_TIERS} | {"<=10"}
    unknown_labels = sorted(set(only or []) - valid_labels)
    if unknown_labels:
        ap.error(f"unknown --only labels: {', '.join(unknown_labels)}")
    if args.since and only and "<=10" not in only:
        ap.error("--since applies only when the <=10 history is selected")
    plan = build_plan(only=only, since=args.since,
                      actionable_only=args.actionable_only)
    if not plan:
        ap.error("the selected filters produced no scan partitions")

    started_at = dt.datetime.now(SHANGHAI).isoformat(timespec="seconds")
    stats = {
        "planned_partitions": len(plan),
        "completed_partitions": 0,
        "count_queries": 0,
        "fetch_queries": 0,
        "leaves": 0,
    }
    failures = []
    over_cap = []

    print(f"=== dsh-plugin full-coverage scan plan ({len(plan)} partitions) ===")
    print(f"    mode: {'DRY-RUN (counts only)' if args.dry_run else 'EXECUTE (fetching)'}")
    print(f"    scope: {'actionable (>10 stars)' if args.actionable_only else 'full topic'}")
    print(f"    started: {started_at}")
    print()

    # Incremental state — written every step so a crash leaves a usable partial file.
    all_items = []
    seen_names = set()

    if args.resume:
        try:
            with open(args.out, encoding="utf-8") as f:
                all_items = json.load(f)
            if not isinstance(all_items, list):
                raise ValueError("resume output must contain a JSON array")
            seen_names = {it["name"].lower() for it in all_items}
            print(f"  [resume] loaded {len(all_items)} existing repos from --out\n")
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def build_summary(status="running", coverage_ok=False, finished_at=None):
        return {
            "mode": "dry-run" if args.dry_run else (
                "daily" if args.actionable_only else "weekly"
            ),
            "actionable_only": args.actionable_only,
            "star_floor": 10,
            "status": status,
            "coverage_ok": bool(coverage_ok),
            "stats": stats,
            "unique_repos": len(all_items),
            "failures": failures,
            "over_cap": over_cap,
            "started_at": started_at,
            "finished_at": finished_at,
            "out": args.out,
            "compat": args.compat,
        }

    def persist_summary(status="running", coverage_ok=False, finished_at=None):
        write_json_atomic(
            args.summary,
            build_summary(status=status, coverage_ok=coverage_ok,
                          finished_at=finished_at),
        )

    def flush(full_only=False):
        # Items are lean {name, stars}; atomic writes keep readers from seeing
        # partial JSON while the long scan is in progress.
        write_json_atomic(args.out, all_items)
        if not full_only:
            write_json_atomic(args.compat, all_items)
        persist_summary()
        sys.stdout.flush()

    # Invalidate any old summary before network calls. A killed process leaves
    # this run in a non-success state instead of reusing a previous run.
    persist_summary()
    flush()

    if args.dry_run:
        for label, base_q, _ in plan:
            c, err = gh_total(base_q)
            stats["count_queries"] += 1
            time.sleep(SLEEP)
            if err:
                _record_failure(failures, "count", base_q, err)
                print(f"  [{label}] count failed: {err}")
                persist_summary()
                continue
            if c > CAP:
                over_cap.append({"query": base_q, "count": c})
            flag = "" if c <= CAP else "  <<< OVER CAP, needs split"
            print(f"  [{label}] total_count={c}{flag}")
            if c <= CAP:
                stats["completed_partitions"] += 1
            persist_summary()
        persist_summary(
            status="dry-run",
            coverage_ok=False,
            finished_at=dt.datetime.now(SHANGHAI).isoformat(timespec="seconds"),
        )
        print("\nDRY-RUN complete. Re-run with --execute to fetch.")
        return 2 if failures or over_cap else 0

    exit_code = 0
    for label, base_q, is_split in plan:
        failure_count_before = len(failures)
        over_cap_count_before = len(over_cap)
        fetched = 0
        try:
            c, err = gh_total(base_q)
            stats["count_queries"] += 1
            time.sleep(SLEEP)
            if err:
                _record_failure(failures, "count", base_q, err)
                print(f"  [{label}] count failed: {err}")
            elif c == 0:
                print(f"  [{label}] 0")
            elif c <= CAP:
                items, fetch_error = gh_fetch_leaf(base_q, c)
                stats["fetch_queries"] += 1
                if fetch_error:
                    _record_failure(failures, "fetch", base_q, fetch_error)
                    print(f"  [{label}] fetch failed: {fetch_error}")
                else:
                    stats["leaves"] += 1
                    for it in items:
                        key = it["name"].lower()
                        if key not in seen_names:
                            seen_names.add(key)
                            all_items.append(it)
                            fetched += 1
            else:
                partition_names = set()

                def emit(it, _sn=seen_names, _ai=all_items):
                    key = it["name"].lower()
                    partition_names.add(key)
                    if key not in _sn:
                        _sn.add(key)
                        _ai.append(it)
                        return 1
                    return 0

                before = len(all_items)
                if is_split:
                    spec = base_q.split("created:", 1)[1].strip()
                    split_base = base_q.split(" created:", 1)[0].strip()
                    recursive_scan(split_base, spec, 0, over_cap, failures,
                                   emit, flush, stats)
                else:
                    for _, spec in created_periods():
                        recursive_scan(base_q, spec, 0, over_cap, failures,
                                       emit, flush, stats)
                fetched = len(all_items) - before
                if (len(failures) == failure_count_before and
                        len(over_cap) == over_cap_count_before and
                        len(partition_names) < c):
                    _record_failure(
                        failures, "partition", base_q,
                        f"partition count mismatch: expected at least {c}, "
                        f"observed {len(partition_names)} unique repos",
                    )
        except Exception as exc:  # preserve the failure in the machine summary
            sys.stderr.write(f"[PARTITION FAIL] {label}: {exc}\n")
            _record_failure(failures, "partition", label, exc)

        if (len(failures) == failure_count_before and
                len(over_cap) == over_cap_count_before):
            stats["completed_partitions"] += 1
        print(f"  [{label}] fetched {fetched} (running unique={len(all_items)})")
        sys.stdout.flush()
        flush()

    print("\n=== done ===")
    print(f"unique repos:           {len(all_items)}")
    if over_cap:
        print(f"OVER_CAP partitions (still >1000 after bisection, NOT fetched): {len(over_cap)}")
        for item in over_cap:
            print(f"   {item['count']:>5}  {item['query']}")
    else:
        print("no OVER_CAP partitions — full coverage achieved")
    if failures:
        print(f"failed queries/partitions: {len(failures)}")
        for failure in failures:
            print(f"   [{failure['stage']}] {failure['query']}: {failure['error']}")

    coverage_ok = bool(
        not failures and not over_cap and
        stats["completed_partitions"] == stats["planned_partitions"]
    )
    persist_summary(
        status="succeeded" if coverage_ok else "failed",
        coverage_ok=coverage_ok,
        finished_at=dt.datetime.now(SHANGHAI).isoformat(timespec="seconds"),
    )
    print(f"wrote {args.out}")
    print(f"wrote {args.compat}  (feed this to scripts/diff_topic.py)")
    print(f"wrote {args.summary}  (coverage_ok={coverage_ok})")
    return 0 if coverage_ok else max(exit_code, 2)


if __name__ == "__main__":
    sys.exit(main())
