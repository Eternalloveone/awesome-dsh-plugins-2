---
name: dsh-topic-curator
description: Scan the GitHub `dsh-plugin` topic for new DeepSeek Harness community extensions, diff them against the local catalog CSVs, dispatch parallel review agents, and merge qualifying repos (above the star floor) into repositories.csv / dsh-plugin-topic-candidates.csv / verified-plugins.csv per the project's curation rules. This skill should be used when the user asks to refresh, sync, or "添砖加瓦" the DSH plugin catalog from the GitHub topic, or to audit newly tagged repos.
agent_created: true
---

# DSH Topic Curator

Keep `data/repositories.csv`, `data/dsh-plugin-topic-candidates.csv`, and
`data/verified-plugins.csv` in sync with the GitHub `dsh-plugin` topic, adding only
genuine, qualifying extensions and respecting the star floor.

## When to use

- The user asks to scan / refresh / sync the `dsh-plugin` GitHub topic into the catalog.
- The user reports "the topic has new repos" and wants them vetted and merged.
- Periodic catalog maintenance ("继续扫", "再扫一轮").

## Workflow

### 1. Collect topic repos (gh Search API, paginated)

- The `dsh-plugin` topic exploded to **~10,600 repos** (2026-08; 9923 of them were
  `pushed` in 2026-08 alone). It is far too big for WebFetch pagination (~260 pages).
- **Search API hard cap:** every query returns at most **1000 results**
  (`page=11` → HTTP 422 "Only the first 1000 search results are available"). A single
  `sort=stars` query therefore only ever sees the top-1000-by-stars — missing the
  ~9,900 long-tail repos where genuine new small plugins hide.
- **Full-coverage scan (recommended):** use
  `scripts/full_topic_scan.py`. It partitions the topic into disjoint sub-queries
  (star tiers for `>10`, then the `stars:<=10` remainder split by `created:` month —
  single-sided `created:YYYY-MM`; an overflowing month is split into its days and a
  day into 24 adjacent hour buckets) so every leaf is fully
  retrievable, then dedupes by repo name. Outputs both a rich JSON and a
  `diff_topic.py`-compatible `{name, stars}` list.
  - `python3 scripts/full_topic_scan.py --dry-run` → print the partition plan + counts.
  - `python3 scripts/full_topic_scan.py --execute` → fetch everything (rate-limited,
    ~9 min; run Bash with `dangerouslyDisableSandbox: true`).
  - `--only ">500,11..20` / `--since 2026-06` to scope a run.
  - Writes `/tmp/dsh_topic_full.json` (rich) and `/tmp/dsh_topic_repos.json` (compat).
  - **GOTCHA (measured 2026-08-23):** day-level `created:A..B` is END-INCLUSIVE —
    `created:2026-08-13..2026-08-14` = 522 + 1702 = both days. Never write a day
    range with a different END day; query a single day as `D..D`, a month as
    single-sided `YYYY-MM`, and hours as adjacent buckets `T00..T01, T01..T02, ...`.
- **Quick top-1000 only (legacy):** if you only want the popular slice,
  `gh api "search/repositories?q=topic:dsh-plugin&sort=stars&order=desc&per_page=100&page=N" --jq '.items[] | {name: .full_name, stars: .stargazers_count}'`
  for N=1..10, then `jq -s . > topic_repos.json`. The diff script's star floor makes
  deeper pages irrelevant for curation.
- Dedupe by lowercased name (the topic occasionally repeats a repo).

### 2. Diff against the catalog

- Run `scripts/diff_topic.py <topic_repos.json> --catalog-dir data --star-floor 10`.
  - Default floor = `10`: repos with `stars <= 10` are skipped (per "10 个 star 内的先不处理").
    To include 10-star repos, pass `--star-floor 9`.
  - The script reports NEW repos (absent from both `repositories.csv` and
    `dsh-plugin-topic-candidates.csv`), split into `above_floor` (to process) and
    `skipped` (below floor). It also writes `/tmp/dsh_new_repos.json`.

### 3. Dispatch parallel review agents

- For **each** new repo above the floor, launch a `general-purpose` agent **in parallel**
  using the prompt template in `references/agent-prompt.md`.
- Pass the agent the repo URL, reported star count, and the curation context. Instruct it
  to WebFetch the repo + README and return the fixed-format catalog entry. Agents MUST NOT
  write files — they only report.
- WebFetch is the only reliable fetch path here (the GitHub API is unauthenticated and
  rate-limited). One agent per repo keeps reviews independent and fast.

### 4. Classify & place each repo

Use `references/curation-criteria.md` (mirrors `data/curation-criteria.yaml`, the source of
truth) and `references/csv-schema.md`:

- `verdict` ∈ {verified, skill, watchlist, related, excluded}
- `MAIN_DIR = yes` ONLY when there is a real DSH load path: native Cordis bundle, a
  documented `dsh plugin --profile` command, a `cordis.patch.yml` mount, or skills
  installed into `~/.dsh`. Aggregate lists (awesome-lists), desktop shells / launchers,
  forks of the core harness itself, and non-DSH plugins (e.g. Claude Code plugins) go to the
  **candidate list only** (`related` / `watchlist`) — never `repositories.csv`.
- Repos with a native DSH load path: add to `repositories.csv` (main) **and**
  `verified-plugins.csv`.
- All newly discovered repos: add a row to `dsh-plugin-topic-candidates.csv` with an
  appropriate `review_status` (`verified_plugin` / `verified_skill` / `watchlist` /
  `related`).

### 5. Merge (back up first)

- Back up the three CSVs before editing: `cp data/*.csv /tmp/`.
- Append rows with `csv.DictWriter` using the exact header order in
  `references/csv-schema.md`. Never rewrite existing rows.
- Verify row counts increased as expected and that the new `full_name`s are present.

### 5b. Regenerate documentation

- After promoting verified verdicts into `data/verified-plugins.csv`, run
  `python3 scripts/generate_docs.py`. This regenerates the README index (a compact
  navigation index that links out to the category pages) and the `docs/categories/*.md`
  category pages (each holding the FULL listing of verified repos in that category). It
  also refreshes the verified-count badge and the snapshot date. The README and
  `docs/categories/` structure follows the companion site's 22 categories (ids match
  `https://deepseekharnessplugins.com/plugins/category/<id>`); the CSV `category` slug is
  mapped to those categories via `SLUG_MAP` in `scripts/generate_docs.py`.

### 6. Log

- Append a brief note to `.workbuddy/memory/YYYY-MM-DD.md` (create if missing): pages
  scanned, new repos found / merged, and the floor used.

## Notes / gotchas

- Topic pages can duplicate repos across pages, and WebFetch star counts are approximate —
  dedupe and treat the floor as a guideline, not gospel.
- Most topic repos are already catalogued; expect a low new-repo rate. The value is
  confirming completeness, not bulk-adding.
- Do NOT describe a project as secure / official / audited / production-ready without strong
  primary evidence (`review_policy` in the criteria).
- Re-check entries after DSH breaking releases, since the ecosystem is in developer preview.
