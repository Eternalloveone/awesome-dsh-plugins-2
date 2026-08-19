# Project Memory — dsh-plugins curation

## Reusable conventions for the dsh-topic-curator workflow

- **Topic size scaling (CRITICAL):** the `dsh-plugin` GitHub topic now has ~7,900 repos
  (7,888 on 2026-08-19). Do NOT use WebFetch pagination for discovery — it needs ~260 pages.
  Use the authenticated `gh` Search API instead:
  `gh api "search/repositories?q=topic:dsh-plugin&sort=stars&order=desc&per_page=100"`
  (top 1000 by stars = 10 pages). Requires `gh` network access → run Bash with
  `dangerouslyDisableSandbox: true` (the sandbox blocks `gh api` network calls).
- **Diff:** `python3 scripts/diff_topic.py /tmp/topic_repos.json --catalog-dir data --star-floor 10`
  writes `/tmp/dsh_new_repos.json` with `above_floor` / `skipped` arrays of `[name, stars]`.
  Floor rule = skip stars ≤ 10 ("10 个 star 内的先不处理").
- **Verdict vocabulary (gotcha):** agent-prompt.md uses
  `verified/skill/watchlist/related/excluded`; `merge_audit_verdicts.py` expects
  `verified_plugin/verified_skill/rejected/watchlist`. Unify by setting `verdict` == `review_status`
  to one of `verified_plugin | verified_skill | related | rejected | watchlist`.
  Only `verified_plugin`/`verified_skill` get promoted into `verified-plugins.csv`.
- **Category enum (gotcha):** use the detailed enum in `scripts/insert_verified_into_readme.py`
  (web_ui, vision, developer_tools, automation, memory_persona, search_browser, mcp, ecosystem,
  skills, fun, tui, session_chat, data_tools, communication, remote_device, diagnostics,
  uncategorized) — NOT the simplified enum in `references/csv-schema.md` (that file is outdated).
- **CSV append formats:**
  - `repositories.csv` columns: full_name,html_url,description,category,stars,license,language,
    topics,pushed_at,homepage,verified,sources. `topics` = pipe-separated (`a|b|c`),
    `verified` = `True`/`False`, `pushed_at` = ISO `2026-08-19T00:00:00Z`,
    `sources` = `topic-candidate-snapshot|verified`. Add ONLY `main_dir==true` (loadable) plugins.
  - `dsh-plugin-topic-candidates.csv` columns: repository,topic,review_status.
    `topic` = `dsh-plugin`; add ALL new repos with their `review_status`.
- **Merge order:** backup `data/*.csv` → `merge_audit_verdicts.py <verdicts...>` (audit + verified)
  → append script (repositories + candidates) → `insert_verified_into_readme.py` (CN + EN).
  `insert_verified_into_readme.py` is idempotent and backfills older verified rows too.
- **Commit locally, push pending user confirmation.**
