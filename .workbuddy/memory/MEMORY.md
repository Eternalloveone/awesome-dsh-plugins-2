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
- **Category enum (gotcha):** the CSV `category` column has drifted to ~66 slugs. The canonical doc
  generator is now `scripts/generate_docs.py`, which reads `data/verified-plugins.csv` and maps each
  `category` slug → one of the companion site's **22 categories** via `SLUG_MAP`. The 22 ids are the
  site's route params: ui-experience, sessions-messages, utilities, desktop, mcp, plugin-tools, web-ui,
  theme, security, chat-im, cli, voice, lists, billing, agents-workflows, integrations-sharing,
  developer-tools, knowledge-research, media-vision, web-browser, ecosystem-resources, fun. Unmapped
  slugs fall back to `utilities`. (The obsolete `insert_verified_into_readme.py` and
  `regen_readme_sections.py` are deleted — do not use them.)
- **README is now an index:** README.md / README.en.md are thin indexes (nav + top-10 per category,
  <600 lines) that point into `docs/categories/`. The full listing lives in `docs/categories/` — 44
  pages (22 category ids × CN/EN: `<id>.md` / `<id>.en.md`). Each page's top link points to the
  matching site category: `https://deepseekharnessplugins.com/plugins/category/<id>`.
- **Regenerate docs:** `python3 scripts/generate_docs.py` (rewrites the README index + all 44 category
  pages, updates nav/badge/snapshot/idempotent w.r.t. CSV). Re-run after any `verified-plugins.csv`
  change.
- **CSV append formats:**
  - `repositories.csv` columns: full_name,html_url,description,category,stars,license,language,
    topics,pushed_at,homepage,verified,sources. `topics` = pipe-separated (`a|b|c`),
    `verified` = `True`/`False`, `pushed_at` = ISO `2026-08-19T00:00:00Z`,
    `sources` = `topic-candidate-snapshot|verified`. Add ONLY `main_dir==true` (loadable) plugins.
  - `dsh-plugin-topic-candidates.csv` columns: repository,topic,review_status.
    `topic` = `dsh-plugin`; add ALL new repos with their `review_status`.
- **Merge order:** backup `data/*.csv` → `merge_audit_verdicts.py <verdicts...>` (audit + verified)
  → append script (repositories + candidates) → `generate_docs.py` (README index + 44 category pages).
- **Website source mismatch (gotcha):** deepseekharnessplugins.com reads its README from
  `cccakeee/awesome-dsh-plugins` (hardcoded `OUR_SOURCE` in the site's `scripts/sync-plugins.ts`),
  NOT this repo; it maps README headings → 22 cats via `SECTION_MAP`. To have the live site ingest
  THIS repo, repoint `OUR_SOURCE` and align `SECTION_MAP`.
- **Commit locally, push pending user confirmation.**
