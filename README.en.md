# awesome-dsh-plugins

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
![Plugins](https://img.shields.io/badge/plugins-51-2563eb)
![Skills](https://img.shields.io/badge/skills-3-7c3aed)
![License](https://img.shields.io/badge/license-MIT-f59e0b)

**English** | [简体中文](README.md)

> A curated, evidence-led directory for [DeepSeek Harness (DSH)][1]. It distinguishes loadable Cordis/DSH extensions from skills, launchers, ordinary DeepSeek applications, and projects that only added a GitHub topic.

DeepSeek Harness is in **Developer Preview** and uses Cordis' “Everything is a plugin” architecture. A DSH profile composes bundles; external extensions commonly declare their loading mechanism through a `dsh` field in `package.json` and a patch file.[1] [2] Test every installation against your own DSH release before relying on it.

**Snapshot: 2026-08-13.** This edition includes **51 native DSH extensions whose source or install manifests were inspected**, **3 DSH skills**, and a topic snapshot of the GitHub discovery pool. The official [`dsh-plugin` topic][3] showed 346 repositories during research, but a topic is not an installation, compatibility, maintenance, or security certification.

| Navigation | Purpose |
| --- | --- |
| [Native DSH extensions](#native-dsh-extensions) | Bundles, Cordis extensions, and Web-client add-ons with verified DSH loading evidence |
| [DSH skills](#dsh-skills) | Discoverable skills; they are not presented as native Cordis bundles |
| [Built-in DSH components](#official-built-in-capabilities-not-community-plugins) | Runtime components shipped in the official source tree |
| [Watchlist and related projects](#watchlist-and-related-projects) | Related but unverified or non-loadable projects |
| [Safety](#installation-and-safety) | Permission-aware installation guidance |

## Native DSH extensions

An entry in this section has at least one verified native signal: a reproducible `dsh plugin` command, a `dsh.bundle` / `cordis.patch.yml` declaration, or a DSH-compatible Cordis `apply` entry. **Verified does not mean audited, endorsed, safe, or stable.** Use each project’s linked README as the canonical installation source.

### Vision and multimodal

| Extension | Capability | Installation / source | License and caution |
| --- | --- | --- | --- |
| [liustack/modlens](https://github.com/liustack/modlens) | OCR, layout and semantic visual evidence | `npx -y @deepseek-ai/dsh plugin --profile web add @liustack/modlens` | MIT; requires a usable vision engine |
| [Scorp1o117/dsh-tool-vision](https://github.com/Scorp1o117/dsh-tool-vision) | `inspect_image` with OpenAI-compatible vision endpoints | Mount in `cordis.patch.yml`; see [README](https://github.com/Scorp1o117/dsh-tool-vision) | MIT; images can leave the machine |
| [TiankunDai/dsh-vision-LMstudio](https://github.com/TiankunDai/dsh-vision-LMstudio) | Local LM Studio vision models | `dsh plugin --profile web add link:<repo>/packages/dsh-lmstudio-vision` | BSD-3-Clause; reads local images or clipboard |

### Web UI, TUI, and developer experience

| Extension | Capability | Installation / source | License and caution |
| --- | --- | --- | --- |
| [zhu1090093659/dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) | Web UI plug-ins and skins: board, Git graph, mobile UI, Token view | `dsh plugin --profile web add @linxin666/dsh-web-ui-all` | BSD-3-Clause; verify the specific package release |
| [Ericwong5021/dsh-taskboard](https://github.com/Ericwong5021/dsh-taskboard) | Web task board | `dsh plugin --profile <profile> add github:Ericwong5021/dsh-taskboard` | MIT; early-stage project |
| [GooodWei/dsh-command-context](https://github.com/GooodWei/dsh-command-context) | `/context` token allocation, compaction and cost view | `npx @deepseek-ai/dsh plugin --profile web add github:GooodWei/dsh-command-context` | MIT; no stable release found |
| [zhaoscsc/dsh-wikilink](https://github.com/zhaoscsc/dsh-wikilink) | Obsidian-style `[[wikilink]]` references | `dsh plugin --profile web add https://github.com/zhaoscsc/dsh-wikilink/archive/refs/heads/main.tar.gz` | MIT; may need re-patching after DSH reinstall |
| [omdsh-dev/dsh-open-in-vscode](https://github.com/omdsh-dev/dsh-open-in-vscode) | Open a workspace in VS Code from the Web UI | `dsh plugin --profile web add https://github.com/omdsh-dev/dsh-open-in-vscode/archive/refs/tags/v0.1.5.tar.gz` | MIT; invokes local editor CLI |
| [omdsh-dev/dsh-notification](https://github.com/omdsh-dev/dsh-notification) | Desktop turn-completion notifications | `dsh plugin --profile web add https://github.com/omdsh-dev/dsh-notification/archive/refs/heads/main.tar.gz` | MIT; notifications may expose session output |
| [openguardrails/dsh-tui](https://github.com/openguardrails/dsh-tui) | Terminal UI and session resumption | `dsh plugin --profile tui add github:openguardrails/dsh-tui` | MIT; pre-release compatibility may change |
| [ccch1mneyyy/dsh-cc-tui](https://github.com/ccch1mneyyy/dsh-cc-tui) | Claude Code-style full-screen terminal UI | `dsh plugin --profile cc-tui add dsh-cc-tui` | BSD-3-Clause; requires Node.js 22.19+ |
| [dingyi222666/dsh-session-notification](https://github.com/dingyi222666/dsh-session-notification) | Session-status notifications and sound | `dsh plugin --profile web add @dingyi222666/dsh-session-notification` | BSD-3-Clause; needs browser notification permission |
| [dingyi222666/dsh-focus-chat](https://github.com/dingyi222666/dsh-focus-chat) | Focused conversation view | `dsh plugin --profile web add @dingyi222666/dsh-focus-chat` | BSD-3-Clause; third-party Web UI injection |
| [omdsh-dev/DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) | Sidebar workbench for files, terminal, Git, subagents and browser | See [README](https://github.com/omdsh-dev/DSH-better-sidebar); its published installer is `curl | bash`, so inspect it first | MIT; can read/write files and execute shell commands |
| [BruceWu1126/dsh-web-background](https://github.com/BruceWu1126/dsh-web-background) | Web UI background customization | `git clone … && node install.mjs` | MIT; installer changes local DSH files |
| [Proton1917/dsh-live-stats](https://github.com/Proton1917/dsh-live-stats) | Live token usage and throughput | Load with a local link and `--patch`; see [README](https://github.com/Proton1917/dsh-live-stats) | BSD-3-Clause; reads session projections |
| [XYZ1024-alt/dsh-side-panel](https://github.com/XYZ1024-alt/dsh-side-panel) | Files, session history, Git status and diff side panel | `dsh plugin --profile web add github:XYZ1024-alt/dsh-side-panel` | MIT; local file/Git access; keep loopback-only |
| [titanwings/dsh-plannotator](https://github.com/titanwings/dsh-plannotator) | Anchored plan review and annotations | `dsh plugin --profile web add github:titanwings/dsh-plannotator#v0.1.3` | MIT; injects into conversation rendering |
| [hellodigua/dsh-share](https://github.com/hellodigua/dsh-share) | Render and share a current conversation as PNG | `dsh plugin --profile web add --ignore-scripts --config.auto-install-peers=false 'github:hellodigua/dsh-share#v0.1.0'` | MIT; reads chat DOM and clipboard |
| [hellodigua/dsh-emoji](https://github.com/hellodigua/dsh-emoji) | Emoji presentation, asset management, and output rewrite | Fixed-RC local bundle; see [README](https://github.com/hellodigua/dsh-emoji) | MIT; prompt/output injection and ZIP uploads |
| [omdsh-dev/dsh-gomoku](https://github.com/omdsh-dev/dsh-gomoku) | Gomoku demo-profile extension | `dsh plugin --profile demo add github:omdsh-dev/dsh-gomoku` | MIT; sends content to the selected model |
| [chen-001/dsh-grok-tui](https://github.com/chen-001/dsh-grok-tui) | grok-build TUI bridge for DSH | `npm install -g dsh-grok-tui && grok-dsh setup` | MIT; writes `~/.dsh` configuration |

### Search, browser, automation, and workflow

| Extension | Capability | Installation / source | License and caution |
| --- | --- | --- | --- |
| [gxpppp/dsh-search-mcp](https://github.com/gxpppp/dsh-search-mcp) | Search MCP providers in place of built-in web search | `dsh plugin --profile web add link:<repo>` | MIT; queries and keys reach external providers |
| [yangzhe1003/dsh-web-search-firecrawl](https://github.com/yangzhe1003/dsh-web-search-firecrawl) | Firecrawl search provider | `dsh plugin --profile web add @yangzhe1003/dsh-web-search-firecrawl` | MIT; requires `FIRECRAWL_API_KEY` |
| [titanwings/dsh-better-browser](https://github.com/titanwings/dsh-better-browser) | Kimi WebBridge for a signed-in browser | `dsh plugin --profile web add github:titanwings/dsh-better-browser#v0.3.5` | BSD-3-Clause; exposes cookies, pages, upload and browser actions |
| [titanwings/dsh-automation](https://github.com/titanwings/dsh-automation) | Schedule coding tasks in fresh Agent sessions | `pnpm dsh plugin --profile web add /absolute/path/to/dsh-automation` | MIT; restrict workspace and permissions |
| [Scorp1o117/dsh-tdai-memory](https://github.com/Scorp1o117/dsh-tdai-memory) | TencentDB Agent Memory L0–L3 recall | Mount in `cordis.patch.yml`; see [README](https://github.com/Scorp1o117/dsh-tdai-memory) | MIT; needs LLM, embedding and storage endpoints |
| [TecFancy/dsh-deeptutor](https://github.com/TecFancy/dsh-deeptutor) | DeepTutor learning, knowledge-base and note bridge | `dsh plugin --profile web add dsh-deeptutor`, then configure bundles | MIT; depends on a DeepTutor service |
| [Scorp1o117/dsh-soul-md](https://github.com/Scorp1o117/dsh-soul-md) | Inject and hot-reload a `soul.md` persona | Mount in `cordis.patch.yml` | MIT; affects global system prompt |
| [codeAnqiang-ma/dsh-superpowers](https://github.com/codeAnqiang-ma/dsh-superpowers) | Superpowers methodology skills and bootstrap | `dsh plugin --profile web add dsh-superpowers` | MIT; injects a bootstrap prompt per request |
| [Xilin3/dsh-prompt-persona](https://github.com/Xilin3/dsh-prompt-persona) | Edit deployment persona in Settings | `dsh plugin --profile web add github:xilin3/dsh-prompt-persona` and add to profile bundles | MIT; persists and replaces system prompt content |
| [SiYue-ZO/dsh-translator](https://github.com/SiYue-ZO/dsh-translator) | Focused translation workspace and session workflow | `dsh plugin --profile web add github:SiYue-ZO/dsh-translator` | MIT; source text is sent to the selected model |
| [YYTbit/dsh-plugin-meta-memory](https://github.com/YYTbit/dsh-plugin-meta-memory) | Persistent local memory, indexing, recall, and prompt injection | `dsh plugin --profile <profile> add dsh-plugin-meta-memory` | MIT; may persist sensitive content |
| [yyh-001/dsh-companion](https://github.com/yyh-001/dsh-companion) | Persona, persistent memory, and optional QQ channel | `pnpm add github:yyh-001/dsh-companion` plus agent-preset configuration | MIT; may write memory and send/receive QQ content |
| [yyh-001/dsh-expression](https://github.com/yyh-001/dsh-expression) | Meme search and QQ image sending | `pnpm add github:yyh-001/dsh-expression` plus agent-preset configuration | MIT; sends actual images through QQ |
| [humblebanana/dsh-record-replay](https://github.com/humblebanana/dsh-record-replay) | Turn macOS demonstrations into agent skills | Build a tarball, then `dsh plugin --profile web add ./dsh-record-replay-*.tgz` | MIT; accessibility/input-monitoring data can be sensitive |

### Communication, infrastructure, and observability

| Extension | Capability | Installation / source | License and caution |
| --- | --- | --- | --- |
| [imetn/dsh-lark-bridge](https://github.com/imetn/dsh-lark-bridge) | Bidirectional Lark/Feishu controller | `dsh plugin --profile lark add github:imetn/dsh-lark-bridge` | MIT; constrain IM access boundary |
| [Roy-oss1/dsh-lark](https://github.com/Roy-oss1/dsh-lark) | Lark/Feishu bot channel, replies and approval cards | `dsh plugin --profile web add <repo-path-or-git-url>` | BSD-3-Clause; IM can trigger shell-capable agents |
| [UynajGI/dsh-ssh](https://github.com/UynajGI/dsh-ssh) | SSH, SFTP, remote subprocesses and PTY | Install `dsh-ssh`, then mount in Cordis configuration | MIT; protect keys and enforce host-key checks |
| [jumpserver-east/jumpserver-dsh](https://github.com/jumpserver-east/jumpserver-dsh) | Audited remote asset operations through JumpServer/KoKo | `dsh plugin --profile web add github:jumpserver-east/jumpserver-dsh` | MIT; high-privilege remote execution |
| [TwotwoPiggy/dsh-balance](https://github.com/TwotwoPiggy/dsh-balance) | DeepSeek balance and session-cost view | `dsh plugin --profile web add dsh-balance` | License not found; reads API key to query balance |
| [rainforest888/dsh-plugins-raincode](https://github.com/rainforest888/dsh-plugins-raincode) | Raincode model gateway, cache/retry, and `/skills` browsing | `npm i dsh-plugins-raincode`, then register in `cordis.yml` | MIT; prompts/tools flow through the gateway |
| [bobleer/dsh-acp-for-bitfun](https://github.com/bobleer/dsh-acp-for-bitfun) | BitFun subagent orchestration through ACP | `dsh plugin --profile web add dsh-acp-for-bitfun` | MIT; manages external processes and permissions |

### Computer use, diagnostics, and specialist tools

| Extension | Capability | Installation / source | License and caution |
| --- | --- | --- | --- |
| [Anionex/dsh-computer-use](https://github.com/Anionex/dsh-computer-use) | macOS accessibility control, screenshots and computer-use tools | Clone `dsh-external/dsh-computer-use`; load with `dsh plugin --profile web add <path>` | MIT; controls keyboard/mouse and reads screen data |
| [CanglongCl/dsh-web-review](https://github.com/CanglongCl/dsh-web-review) | Web preview, element control and review evidence | `dsh plugin --profile web add @canglongcl/dsh-web-review` | License not found; defend against web prompt injection |
| [csyangwen/dsh-memory-evolve](https://github.com/csyangwen/dsh-memory-evolve) | Memory, skills, todos and external-agent orchestration | Only a client manifest is currently documented; see [README](https://github.com/csyangwen/dsh-memory-evolve) | MIT; file access, prompt injection and external CLIs should start disabled |
| [omdsh-dev/dsh-security-audit](https://github.com/omdsh-dev/dsh-security-audit) | Read-only local DSH config, plugin and session audit | `dsh plugin --profile web add <local-path>` | MIT; reads credential metadata and session files |
| [omdsh-dev/dsh-session-health](https://github.com/omdsh-dev/dsh-session-health) | Session directory, log and decoder diagnostics | `dsh plugin --profile web add <local-path>` | MIT; reads `$DSH_HOME/sessions` |
| [omdsh-dev/dsh-toolkit](https://github.com/omdsh-dev/dsh-toolkit) | Deterministic CSV, JSON and text tools | Build, then `dsh plugin --profile web add <local-path>` | MIT; review all aggregated local tools |
| [1na-ko/dsh-hdc-bridge](https://github.com/1na-ko/dsh-hdc-bridge) | HarmonyOS screenshot, installation, shell and verification bridge | `dsh plugin --profile <profile> add github:1na-ko/dsh-hdc-bridge` | MIT; device control, device shell, and HAP installation |

## DSH skills

A skill may be discovered through the DSH skills filesystem, but it is not the same as a native Cordis plugin.

| Project | Capability | Installation / use | License and caution |
| --- | --- | --- | --- |
| [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill) | Distil working styles from collaboration material | Clone into `.dsh/skills/dot-skill`, then run `/dot-skill` | MIT; can process personal collaboration data |
| [titanwings/ex-skill](https://github.com/titanwings/ex-skill) | Generate relationship/person-oriented skills | Clone into `.dsh/skills/ex-skill`, then run `/create-ex` | MIT; may process chat records |
| [omdsh-dev/dsh-plugin-dev](https://github.com/omdsh-dev/dsh-plugin-dev) | Plugin-development skill and validation workflow | Put `skills/dsh-plugin-dev` in the skills directory or reference it in an agent session | MIT; downstream development can touch files, network and processes |

## Official built-in capabilities (not community plugins)

The official source repository contains a large set of runtime packages. They are composable DSH components, not independent community extensions. The architecture documentation identifies model, tools, session, and agent-loop seams as replaceable layers.[2]

| Official family | Purpose | Source |
| --- | --- | --- |
| `dsh-base`, `dsh-web-app`, `dsh-headless` | Base, Web, and headless profile bundles | [official `packages/bundle`](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/bundle) |
| `llm-deepseek`, `llm-pi-ai`, `llm-retry` | Model adapters and retry behavior | [official `packages/llm`](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/llm) |
| `tool-web`, `web-search-*` | Web tooling and search providers | [official `packages/web`](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/web) |
| `skill-filesystem`, `tool-skill` | Skill discovery and invocation | [official `packages/skill`](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/skill) |
| `sandbox-*`, `fs-*`, `shell-*` | Sandbox, filesystem, and command-execution boundaries | [official `packages`](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages) |
| `session-*`, `subagent-*`, `schedule`, `workflow-*` | Sessions, subagents, scheduling, and workflow | [official `packages`](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages) |

## Watchlist and related projects

These projects are intentionally outside the native directory because the inspected repository is not itself a verified DSH-loadable extension, or the evidence is incomplete.

| Project | Position | Reason |
| --- | --- | --- |
| [whiteguo233/OpenBiliClaw](https://github.com/whiteguo233/OpenBiliClaw) | Local content-discovery agent | The main repository points to a separate `whiteguo233/dsh-openbiliclaw` client plugin that should be reviewed on its own |
| [Anionex/agent-vision-toolkit](https://github.com/Anionex/agent-vision-toolkit) | Generic vision CLI and skill | Native DSH bundle is in separate `Anionex/dsh-vision-toolkit`, awaiting independent verification |
| [paean-ai/deeptide](https://github.com/paean-ai/deeptide) | Standalone macOS coding agent | No inspected DSH bundle, patch, or profile install path |
| [yejiming/MuseAI](https://github.com/yejiming/MuseAI) | AI companion / narrative desktop application | DeepSeek API support is not evidence of a DSH plugin protocol |
| [PM-Shawn/Abu-Cowork](https://github.com/PM-Shawn/Abu-Cowork) | Local-first desktop agent | No verified DSH profile/bundle mounting evidence |
| [cofy-x/axern](https://github.com/cofy-x/axern) | Agent sandbox service | Related infrastructure, not a DSH plugin |

## Installation and safety

Start DSH with the official quick-start command:

```bash
npx @deepseek-ai/dsh web
```

Then follow the exact `dsh plugin --profile <profile> add …` command provided by a project. Before installation, pin a version or commit, inspect `package.json`, `cordis.patch.yml`, and lifecycle scripts. Do not blindly execute `curl | bash`, package-manager lifecycle hooks, or scripts requesting system credentials.

| Risk level | Examples | Minimum control |
| --- | --- | --- |
| High | Browser bridge, SSH, JumpServer, Lark/Feishu, computer use, device bridge | Isolated profile, least-privilege credentials, target allowlists, human approval, no production secrets |
| Medium | Search, vision, memory, automation, external agent gateway, balance queries | Identify where prompts/images/logs go; use per-plugin environment keys, budgets, and retention controls |
| Low to medium | UI, TUI, notifications, themes, links | Audit client injection and browser permissions; retest after DSH upgrades |

Read the detailed [English safety guide](docs/SECURITY.md) or [简体中文安全指南](docs/SECURITY.zh-CN.md).

## Contributing and maintenance

Please read the [English contribution guide](docs/CONTRIBUTING.md), [简体中文贡献指南](docs/CONTRIBUTING.zh-CN.md), and [English maintenance guide](docs/MAINTENANCE.md). New native entries must include public source, an exact install or mounting path, native DSH evidence, license information, and a permission/data-flow note.

The machine-readable catalog is [data/verified-plugins.csv](data/verified-plugins.csv). A discovery snapshot from the GitHub topic is preserved in [data/dsh-plugin-topic-candidates.csv](data/dsh-plugin-topic-candidates.csv); it is an **unreviewed candidate pool**, not a recommendation list. Curation rules are in [data/curation-criteria.yaml](data/curation-criteria.yaml). This repository is licensed under [MIT](LICENSE); each listed project retains its own license.

## References

[1] [DeepSeek Harness Developer Preview — Everything is a plugin](https://deepseek.com/harness/en/)

[2] [DeepSeek Harness Architecture — Profiles and Bundles](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)

[3] [GitHub Topic: dsh-plugin](https://github.com/topics/dsh-plugin)

[4] [Official DeepSeek Harness source repository](https://github.com/deepseek-ai/deepseek-harness)
