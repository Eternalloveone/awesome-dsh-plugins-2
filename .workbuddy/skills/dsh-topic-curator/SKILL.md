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

### 1. Collect topic repos (WebFetch, paginated)

- Fetch `https://github.com/topics/dsh-plugin?page=N` for `N = 1, 2, 3, …` with WebFetch.
- GitHub topic pages are sorted by stars **descending**. Stop scanning when a page is
  empty OR every repo on it is at/below the star floor — all later pages will also be
  at/below the floor, so the sweep is complete.
- For each page, extract `owner/repo` and its star count. Dedupe by lowercased name
  across pages (the topic lists occasionally repeat a repo across pages).
- Save the combined list to a JSON file:
  `[{"name": "owner/repo", "stars": 725}, …]`

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
