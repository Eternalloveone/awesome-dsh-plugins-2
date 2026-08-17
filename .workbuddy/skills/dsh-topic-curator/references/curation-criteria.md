# Curation criteria (condensed mirror of data/curation-criteria.yaml)

The authoritative source is `data/curation-criteria.yaml`. This file is a quick reference
for review agents and the merge step.

## Include (main directory / verified)

- Public-source projects with reproducible DSH installation or mounting instructions.
- Cordis/DSH bundles declared via `package.json` `dsh` fields, patch files, or verified
  apply entry points.
- DSH-discoverable skills explicitly labelled as skills.

## Exclude from main directory (→ candidate list as `related` / `watchlist`)

- Projects that merely support the DeepSeek API or DeepSeek models.
- Projects relying only on the `dsh-plugin` / `dsh` topic tag as evidence.
- Tutorials, launchers, desktop shells, generic libraries, and aggregate lists (awesome
  lists) without a DSH load path.
- Forks of the core DeepSeek Harness itself (they are the runtime, not extensions).
- Non-DSH plugins (e.g. Claude Code plugins).
- Projects with no public source, no identifiable purpose, or materially misleading claims.

## Verification labels

- `verified` — Native DSH loading evidence **and** a reproducible install / mount path were
  inspected (documented `dsh plugin --profile`, `package.json` `dsh.bundle`/`dsh.profile`,
  `cordis.patch.yml`, or a Cordis apply entry with DSH-compatible deps).
- `skill` — A DSH skill path / entry point was inspected (not an assertion of native bundle
  status).
- `watchlist` — Related project with incomplete or untested compatibility evidence.
- `related` — Ecosystem-adjacent project that is **not** a DSH-loadable plugin.
- `excluded` — Out of scope, unavailable, misleading, or unsafe.

## Risk levels

- `high` — browser session / cookie / authenticated-page access; SSH / SFTP / remote command
  execution / PAM; external chat / IM channels that can trigger agents; privileged credentials
  or production infrastructure.
- `medium` — external API calls (prompts, code, images, search, embeddings, memory);
  filesystem / workspace reads; task automation / scheduling; API keys, budgets, account
  balances.
- `low` — local UI / TUI / theme / client display changes with no elevated capability.

## Review policy

- Do not call a project secure / official / audited / production-ready without strong primary
  evidence.
- Preserve the author's installation command and link to the canonical source.
- Re-check entries after DSH breaking releases (developer preview).
- Place entries with missing licenses or unclear data flows in `watchlist` or disclose the
  uncertainty.
