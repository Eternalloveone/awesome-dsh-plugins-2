# Review-agent prompt template

Use one review agent for a batch of at most six repositories. Run no more than
three agents concurrently. Replace `<REPOSITORIES>` and `<OUTPUT_JSON>`.

```text
You are reviewing a small batch of GitHub repositories for the DeepSeek Harness
(DSH) community catalog.

REPOSITORIES (owner/repo and reported stars):
<REPOSITORIES>

OUTPUT_JSON: <OUTPUT_JSON>

Review every repository in this batch. Do not modify the checked-out project.
Write one top-level JSON array to OUTPUT_JSON, with exactly one object for every
input repository and no extra objects. Do not wrap the JSON in Markdown.

Use primary evidence. At minimum inspect:
1. GitHub metadata: canonical owner/name, fork status, archived state, default
   branch, star count, language, license, topics, and pushed_at.
2. README installation and usage instructions.
3. package.json, especially dsh, dsh.bundle, dsh.profile, exports, and DSH/Cordis
   dependencies.
4. cordis.patch.yml or an equivalent manifest/patch, a concrete plugin apply
   entry, or a DSH-discoverable SKILL.md entry.
5. The exact reproducible install or mount command for anything verified.

A topic, repository description, README claim, package name, or generic
DeepSeek-model support is not enough by itself. Check whether the repository is a
fork or mirror of the core harness, an aggregate list, desktop shell/launcher,
tutorial, non-DSH plugin, or unsafe/misleading project.

Use these verdicts:
- verified_plugin: native DSH/Cordis load evidence plus reproducible install or
  mount path; main_dir must be true.
- verified_skill: concrete DSH-discoverable skill entry plus reproducible
  installation; main_dir must be true.
- watchlist: plausible but incomplete or untested compatibility; main_dir false.
- related: ecosystem-adjacent but not DSH-loadable; main_dir false.
- rejected: out of scope, unavailable, misleading, unsafe, or otherwise
  unsuitable; main_dir false.

Use one category from: ui, vision, automation, desktop, memory, mcp,
agent_orchestration, developer_tools, data_tools, security, chat_integration,
skills, launcher, list, legal, other.

Risk levels:
- high: browser sessions/cookies, SSH/SFTP/remote execution, external chat/IM
  triggers, privileged credentials, or production infrastructure.
- medium: external APIs, filesystem/workspace reads or writes, task automation,
  API keys, budgets, or account data.
- low: local UI/TUI/theme/display behavior without elevated capabilities.

Every object must contain exactly these fields:
{
  "repo": "owner/repo",
  "verdict": "verified_plugin|verified_skill|watchlist|related|rejected",
  "main_dir": true,
  "reason": "concise classification reason",
  "description": "one-line repository description",
  "capability": "one-line user-facing capability",
  "category": "ui",
  "kind": "installable_dsh_plugin",
  "install_or_usage": "exact command or instructions; empty when unverified",
  "license": "SPDX id or Not found",
  "language": "primary language or empty",
  "homepage": "URL or empty",
  "dsh_load_path": "specific positive or negative finding",
  "risk_level": "low|medium|high",
  "risk_note": "why this risk level applies",
  "topics": ["topic-one", "topic-two"],
  "pushed_at": "2026-08-29T00:00:00Z",
  "evidence": "files/metadata inspected and decisive facts",
  "caution": "important caveat or empty",
  "checked_at": "YYYY-MM-DD"
}

For kind, use installable_dsh_plugin, dsh_skill, cordis_bundle, or other. A
verified object requires a non-empty kind, pushed_at, install_or_usage, and
positive dsh_load_path. Unverified objects may leave kind, pushed_at, and
install_or_usage empty when primary metadata is unavailable, but still explain
the negative finding. Use N/A only when a value is genuinely unknown.

If a repository cannot be fetched, return a rejected object with main_dir false
and explain the failure in reason, dsh_load_path, and evidence. Before finishing,
parse OUTPUT_JSON and verify its repository set exactly matches the input batch.
```
