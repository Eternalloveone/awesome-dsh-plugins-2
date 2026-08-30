# CSV schemas (preserve exact column order)

All four files live in `data/`. `scripts/merge_audit_verdicts.py` validates the
headers, existing primary keys, and complete proposed output before replacing the
tables. Do not append or rewrite these tables manually.

## repositories.csv — MAIN directory (genuine DSH-loadable extensions)

```
full_name,html_url,description,category,stars,license,language,topics,pushed_at,homepage,verified,sources
```

- `full_name` — `owner/repo` (lowercase-stable, used as the dedup key).
- `html_url` — `https://github.com/owner/repo`.
- `description` — one-line summary.
- `category` — a fine-grained slug (e.g. `ui`, `model_gateway`, `agent_orchestration`); it
  is mapped to the companion site's 22 capability categories via `SLUG_MAP` in
  `scripts/generate_docs.py`. The 22 human-facing categories are the companion site's
  taxonomy (ids match `https://deepseekharnessplugins.com/plugins/category/<id>`).
- `stars` — integer string.
- `license` — SPDX id if visible (e.g. `MIT`, `Apache-2.0`); note proprietary/EULA explicitly.
- `language` — primary language.
- `topics` — pipe-separated GitHub topics.
- `pushed_at` — ISO date or timestamp of last push.
- `homepage` — project homepage URL or empty.
- `verified` — `True` / `False`.
- `sources` — provenance, e.g. `topic-new|agent-review`.

## dsh-plugin-topic-candidates.csv — discovery / triage list (all topic hits)

```
repository,topic,review_status
```

- `repository` — `owner/repo`.
- `topic` — `dsh-plugin`.
- `review_status` — one of: `unreviewed`, `verified_plugin`, `verified_skill`, `watchlist`,
  `related`, `rejected`.

## verified-plugins.csv — repos with a native DSH load path

```
repository,url,kind,category,install_or_usage,license,last_activity,verification_status,risk_level,verification_source,checked_at,capability,caution
```

- `repository` — `owner/repo`.
- `url` — `https://github.com/owner/repo`.
- `kind` — `dsh_skill` | `installable_dsh_plugin` | `cordis_bundle` | …
- `category` — fine-grained slug, mapped to the site's 22 capability categories via
  `SLUG_MAP` in `scripts/generate_docs.py` (same mapping as `repositories.csv`).
- `install_or_usage` — the author's exact install / mount command or instructions.
- `license` — SPDX id (note proprietary/EULA).
- `last_activity` — ISO date of last push.
- `verification_status` — `verified` | `skill` | `watchlist`.
- `risk_level` — `high` | `medium` | `low`.
- `verification_source` — concrete evidence of the DSH load path.
- `checked_at` — ISO date the review was done.
- `capability` — short description of what it does.
- `caution` — risks / caveats for a curator (license traps, external calls, etc.).

## audit-results.csv — review evidence for every processed repo

```
repo,verdict,reason,capability,install_cmd,license,risk_level,risk_note,category,evidence,checked_at
```

- `repo` — `owner/repo` and the case-insensitive deduplication key.
- `verdict` — `verified_plugin`, `verified_skill`, `watchlist`, `related`, or `rejected`.
- `reason` / `capability` — concise classification and actual behavior.
- `install_cmd` — exact install or mount command when one exists.
- `license`, `risk_level`, `risk_note`, `category`, `evidence`, `checked_at` — the
  reviewed metadata and primary evidence.

## Merge invariants

- Review repositories must exactly equal `above_floor` from `/tmp/dsh_new_repos.json`;
  missing, duplicate, or extra reviews fail before writing.
- Only `verified_plugin` and `verified_skill` may set `main_dir=true` and enter
  `repositories.csv` plus `verified-plugins.csv`.
- Every reviewed repository enters the candidate and audit tables.
- Existing primary keys are checked case-insensitively; conflicting rows fail.
