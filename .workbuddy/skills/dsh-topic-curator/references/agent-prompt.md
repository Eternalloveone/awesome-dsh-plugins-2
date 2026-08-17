# Review-agent prompt template

Copy this template for each new repo discovered above the star floor. Launch one
`general-purpose` agent per repo, **in parallel**. Replace the `<PLACEHOLDERS>`.

```text
You are helping curate a catalog of DeepSeek Harness (DSH) community extensions.
Investigate ONE GitHub repo and return a structured catalog entry. DO NOT write any
files — just return the report in the format at the end.

REPO: <https://github.com/OWNER/REPO>
REPORTED STAR COUNT: ~<STARS>

Context — our curation criteria:
- INCLUDE: public-source projects with reproducible DSH install/mount instructions;
  Cordis/DSH bundles (package.json dsh fields, cordis.patch.yml, or a documented
  `dsh plugin --profile` command); DSH-discoverable skills.
- EXCLUDE from the MAIN directory (mark as "related" or "excluded" instead): projects
  that merely support the DeepSeek API/models; those relying only on the dsh-plugin
  topic tag; tutorials, launchers, DESKTOP SHELLS, generic libraries, and AGGREGATE
  LISTS without a DSH load path; forks of the core harness itself; non-DSH plugins
  (e.g. Claude Code plugins); misleading or unsafe projects.
- Verification labels: verified (native DSH loading evidence + reproducible install),
  skill (DSH skill path inspected), watchlist (incomplete/untested compat), related
  (ecosystem-adjacent, NOT DSH-loadable), excluded (out of scope).
- Risk levels: high (browser session/cookie access, SSH/SFTP/remote exec, external
  chat/IM, privileged creds), medium (external API calls, filesystem/workspace reads,
  task automation, API keys), low (local UI/TUI/theme/client display changes).

Your task:
1. WebFetch the repo main page and its README to learn what it actually is. Be skeptical
   of generic names — they are often forks, mirrors, tutorials, or skeletons.
2. Determine whether it is a genuine DSH plugin/skill/tool WITH A REAL DSH LOAD PATH, or
   an adjacent/standalone project (awesome-list, launcher, desktop shell, core-harness
   fork, Claude Code plugin, generic library).
3. Decide the verdict and whether it belongs in the MAIN directory (repositories.csv) or
   only the candidate list.
4. Gather: description, category (skills|vision|automation|desktop|ui|memory|mcp|agent-os|
   launcher|list|legal|other), license (SPDX id if visible), primary language, homepage,
   whether a DSH load path exists and how, install/usage command or instructions,
   last-push date (ISO if findable), and an honest risk level.

Return EXACTLY this format (fill every line; use "N/A" if truly unknown):
REPO: <owner/repo>
VERDICT: <verified|skill|watchlist|related|excluded>
MAIN_DIR: <yes|no>
DESCRIPTION: <one line>
CATEGORY: <category>
LICENSE: <license>
LANGUAGE: <language>
HOMEPAGE: <url or empty>
DSH_LOAD_PATH: <yes|no — how>
INSTALL_OR_USAGE: <command/instructions or empty>
RISK_LEVEL: <high|medium|low>
TOPICS: <comma-separated>
PUSHED_AT: <ISO date or empty>
NOTES: <anything important for a curator — especially whether this looks like a
fork/mirror/skeleton/tutorial/non-DSH plugin>
```
