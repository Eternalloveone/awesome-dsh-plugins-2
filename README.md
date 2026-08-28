# awesome-dsh-plugins

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
![Catalog](https://img.shields.io/badge/catalog-2296-2563eb)
![Verified](https://img.shields.io/badge/verified-1729-16a34a)
![License](https://img.shields.io/badge/license-MIT-f59e0b)

[English](README.en.md) | **简体中文** | [🌐 网站](https://deepseekharnessplugins.com)

> 一个面向 [DeepSeek Harness（DSH）][1] 的精选插件目录。项目优先收录**可由 DSH Profile 装载**、具备可复现安装说明且源码公开的社区扩展；技能、预设与相关应用会明确区分，不把“使用 DeepSeek API”或仅贴有 `dsh-plugin` 标签的项目误当作原生插件。

DeepSeek Harness 目前处于 **Developer Preview**。官方采用 Cordis 的“Everything is a plugin”架构：Profile 组合 Bundle，外部插件通常以 `package.json` 的 `dsh` 字段及 patch 文件声明挂载方式。[1] [2] 因此，本目录中的安装方法和兼容性应在你自己的 DSH 版本上先行验证。

**快照日期：2026-08-22。** 本版主目录收录 **1729 个**经源码或安装清单核验的插件与 Skill，按 22 个能力分类组织（与配套网站 [deepseekharnessplugins.com](https://deepseekharnessplugins.com) 同构）；完整清单已拆分到 [`docs/categories/`](docs/categories/) 的 22 个分类页面。同时提供 **全量聚合目录 [`CATALOG.md`](CATALOG.md)（2296 个仓库）**，合并 GitHub 搜索与多个社区目录去重后得到。**聚合 ≠ 可装载、可兼容、可安全运行**；只有本目录核验子集进入主目录，证据见 [data/verified-plugins.csv](data/verified-plugins.csv) 与 [data/audit-results.csv](data/audit-results.csv)。[3]

| 导航 | 内容 |
| --- | --- |
| [全量聚合目录](#全量聚合目录) | **2296 个** DSH 相关仓库的完整聚合（含未审核候选）；[审计日志](data/audit-results.csv) |
| [已核验插件目录](#已核验插件目录) | 按 22 个能力分类的已核验可装载扩展（与[网站](https://deepseekharnessplugins.com)同构） |
| [界面与体验](#界面与体验) · [会话与消息](#会话与消息) · [其他](#其他) · [桌面与应用](#桌面与应用) · [MCP 与协议](#mcp-与协议) · [插件工具](#插件工具) · [Web 界面与前端](#web-界面与前端) · [主题与皮肤](#主题与皮肤) · [安全与鉴权](#安全与鉴权) · [聊天与 IM](#聊天与-im) · [命令行与终端](#命令行与终端) · [语音](#语音) · [清单与资源](#清单与资源) · [用量与计费](#用量与计费) · [Agent、自动化与工作流](#agent自动化与工作流) · [集成与分享](#集成与分享) · [开发者工具](#开发者工具) · [知识与研究](#知识与研究) · [设计、媒体与视觉](#设计媒体与视觉) · [网页与浏览器](#网页与浏览器) · [生态与资源](#生态与资源) · [纯属好玩](#纯属好玩) | 22 个分类锚点 |
| [官方内置能力](#官方内置能力不是社区插件) | 随 DSH 源码发行的官方运行时构件 |
| [相关项目与观察名单](#相关项目与观察名单不计入主目录) | 相关但并非已核验原生插件的项目 |
| [安装与安全](#安装与安全) | 安装惯例、权限提示与审计建议 |
| [贡献规则](#贡献与维护) | 新项目的提交格式与审核门槛 |

## 全量聚合目录

[`CATALOG.md`](CATALOG.md) 是自动生成的**全量聚合目录**：它把 GitHub `dsh-plugin` / `deepseek-harness` 话题、名称搜索、[`dsh-plugin` 主题页候选快照](data/dsh-plugin-topic-candidates.csv)以及多个社区目录（[bruc3van/awesome-dsh-plugin](https://github.com/bruc3van/awesome-dsh-plugin)、[Alex-Yanggg/awesome-DSH-plugin](https://github.com/Alex-Yanggg/awesome-DSH-plugin)、[awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin)、[AdamPlatin123/awesome-dsh-plugins](https://github.com/AdamPlatin123/awesome-dsh-plugins)）中发现的**全部**仓库合并去重。机器可读版本是 [`data/repositories.csv`](data/repositories.csv)。

- 聚合池是**发现清单**，不是推荐或兼容性列表；只有 `✅` 已核验子集进入下方主目录。
- 用 [scripts/aggregate.py](scripts/aggregate.py) 重新拉取并重建 `CATALOG.md` 与 `data/repositories.csv`（需要 `gh` 登录）。

## 已核验插件目录



下列条目已核验至少一个原生特征：可复现的 `dsh plugin` 安装命令、`dsh.bundle` / `cordis.patch.yml` 声明，或 DSH/Cordis 可挂载的 `apply` 入口。**“已核验”不代表作者、代码质量或安全性背书。**

> 每个分类的**完整清单**已拆到 [`docs/categories/`](docs/categories/) 下的独立页面，顶部均附有对应网站分类的链接；下方仅展示每类最近活跃的若干条目。



| 导航 | 内容 |
| --- | --- |
| [全量聚合目录](#全量聚合目录) | **2296 个** DSH 相关仓库的完整聚合（含未审核候选）；[审计日志](data/audit-results.csv) |
| 分类目录（完整清单） | [界面与体验](docs/categories/ui-experience.md) · [会话与消息](docs/categories/sessions-messages.md) · [其他](docs/categories/utilities.md) · [桌面与应用](docs/categories/desktop.md) · [MCP 与协议](docs/categories/mcp.md) · [插件工具](docs/categories/plugin-tools.md) · [Web 界面与前端](docs/categories/web-ui.md) · [主题与皮肤](docs/categories/theme.md) · [安全与鉴权](docs/categories/security.md) · [聊天与 IM](docs/categories/chat-im.md) · [命令行与终端](docs/categories/cli.md) · [语音](docs/categories/voice.md) · [清单与资源](docs/categories/lists.md) · [用量与计费](docs/categories/billing.md) · [Agent、自动化与工作流](docs/categories/agents-workflows.md) · [集成与分享](docs/categories/integrations-sharing.md) · [开发者工具](docs/categories/developer-tools.md) · [知识与研究](docs/categories/knowledge-research.md) · [设计、媒体与视觉](docs/categories/media-vision.md) · [网页与浏览器](docs/categories/web-browser.md) · [生态与资源](docs/categories/ecosystem-resources.md) · [纯属好玩](docs/categories/fun.md) |
| [官方内置能力](#官方内置能力不是社区插件) | 随 DSH 源码发行的官方运行时构件 |
| [相关项目与观察名单](#相关项目与观察名单不计入主目录) | 相关但并非已核验原生插件的项目 |
| [安装与安全](#安装与安全) | 安装惯例、权限提示与审计建议 |
| [贡献与维护](#贡献与维护) | 新项目的提交格式与审核门槛 |



### 界面与体验

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [10086ggqq/dsh_theme_terraria](https://github.com/10086ggqq/dsh_theme_terraria) | Full Terraria-themed web UI: real chat with streaming, tool-approval panels, model switching, 4 agent presets, desk pets. | `dsh plugin --profile web add dsh-theme-terraria (or github:10086ggqq/dsh_theme_terraria)` | MIT；Fan-art skin using Terraria trademark — unaffiliated; pins @deepseek-ai/dsh-web-app rc.5. |
| [DIAG5/dsh-better-input](https://github.com/DIAG5/dsh-better-input) | Adds voice dictation, AI text polishing, one-click prompt optimization, multi-format file input, OCR of scanned PDF/PPT. | `dsh plugin --profile web add dsh-better-input` | MIT；OCR sends rendered document pages to a configured vision model; browser mic requires Chrome/Edge; requires DSH >= 0.1.0-rc.8. |
| [dsh-blue/blue](https://github.com/dsh-blue/blue) | Interactive terminal UI for DeepSeek Harness: streaming transcripts, tool cards, dock panes, status bars, slash commands, themes. | `npm i -g @deepseek-ai/dsh; dsh plugin --profile blue add @dsh-blue/blue@rc; dsh --profile blue` | MIT；Preview 0.1.0-rc.8 under @rc dist-tag; requires Node ^22.19\|\|>=24, pnpm 11. |
| [FeatherHunter/dsh-mattpocock-skills-deck](https://github.com/FeatherHunter/dsh-mattpocock-skills-deck) | Adds a task-system deck to DSH: wayfinder map, ticket/issue tracking, progress ring, injects Matt Pocock skills. | `dsh plugin --profile web add dsh-mattpocock-skills-deck` | MIT；Third-party unofficial wrapper around mattpocock/skills; DSH update lag noted by author. |
| [kenz1117/dsh-ui-usage-billing](https://github.com/kenz1117/dsh-ui-usage-billing) | Real-usage cost dashboard (overview/trend/detail/stats), peak-off-peak billing engine, 73-model catalog, CSV/JSON export. | `Add to host cordis.patch.yml: insert {id: ui-usage-billing, name: '@kenz1117/dsh-ui-usage-billing'}` | MIT；Costs are catalog-price estimates, not official invoices; relay quota schemas undocumented. |
| [lamost423/dsh-maze](https://github.com/lamost423/dsh-maze) | Visualizes DSH agent sessions as a maze timeline: main path, failed branches, data tracks, failure-recovery analysis, replay. | `npm install --global @deepseek-ai/dsh@0.1.0-rc.8 && dsh plugin --profile web add dsh-maze && dsh web` | MIT；None. Self-contained UI plugin; client-side parsing only. |
| [Lzh3070/dsh-file-review-tab](https://github.com/Lzh3070/dsh-file-review-tab) | Sidebar tab + chat-row review of agent file edits: per-turn grouped line-level diffs, per-file/per-turn undo & reapply. | `dsh plugin --profile web add dsh-file-review-tab` | MIT；Depends on external plugin dsh-better-sidebar; ported from left0ver/dsh-file-review (MIT credited). |
| [plolpl789/dsh-raw-html](https://github.com/plolpl789/dsh-raw-html) | Toggles rendering of model HTML into real UI in the DSH web GUI; KaTeX/Mermaid/card rendering, vcp-fast caching. | `dsh plugin --profile web add <plugin-path> (one-click installer install-v6.cjs)` | MIT；Install relies on patching the DSH dist bundle; verify against your DSH version. |
| [WizisCool/dsh-ears](https://github.com/WizisCool/dsh-ears) | Voice input for DSH web UI with Web Speech, local GPU Whisper, Groq, Aliyun Bailian, Tencent Cloud and OpenAI-compatible ASR backends, plus automatic polishing. | `dsh plugin --profile web add dsh-ears` | MIT |
| [wlj521/dsh-ui-tweaks](https://github.com/wlj521/dsh-ui-tweaks) | Adjust DSH UI via settings panel; GitBar branch/diff ops, real PTY terminal, IDE project launcher, archive restore/delete, MCP server management. | `npx -y @deepseek-ai/dsh plugin --profile web add dsh-ui-tweaks (or github:wlj521/dsh-ui-tweaks)` | MIT；Contains browser PTY terminal, git push, archived-log deletion, cordis.patch.yml rewriting — review source before install. |

> 该分类共 **224** 个已核验条目，[查看完整清单 →](docs/categories/ui-experience.md)

### 会话与消息

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [AgentDebugX/AgentDebugX](https://github.com/AgentDebugX/AgentDebugX) | Captures and diagnoses DSH session trajectories via /agentdebug commands and model tools; local FastAPI dashboard. | `python -m pip install "agentdebugx[ui]>=0.3.1,<0.4" && dsh plugin --profile web add dsh-agentdebugx && dsh web` | MIT；Targets DSH 0.1.1-rc.2; dashboard must not be exposed without auth/TLS. |
| [corrinehu/dsh-workbuddy-connect](https://github.com/corrinehu/dsh-workbuddy-connect) | Adds WorkBuddy models to the DSH model picker with zero configuration across Web/Desktop/TUI; settings card shows account info and remaining credits. | `dsh plugin --profile web add dsh-workbuddy-connect` | MIT；Depends on non-official WorkBuddy client interface; may break on app updates; README restricts to personal research use. |
| [DingTalk-Real-AI/dsh-dingtalk](https://github.com/DingTalk-Real-AI/dsh-dingtalk) | Chat bot bridging dsh web to DingTalk private/group chats: streaming AI cards, session persistence, model selection, workspace switch, access policies. | `dsh plugin --profile web add @dingtalk-real-ai/dsh-dingtalk@latest && dsh web` | MIT；Only dsh web profile supported; local-only uptime; Windows experimental; requires Node ^22.19 or >=24. |
| [MichengAI/dsh-archive-manager](https://github.com/MichengAI/dsh-archive-manager) | Archive sessions from sidebar, browse/manage in Settings->Archived, restore single/all, permanent delete with double-confirm. | `dsh plugin --profile web add @michengai/dsh-archive-manager@latest` | Apache-2.0；Not an official DeepSeek product; verify plugin source before granting delete permissions. |
| [Ultronen/dsh-archived-chats](https://github.com/Ultronen/dsh-archived-chats) | Web-plugin archive management UI: workspace-grouped browsing, full-text search, native preview, History with restore-as-copy, ZIP export/import, Recycle Bin, retention policies. | `dsh plugin --profile web add dsh-archived-chats@latest` | MIT；Reads archived conversation content (may include sensitive chat text); data persists under $DSH_HOME after uninstall (by design). |
| [AgentConnect/dsh-awiki](https://github.com/AgentConnect/dsh-awiki) | Web-profile DSH bundle adding AWiki identity (OTP login/recovery), IM (DMs, groups, attachments), AI summaries, 5 mail + 5 message agent tools. | `dsh plugin --profile web add @awiki/dsh-plugin@latest` | MIT；Third-party org (not DeepSeek); depends on hosted awiki.ai services; v1 lacks E2E encryption. |
| [boomzikazita/dsh-cybernetics](https://github.com/boomzikazita/dsh-cybernetics) | Agent 工具循环的控制论运行时：前馈拦截不可逆操作、EMA 失败率滤波、fast/deep/conservative 档位自适应稳定阀、发散/振荡检测、能控性自检 | `dsh plugin --profile web add github:boomzikazita/dsh-cybernetics` | MIT；拦截并记录本地工具调用、写本地 NDJSON 状态日志；不访问网络、无需 API Key；会 block 命中规则的工具调用 |
| [yjh051108/dsh-router-standard](https://github.com/yjh051108/dsh-router-standard) | Task-aware reasoning-mode router for DSH: classifies first real user message (build/fix/ambiguous), injects matching persona + band-gated tool surface, progressive tool disclosure, dev_router_status/mode/subagent commands | `Copy-Item -Recurse .\preset\router-standard $HOME\.dsh\.agent-presets\router-standard; npm package dsh-router-standard` | MIT；Research artifact; author formally retracted dual-attractor theory sections; presets are experimental and rewrite first-turn prompts |
| [SiriLee/dsh-rewind](https://github.com/SiriLee/dsh-rewind) | Claude Code-style in-place /rewind for DSH web profile: cut conversation back to any earlier user message, optional workspace-file restore from disk-persisted before-backups, per-message button + candidate picker UI | `dsh plugin --profile web add dsh-rewind-plugin (git installs need allowBuilds in profile's pnpm-workspace.yaml)` | MIT；npm name is dsh-rewind-plugin (dsh-rewind taken); known <=v0.2.4 marker-turn bug can corrupt client replay; ships dsh-rewind-repair |
| [tinqiao-oss/engramory](https://github.com/tinqiao-oss/engramory) | 便携记忆协议：常驻规则 + 记忆纪律（SKILL.md），纯 markdown 笔记单一库跨宿主共享；原生插件 dsh-engramory 用 ctx.tools.guard() 把常驻索引的体积上限做成单调拒绝（写前 deny 而非提醒），并经 ctx.inject(['skills']) 在运行时注册 skill，不依赖文件落到五个 skill 根之一 | `dsh plugin --profile <name> add dsh-engramory（npm 包 dsh-engramory；亦可 python tools/engramory_init.py dsh --install-skill 只装 skill + AGENTS.md 块）` | MIT；dsh 仍是开发者预览、插件 API 可能变化；0.2.0 装上永不激活（issue #8），须 0.2.1 及以上；记忆以明文 markdown 存本地 .engramory-memory/，位于项目仓内时应加入 git 忽略；插件本身无 exec/eval/网络请求/环境变量读取 |

> 该分类共 **110** 个已核验条目，[查看完整清单 →](docs/categories/sessions-messages.md)

### 其他

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [TencentCloud/tencentcloud-agentobs-sdk-dsh](https://github.com/TencentCloud/tencentcloud-agentobs-sdk-dsh) | Streams DSH GenAI traces to Tencent Cloud CLS log service with 5-layer span hierarchy, configurable batching/retry, content capture toggle. | `dsh plugin --profile web\|headless\|harness add tencentcloud-agentobs-sdk-dsh` | Apache-2.0；Content capture enabled by default; disable via captureContent:false; requires DSH >=0.1.0-rc.6 <0.2.0. |
| [lizhiyao/oh-my-knowledge](https://github.com/lizhiyao/oh-my-knowledge) | Runs controlled A/B evals, artifact health checks, evidence-gated promote/evolve/rollback version lifecycle, observability traces. | `dsh plugin --profile web add oh-my-knowledge && dsh --profile web` | MIT；Primarily a standalone npm CLI; DSH integration is one of several executors. |
| [ZSeven-W/dsh-harbor](https://github.com/ZSeven-W/dsh-harbor) | Scans installed third-party DSH bundles and reports 13 capabilities with file:line evidence, conflict detection, version drift tracking. | `dsh plugin --profile web add @zseven-w/dsh-harbor@next && dsh web` | MIT；Pre-release 0.1.0-rc.2 (install via @next tag); static analysis yields false pos/neg. |
| [Yan-Zero/dsh-std](https://github.com/Yan-Zero/dsh-std) | Protocol-definition meta-layer and DSH adapter loading standard dsh-plugin.json facets into DSH. | `dsh plugin --profile web add @dsh-std/adapter-dsh` | MIT；Explicitly early drafts (0.1.0-rc); package surface and rc protocol alignment still churning. |
| [lninghaha/dsh-coding-subscription-oauth](https://github.com/lninghaha/dsh-coding-subscription-oauth) | 为 DSH 提供编码订阅 OAuth 登录的模型路由插件，一个插件覆盖五个 Provider：SuperGrok/Grok Build、ChatGPT Plus/Pro Codex、Kimi Code、Claude Code 及 Google Antigravity。含本地 OAuth/device-code 登录、动态模型目录、凭据 0600 原子存储、可选本地 API 网关、Codex 搜索/用量/图像等可选能力 | `dsh plugin --profile web add dsh-coding-subscription-oauth@0.6.0（可选加 dsh plugin --profile web add dsh-agy@0.1.2），随后重启 DSH Web 进程；要求 DeepSeek Harness 0.1.0-rc.6+ 与 Node 22.19+` | Apache-2.0；合规性：通过第三方 harness 使用厂商订阅账号处于各厂商条款灰色地带，项目声明仅限自有账号、不支持批量/配额转售/绕过付费墙；商业使用建议官方 API-key 渠道 |
| [zexadev/dsh-tether](https://github.com/zexadev/dsh-tether) | 通过 iroh P2P 打洞将开发机上的 DSH Web 界面端到端带到手机（Android 已签 APK / iOS 未签 beta IPA），支持多机配对、审批通知、跨网直连，无需公网 IP 或中转服务器；附 Rust sidecar 与 Tauri 手机应用 | 机器端：`dsh plugin --profile web add dsh-plugin-tether`；或源码：`cargo build --release -p tether-host && dsh plugin --profile web add .`；手机端从 GitHub Release 安装 APK | MIT；DSH 处于 developer preview，仅对 dsh 0.1.0-rc.7/rc.8 验证；iOS 为 beta（未真机运行、需自签、7 天过期）；README 建议不要在运行不可信代码的机器上启用本插件 |
| [ZJU-LLMs/OpenStory](https://github.com/ZJU-LLMs/OpenStory) | Multi-agent story-world simulation registered as a DSH tool. | `npx -y @deepseek-ai/dsh plugin --profile web add dsh-openstory@0.2.0` | MIT；Heavy install (needs Redis + Python 3.11-3.13 + full source checkout). Freshly published; may trip DSH ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION supply-chain guard - wait and retry, do not disable the policy. |
| [zuorn/Tydora](https://github.com/zuorn/Tydora) | Tauri v2 桌面 Markdown 编辑器（WYSIWYG/双向链接/思维导图/无限画布），仓库声明 dsh.bundle 补丁挂载最小 DSH 插件骨架 | see README（桌面应用，Release 安装）; DSH 装载：dsh plugin add 时应用 package.json dsh.bundle → cordis.patch.yml 补丁 | Apache-2.0；DSH 入口 dsh/index.ts 为最小可加载骨架，当前不注册任何能力；仓库主体是独立的桌面 Markdown 编辑器 |
| [Thanksgiver233/comm-protocol-hub](https://github.com/Thanksgiver233/comm-protocol-hub) | 3GPP 通信协议知识库插件：内置 70+ 条 Rel-15~18 协议结构化索引（TN/NTN/全息/近远场/混合/安全等 8 类），通过 3 个 DSH 工具（comm_protocol_query / comm_protocol_browse / comm_protocol_detail）供大模型按需查询，并附带 web 交互面板与对话内联卡片，数据本地内嵌、无需联网 | `npx -p @deepseek-ai/dsh dsh plugin --profile web add github:Thanksgiver233/comm-protocol-hub（本地开发可用 add <path-to-repo>）` | MIT；仓库仅单次提交 'Add files via upload'（无开发历史）；package.json 的 repository.url 仍是 example.com 占位符；lib/ 构建产物未随仓库提供，需自行 pnpm build |
| [030611/dsh-context-provenance](https://github.com/030611/dsh-context-provenance) | Observe-only plugin tagging adjacent request evidence as Observed/Estimated/Unavailable without altering output. | `` | N/A |

> 该分类共 **71** 个已核验条目，[查看完整清单 →](docs/categories/utilities.md)

### 桌面与应用

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [slywalker2006/dsh-passwords](https://github.com/slywalker2006/dsh-passwords) | 登录网关（密码门）：首次配置、多用户（主/子用户）、防爆破锁定、审计日志、自动 HTTPS；让 DSH 可安全远程访问 | `bash install.sh（一键安装；Windows: install.bat；dsh 侧挂载 cordis 补丁）` | GPL-3.0-only；处理特权凭证属高风险；公网部署需放行 80/443 并妥善保管首次配置密钥；经密码门登录的远程浏览器可编辑 dsh 设置 |
| [ARFCON/dsh-hotplug-hub](https://github.com/ARFCON/dsh-hotplug-hub) | DSH 热插拔插件中枢/桌面管理器（C# WinForms + WebView2）：插件与 Skill 管理、MCP（STDIO/streamable-http）管理、全局记忆中枢（~/.dsh/memory-hub）、hotpack 插件组合（assembly）、AI 对话式装配 | `从 Releases 下载安装包 DSH-Hotplug-Hub-win-x64-setup-v0.9.8.exe --silent，安装后自动将内置插件装入 ~/.dsh/profiles/web；或 node launcher/index.js assemble example` | MIT；仓库仅创建 3 天（2026-08-19），版本处于 pre-release；插件打包用自定义 hotpack 格式而非标准 cordis.patch.yml；桌面端以 Windows 为主 |
| [RAFOLIE/dsh-desktop-windowos](https://github.com/RAFOLIE/dsh-desktop-windowos) | DSH Windows desktop shell plugin: installs/auto-updates a Tauri v2 tray app (single portable exe) launching dsh web with embedded webchat UI, desktop shortcuts, desktop_launch tool, task-done notifications, diagnostics export | `dsh plugin --profile web add dsh-desktop-plugin (or drop the exe beside node_modules/.bin/dsh.cmd)` | MIT；Project is primarily a desktop shell; only the companion dsh-desktop-plugin npm package is the DSH-loadable artifact; unsigned exe triggers SmartScreen |
| [saya-ch/dsh-mobile](https://github.com/saya-ch/dsh-mobile) | Exposes a computer's DeepSeek Harness over a secure LAN to a phone browser or Android App; provides a mobile layout, device pairing (QR/link/key), /mobile conversational customization of the phone UI, and a local extension host for phone-triggered computer capabilities (e.g. live CPU/RAM/disk monitor). | `dsh plugin --profile web add dsh-mobile@alpha` | Apache-2.0；LAN-only; treat paired devices as fully trusted since they can control computer DSH; do not forward the gateway to the public internet; lost phone should have its device trust revoked on the desktop; extension host.mjs runs with local user privileges. |
| [JUANWANG-BUAA/dsh-full-remote](https://github.com/JUANWANG-BUAA/dsh-full-remote) | Token-gated reverse proxy keeps DSH web usable over public tunnels/other devices: settings, credentials and file access stay working; per-device sessions. | `dsh plugin --profile web add dsh-full-remote` | MIT；公网反向代理暴露设置/凭据/文件访问，务必启用 token 鉴权并限制暴露面。 |
| [Asaiuta/dsh-session-hub](https://github.com/Asaiuta/dsh-session-hub) | Session Hub:把多台远端 dsh web 部署的会话聚合进本机官方 Web UI 并原生操控——会话历史、逐 token 实时流、审批/提问卡片均由官方组件渲染,插件只做 /api 数据桥接;设置→插件→Session Hub 管理服务器(增删/探活/远端新建会话/模型配置同步);无 SSH、无屏幕抓取、远端零配置零插件。 | `dsh plugin --profile web add dsh-session-hub (npm dist; dev: git clone + dsh plugin --profile web add file:/path/to/dsh-session-hub; remove leaves registry file $DSH_HOME/plugins/dsh-session-hub.json)` | MIT；Server registry is plaintext JSON containing remote baseUrls; only point it at trusted DSH instances. |
| [beex-labs/dsh-desktop-plugin](https://github.com/beex-labs/dsh-desktop-plugin) | Desktop-launcher plugin: mounts a desktop-launcher host row in dsh web; with autoLaunch it spawns the packaged DeepSeekHarness.Desktop.exe (WPF/WebView2 shell, .NET 8 self-contained) once the web server is ready, handing it DSH_WEB_PORT; never downloads anything and never spawns a second server. | cd packages/dsh-desktop && pnpm build (tsc) && pnpm pack, then `dsh plugin --profile web add ./dsh-desktop` (or npm-publish and `dsh plugin --profile web add dsh-desktop`); optionally enable `- id: desktop-launcher` + config { autoLaunch: true } in the profile's cordis.patch.yml | MIT；Repo root has no LICENSE file but the published npm package declares MIT; shell exe is Windows-only. |
| [bluecobaltum/dsh-lan-proxy](https://github.com/bluecobaltum/dsh-lan-proxy) | LAN access for the DSH Web UI: makes the local `dsh web` control plane reachable from other devices on the network; ships an explicit security warning and recommends pairing with an auth layer. | Put the repo dir where DSH can resolve it (e.g. plugins/dsh-lan-proxy under the checkout) and add `- id: dsh-lan-proxy` with name pointing at src/index.ts to ~/.dsh/profiles/web/cordis.patch.yml (or `dsh plugin add dsh-lan-proxy` once published to npm) | 未发现；Do not enable on untrusted networks without a reverse-proxy auth layer (e.g. deepseek-harness-auth). |
| [ch1bug/dsh-wsl-bridge](https://github.com/ch1bug/dsh-wsl-bridge) | WSL 内 DSH agent 的 Windows 访问工具集：win_ls / win_read / win_write / win_run / win_open / win_path / win_drives，操作 Windows 文件系统与进程（exec）。 | `dsh plugin --profile web add /path/to/dsh-wsl-bridge（或 github:ch1bug/dsh-wsl-bridge）；重启 dsh web 后工具自动挂载` | MIT；授予前确认 Windows 侧命令执行与文件访问边界。 |
| [chenw2759-wq/dsh-easyssh](https://github.com/chenw2759-wq/dsh-easyssh) | DSH Web GUI 内 SSH 远程工作区：右上角（session log 左侧）配置 SSH 主机（密码/密钥，复用 ~/.dsh/dsh-ssh.json），左侧远程文件树面板（完整 @deepseek-ai/dsh-fs 实现：路径/版本/原子写/CRLF/规范路径），远程子进程（@deepseek-ai/dsh-subprocess：exec + PTY，输出溢出转储本地）。 | `dsh plugin --profile web add file:<repo>/packages/dsh-ssh && dsh plugin --profile web add file:<repo>/packages/dsh-easyssh，然后在 <profile>/cordis.patch.yml 写入接缝切换补丁（禁用本地 fs/subprocess，插入 name: 'dsh-easyssh/fs' 与 'dsh-easyssh/subprocess' 门面行）并重启；回滚 = 恢复 cordis.patch.yml 为 []` | BSD-3-Clause；远程执行能力高风险，授予前确认边界；移植代码版权归属 UynajGI/dsh-ssh 见 NOTICE。 |

> 该分类共 **47** 个已核验条目，[查看完整清单 →](docs/categories/desktop.md)

### MCP 与协议

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [BeforeWave/dsh-with-chatgpt](https://github.com/BeforeWave/dsh-with-chatgpt) | Lets ChatGPT inspect local repos, trace symbols, edit files, delegate build/test loops to native DSH sessions. | `dsh plugin --profile web add @beforewave/dsh-with-chatgpt && dsh web` | MIT；Repo is a README-only documentation front — actual source in beforewave/agent-chatgpt-helm monorepo; grants remote session command execution. |
| [chainbase-labs/Agentkey](https://github.com/chainbase-labs/Agentkey) | Grants agents live web search, scraping, social media, crypto, finance and e-commerce data through one remote MCP server. | `npx -y skills add chainbase-labs/agentkey -g -a universal -s agentkey -y && npx -y @agentkey/cli --auth-login --only dsh` | Apache-2.0；Hosted paid service; requires auth-login to write local Bearer key; the platform proxies all data queries. |
| [FTShare-Lab/dsh_kline](https://github.com/FTShare-Lab/dsh_kline) | 面向 DeepSeek Harness 的交互式 K 线/金融数据插件：MCP 工具（analyze_kline、fetch_candles、calc_metrics、health）提供港股/美股/A 股多市场行情，技术指标（MA/MACD/KDJ/RSI/BOLL/ATR/VWAP）、支撑压力位、区间统计、新闻与基本面，并在原生侧栏以交互图表展示 | `git clone && cd dsh_kline && pnpm install && bash ./scripts/bootstrap.sh && pnpm dsh:web（等价于 dsh plugin --profile web add "link:$PROJECT_ROOT" && dsh --profile web --patch config/dsh-kline.patch.yml）` | MIT；package.json 标记 private:true，未发布到 npm，只能源码构建挂载；行情数据依赖 FTShare 外部数据源，README 注明可能延迟且非投资建议；仓库创建于 2026-08-14，属于新项目 |
| [volcengine/ark-cli](https://github.com/volcengine/ark-cli) | 向 DSH 提供火山方舟能力：ark-plan-api 在 DSH 原生模型选择器注册 Agent Plan/Coding Plan/后付费模型路由（Anthropic Messages 协议），ark-managed-agents 注入 Managed Agents 设置页并通过 stdio MCP 工具派发云端 Managed Agents 长任务 | `dsh plugin --profile web add ./dsh-plugins/ark-plan-api、dsh plugin --profile web add ./dsh-plugins/ark-managed-agents；正式安装从 GitHub Releases 下载预构建 tarball` | Apache-2.0；提交说明明确'插件 JS 源码留在内部仓库，本仓库仅存放元数据，二进制以 GitHub Release tgz 分发'——社区无法在公开仓库直接审计/复现插件构建；需要火山方舟账号与 API Key；插件 v0.1.0 为 2026-08-21 新发布 |
| [mrpulor-gh/nuphus-mcp](https://github.com/mrpulor-gh/nuphus-mcp) | 38 MCP tools (15 desktop + 23 browser): screenshots, window control, mouse/keyboard, clipboard, local OCR, BYOK vision, Chrome CDP automation incl. cookies/exec/snapshot. | `npm install -g @nuphus/nuphus-mcp  # prebuilt binary; or cargo build --release -p nuphus-mcp` | MIT；High risk: can take physical control of the machine and access browser cookies/clipboard. Run only in a trusted desktop session with --confirm-write. BYOK vision key is transmitted to an external provider. |
| [oomol-lab/dsh-oomol](https://github.com/oomol-lab/dsh-oomol) | Bridges OOMOL Connector Actions into DSH via progressive MCP discovery — discover connected apps and run Actions without exposing provider credentials | `dsh plugin --profile web add -w dsh-oomol` | MIT；Requires an OOMOL MCP API key; connects to an external Connector endpoint (hosted or self-hosted); self-hosted can run without auth |
| [ConsoleSun/Gemini-Eyes](https://github.com/ConsoleSun/Gemini-Eyes) | Gemini 网页端 MCP 桥接插件（逆向复用登录 Cookie 提供对话/识图/生图/生视频） | `` | MIT |
| [fly233338/dsh-overleaf](https://github.com/fly233338/dsh-overleaf) | 通过 OverleafMCP 把多个 Overleaf 项目接入 DSH 的插件（浏览/读取/写回） | `` | MIT |
| [inthepond/ff-toolkit](https://github.com/inthepond/ff-toolkit) | FFmpeg 操作封装为 CLI / MCP / DSH 插件工具集（dsh-ffkit） | `` | MIT |
| [jiezeng2004-design/dsh-chatgpt-bridge](https://github.com/jiezeng2004-design/dsh-chatgpt-bridge) | ChatGPT 经 MCP 连接并监督本地 DSH 代理会话的零侵入桥接插件（15 个 MCP 工具） | `` | MIT |

> 该分类共 **20** 个已核验条目，[查看完整清单 →](docs/categories/mcp.md)

### 插件工具

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [yxxbc/dsh-balance-plugin](https://github.com/yxxbc/dsh-balance-plugin) | DeepSeek 余额监控与用量统计：CNY/USD 双余额池多账户查询、低余额告警、官方充值入口、Miyu 风格用量仪表盘、三方插件管理、query_api_quota 模型工具 | `dsh plugin --profile web add dsh-balance-plugin（github: 源）或 curl -fsSL https://raw.githubusercontent.com/yxxbc/dsh-balance-plugin/main/install.sh \| bash` | MIT；npm 上存在他人同名包 dsh-balance-plugin@0.1.0，裸包名会装错，务必用 github: 源或官方一键脚本 |
| [bowenliang123/dsh-context](https://github.com/bowenliang123/dsh-context) | Context dashboard tab + /context command showing context-window composition, per-turn history, compaction/prune events, per-message token costs | `dsh plugin --profile web add dsh-context` | Apache-2.0 |
| [crazywoola/dsh-balance](https://github.com/crazywoola/dsh-balance) | DSH Settings-page balance monitor: total/recharge/gift balance, chat-composer balance summary, available models for the API key, cached queries with manual refresh, DeepSeek peak-hour indicator, zh/en i18n | `dsh plugin --profile web add @pinkbanana/dsh-balance@latest ; dsh --profile web` | MIT；以本机保存的 DEEPSEEK_API_KEY 调用 DeepSeek API 查余额/模型，key 只在本机 Host 使用、不上浏览器 |
| [feibi-mochi/deepseek-harness-control-center](https://github.com/feibi-mochi/deepseek-harness-control-center) | Web control center for DSH: account monitoring, usage accounting, completion alerts, official recharge link, flexible layout, agent-assisted session controls (capability-gated) | `dsh plugin --profile web add deepseek-harness-wallet  (or: dsh plugin --profile web add github:feibi-mochi/deepseek-harness-control-center)` | MIT；插件会读取 DSH 本地存储并可能调用账户接口，涉及额度信息 |
| [feiyang-dev/dsh-usage-plugin](https://github.com/feiyang-dev/dsh-usage-plugin) | DSH 用量与成本追踪：每次调用的 token/缓存命中统计、峰谷计费、余额查询、日历热力图、CSV/JSON/PNG 导出，Host+Client 双半一体化包 | `dsh plugin --profile web add @feiyang666/dsh-usage-plugin（或经 DeepSeek Harness Desktop 一键安装），重启生效` | MIT；余额查询使用 DEEPSEEK_API_KEY 调官方接口；用量记录写入会话工作区 dsh-usage/usage-records.json |
| [Francis-Xavier-code/dsh-balance-plugin](https://github.com/Francis-Xavier-code/dsh-balance-plugin) | DeepSeek 余额监控与用量统计（CNY/USD 双余额池、阈值告警、充值入口、Miyu 风格用量图表、三方插件管理、query_api_quota 工具） | `dsh plugin --profile web add github:Francis-Xavier-code/dsh-balance-plugin（另在 ~/.dsh/cordis.patch.yml 追加 insert id: dsh-balance-plugin）` | MIT；自动读取 DEEPSEEK_API_KEY 并调用 api.deepseek.com 余额接口；密钥仅存于插件进程内存，不上传第三方 |
| [toby-bridges/api-relay-audit](https://github.com/toby-bridges/api-relay-audit) | Local 14-step security audit of AI API relays/LLM proxies — detects prompt injection, model substitution, tool-call rewriting, SSE anomalies, error leakage and Web3 wallet risks; emits a Markdown report via the /relay-audit slash command. | `DSH_PLUGIN_REF=v2.4.0; dsh plugin --profile web add "github:toby-bridges/api-relay-audit#${DSH_PLUGIN_REF}"  (or --profile cc-tui)` | AGPL-3.0；AGPL-3.0 copyleft; audits require trusting the target relay with your API key; Web3 profile can trigger wallet-signing probes; depends on @deepseek-ai DSH rc packages. |
| [1514100951/dsh-usage-footer](https://github.com/1514100951/dsh-usage-footer) | Floating coin button showing account balance, peak/off-peak pricing, today/session cost & token estimates; adds a '用量与费用栏' toggle in Settings; day-reset local stats in localStorage. | Link/copy packages dsh-usage-status and dsh-client-ui-usage-footer into $DSH_HOME/profiles/node_modules/ and append `name: dsh-usage-status` + `name: dsh-client-ui-usage-footer` to profiles/web/cordis.patch.yml; restart dsh web | MIT |
| [1HelloMan1/dsh-stats-dashboard](https://github.com/1HelloMan1/dsh-stats-dashboard) | Provider/model usage stats dashboard: response speed, call log, token totals, cache rate, cost estimates (built-in DeepSeek pricing), CSV export; driven by dsh-session-stats and dsh-token-meter projections. | `dsh plugin --profile web add "github:1HelloMan1/dsh-stats-dashboard#main" (npm: dsh plugin --profile web add dsh-stats-dashboard)` | MIT；GitHub API reports no LICENSE file, but package.json declares MIT. |
| [95384/DSH-user-plugin-list](https://github.com/95384/DSH-user-plugin-list) | Adds a '用户插件' tab in Settings→插件 listing non-system plugins from the loader tree (profile-local, external-path, enabled/disabled) with search/status/collapse interaction; classifies via Node resolve + realpath and excludes transitive deps. | `dsh plugin --profile web add github:95384/DSH-user-plugin-list (or local: git clone && dsh plugin --profile web add .; update: dsh plugin --profile web update user-plugin-list; remove: dsh plugin --profile web remove user-plugin-list)` | MIT |

> 该分类共 **64** 个已核验条目，[查看完整清单 →](docs/categories/plugin-tools.md)

### Web 界面与前端

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [1692775560/dsh-Mimir-Academic-research](https://github.com/1692775560/dsh-Mimir-Academic-research) | Installs into DSH as a native Cordis bundle providing an 8-view research web workbench, slash commands, agent tools, 9 research skills. | `npm install -g @deepseek-ai/dsh && dsh plugin --profile web add dsh-mimir@latest && dsh web` | MIT；Very new repo (created 2026-08-20); remote GPU/SSH features require user-supplied server credentials. |
| [ai-daming/clickvibe](https://github.com/ai-daming/clickvibe) | GitHub issue-to-merge delivery control plane: per-issue status board, one-click agent dev in worktrees, auto review, rework, dry-run. | `dsh plugin --profile web add link:/path/to/clickvibe` | MIT；v0.1.0 experimental; no LICENSE file detected on GitHub (MIT only in package.json); agents run arbitrary shell and may auto-merge. |
| [hancao97/hanai-investment-dsh](https://github.com/hancao97/hanai-investment-dsh) | A-share research workbench on DSH: market heatmap, watchlists, valuation views, four investor-method agent personas. | `git clone ... && pnpm install && pnpm run build && pnpm run profile:install -- --package . && dsh --profile hanai-investment` | MIT；README clone URL points to hanai-labs/worth-dsh (repo mismatch); requires DSH pre-release 0.1.1-rc.2; not investment advice. |
| [statem-li/dsh-webui](https://github.com/statem-li/dsh-webui) | DSH desktop-shell session enhancement suite: view tiles, tool-call aggregation, Shiki/KaTeX/Mermaid Markdown, cron task engine, multi-agent relay canvas, AI browser, memory, usage heatmap. | `dsh plugin --profile web add github:statem-li/dsh-webui` | BSD-3-Clause；Disable kernel ui-skill to avoid slash-menu conflict; browser/proxy/gateway-masquerade modules should be toggled off as needed. |
| [zhu1090093659/dsh-web](https://github.com/zhu1090093659/dsh-web) | One-command install of a full DSH web workbench: monitoring HUD, task board, SSH panel, mobile remote, vision tool, git graph, skins, plugin manager. | `dsh plugin --profile web add @linxin666/dsh-web-all@latest` | Apache-2.0；Third-party community project (not official); verify npm package availability before install; not a fork of core harness. |
| [Aisland-SJL/dsh-worktable](https://github.com/Aisland-SJL/dsh-worktable) | Sidebar project drawer, dockable split workspace (file explorer, terminal, browser), control-room dashboard. | `dsh plugin --profile web add "https://github.com/Aisland-SJL/dsh-worktable/releases/latest/download/dsh-worktable.tgz"` | MIT；Windows fully tested; macOS experimental; state stays in localStorage. |
| [lavapapa/dsh-composer-layout](https://github.com/lavapapa/dsh-composer-layout) | DSH Web Composer 布局插件：可选右侧停靠、可调整面板宽度、按会话记录布局偏好，并在空间不足时临时回到底部布局 | `dsh plugin --profile web add dsh-composer-layout@0.1.5` | MIT；仅调整界面和布局；不访问本地文件、网络、API Key、凭据或 shell；布局偏好通过 DSH 设置与会话状态保存 |
| [GDWhisper/dsh-web-startup-auth](https://github.com/GDWhisper/dsh-web-startup-auth) | Remote DSH Web startup (replaces hard-reject 0.0.0.0), login/register pages, signed session cookies, all-route API auth, password reset. | `dsh plugin --profile web add dsh-web-startup-auth@latest` | MIT；No built-in transport encryption — trusted intranet or HTTPS reverse proxy only; complete first registration before exposing. |
| [liangmianya/dsh-synapse](https://github.com/liangmianya/dsh-synapse) | DeepSeek Harness Web 可视化会话工作区：把会话/追问/分支渲染为可拖拽缩放的画布式会话地图，双向同步原生对话，按 callId 折叠工具过程，持久化画布布局 | `corepack pnpm dsh plugin --profile web add github:liangmianya/dsh-synapse && corepack pnpm dsh web（卸载：corepack pnpm dsh plugin --profile web remove dsh-synapse）` | MIT；仅支持 web profile 且要求 DSH 2026-08+ 与 Node>=22.19；两个 dsh web 实例共享同一 profile 写同一 workspaces.json 存在覆盖风险（作者建议单实例运行） |
| [omdsh-dev/stent](https://github.com/omdsh-dev/stent) | 受 MC Fabric mixin 启发的 Cordis/DSH hook 处理器：提供 stent（纯转换服务）、stent-api（兼容门面）、stent-dsh（DSH 门面/preload/配置文件引导）三件套，向 DSH web 客户端挂载钩子与 facade、发布浏览器 closure 工厂 bundle，并注入 launcher preload | `dsh plugin --profile web add @oh-my-dsh/stent-pack（@oh-my-dsh/stent-pack@0.1.1 已在 npm 发布）` | BSD-3-Clause；依赖 DSH 上游 @deepseek-ai/dsh-* rc 轨道包，registry 版本跳跃频繁（rc.3→rc.6）；仓库无独立 LICENSE 文件（仅 package.json/npm 声明 BSD-3-Clause）；版本 0.1.x 较新，建议安装前验证 npm 包完整性 |

> 该分类共 **211** 个已核验条目，[查看完整清单 →](docs/categories/web-ui.md)

### 主题与皮肤

> 暂无已核验条目。

### 安全与鉴权

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [TiantianFlow/dsh-one-gateway](https://github.com/TiantianFlow/dsh-one-gateway) | 面向 DSH Web 的私有零信任网关：仅回环监听的 HTTP/WebSocket 反向代理，经 Tailscale Serve/Cloudflare Access/Headscale TCP Serve 提供身份优先入口，支持 trusted-header、signed-jwt、gateway-credential 三种认证模式与精确 principal 允许列表 | `dsh plugin --profile web add -w /path/to/dsh-one-gateway（随后执行 dsh plugin --profile web exec dsh-gateway -- setup --provider <tailscale-serve\|cloudflare-access\|headscale-tcp-serve>）` | MIT；仓库仅创建约 6 天（2026-08-16），0 forks 无外部审计，作为安全边界组件建议上架前谨慎评估；EasyTier provider 标注 Not shipped；安装后默认惰性（enabled:false），需手动 setup 才启用监听 |
| [PensiveFei/dsh-secure-audit](https://github.com/PensiveFei/dsh-secure-audit) | DSH 只读安全与合规插件：提示注入/越狱检测（规则引擎+可选模型分类器）、中文 PII（手机号/身份证/银行卡等）脱敏、本地配置安全审计（密钥/文件权限/会话文件/环境变量），输出脱敏报告并注册 security-review 技能 | `dsh plugin add dsh-secure-audit（或从 GitHub release tarball 安装：dsh plugin add github:PensiveFei/dsh-secure-audit#<commit>）` | MIT；仅针对 dsh-tools 0.1.0-rc.7 测试，DSH 尚未 1.0，升级后需重新验证；检测为启发式规则，可能漏报误报；仓库创建于 2026-08-19，较新且星标少 |
| [niaccky/dsh-install-guard](https://github.com/niaccky/dsh-install-guard) | 拦截 DSH bash 工具中的 npm install：解析命令后并行审计漏洞（OSV.dev）/许可证（SPDX）/体积（Bundlephobia）/健康度（typosquat），按策略返回 allow / ask / deny；另注册只读 dep_check 工具 | `dsh plugin --profile web add dsh-install-guard` | MIT；审计时向 npm registry、OSV.dev、Bundlephobia、npm downloads API 发送包名与版本；无 API key、不读源码；默认 fail-open，可配 failClosed: true |
| [ang-XWBWZ/dsh-approval-ai](https://github.com/ang-XWBWZ/dsh-approval-ai) | AI 审批应答器:用统一 LLM 路由自动应答 DSH 审批提示,带 fail-closed 策略检查;注册原生 /approval-ai 斜杠命令,设置经 approval-ai settings 命名空间实时生效,无需手改 cordis.patch.yml。 | `pnpm dsh plugin --profile approval-ai add @llangtop/dsh-approval-ai@next (dev: pnpm dsh plugin --profile approval-ai-local add /mnt/data/demo/dsh插件/approval-ai or add the packed .tgz)` | MIT；Prerelease version; pin the exact tag and review the fail-closed policy rules before use on production profiles. |
| [arrow949/dsh-turn-approval](https://github.com/arrow949/dsh-turn-approval) | 任务级授权:在 DSH Web 审批卡片上增加「允许本次任务」按钮——请求 danger-full-access 时只授权当前任务余下时间内的同类升级,任务结束授权自动消失;授权仅存内存,进程重启/卸载/session 释放即失效(fail-closed),不修改官方 bundle 文件。 | `dsh plugin --profile web add github:arrow949/dsh-turn-approval#<commit-sha> (or: dsh plugin --profile web add ./dsh-turn-approval; remove: dsh plugin --profile web remove dsh-turn-approval)` | MIT；Reuses official ApprovalPanel CSS class names — may need compatibility updates if DSH changes that component. |
| [BlockRunAI/dsh-clawrouter](https://github.com/BlockRunAI/dsh-clawrouter) | Second brain for the DSH agent: runs a strong review model over material you choose before risky tool calls run, mounted as an extra model route without changing the default model (dsh-base stays deepseek-official); 70 models from one wallet (x402) where configured; per-profile enable in cordis.patch.yml. | `dsh plugin --profile web add dsh-clawrouter ; enable the route in the profile's cordis.patch.yml` | MIT；Review exactly which calls are routed externally; wallet/x402 only when explicitly configured. |
| [cyzlmh/dsh-cyber-sec](https://github.com/cyzlmh/dsh-cyber-sec) | Authorized security-assessment profile for DeepSeek Harness: scoped network tools, bash in an ephemeral cyberstrike-kali container (auto-removed), authorization/scope guard, durable evidence, 21 security skills and 7 specialist subagents; a mutually exclusive red-team profile enables all 21 skills and removes the scope guard. | `pnpm install && pnpm run pack:bundle, then: dsh plugin --profile cyber-sec add ./dist/<plugins.tgz> ./dist/<bundle.tgz> (absolute or ./-prefixed paths; red-team profile install documented separately)` | Apache-2.0；Use only on authorized ranges; never enable the red-team profile on machines that can reach production networks. |
| [dongsheng123132/dsh-capability-receipt](https://github.com/dongsheng123132/dsh-capability-receipt) | 技能能力凭证 (skill capability receipts): 对 DSH 实际加载的技能生成 SHA-256 内容寻址凭证并 verify（contentHash + fileCount），不返回技能指令/元数据/绝对路径，目录闭包限 256 文件/1MiB/8MiB 且拒绝符号链接。 | `dsh plugin --profile capability-proof add github:dongsheng123132/dsh-capability-receipt#<commit>` | MIT |
| [dongsheng123132/dsh-policy-drift-proof](https://github.com/dongsheng123132/dsh-policy-drift-proof) | 策略漂移审计 (policy drift evidence): 只读、内容寻址、值脱敏的策略/配置漂移证据（inspect/verify）。 | `dsh plugin --profile policy-proof add github:dongsheng123132/dsh-policy-drift-proof#<commit>` | MIT |
| [henlii/dsh-plugins](https://github.com/henlii/dsh-plugins) | 插件集合：dsh-web-auth 为内网/LAN/Tailscale 访问提供密码认证+信任校验（非回环 /api 与 WebSocket 需登录，认证后特权页可用）；可独立或整包安装 | `dsh plugin --profile web add /path/to/dsh-plugins/plugins/<name>   或   dsh web --patch /path/to/dsh-plugins/cordis.patch.yml` | MIT；@deepseek-ai/* / cordis deps are injected by the official runtime - do not declare them in plugin package.json. |

> 该分类共 **24** 个已核验条目，[查看完整清单 →](docs/categories/security.md)

### 聊天与 IM

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [PGZXB/dsh-feishu](https://github.com/PGZXB/dsh-feishu) | Feishu/Lark chat UI for DSH: every slash command a button on a control-panel card, in-card approvals/questions, streaming cards, QR setup | `npx @deepseek-ai/dsh plugin --profile feishu add @dsh-feishu/dsh-feishu@latest` | MIT；Requires Feishu/Lark app credentials and a bot webhook; processes inbound messages and approvals — restrict who can send commands; external network egress to Feishu APIs |
| [wenbin-wb/dsh-bridge](https://github.com/wenbin-wb/dsh-bridge) | 多通道远程访问：局域网扫二维码在手机上继续会话（默认端口 3082）、Cloudflare 隧道一键公网、自建隧道固定域名、微信 Bot（多工作区/会话持久化/媒体/审批） | `dsh plugin --profile web add @wenbin_wb/dsh-bridge` | MIT；会把 DSH Web UI 暴露到局域网（默认端口 3082）或公网隧道；微信 IM 通道可驱动并审批 agent 操作；首次使用会下载 cloudflared；自建隧道请按文档配置访问路径前缀 + 令牌鉴权 |
| [MarioZZJ/cc-notify-hooks](https://github.com/MarioZZJ/cc-notify-hooks) | 为 AI 编程 Agent 的等待/权限确认事件提供分级推送：短通知秒级触达（系统通知、手机推送），长通知分钟级异步兜底（企业微信/飞书/Slack 等），多 Agent 共享同一份配置，用户响应后自动作废排队推送 | `bash install/dsh.sh  (或 cd cc-notify-hooks && bash install.sh dsh)` | MIT；非浏览器 Cookie 类风险；但要求用户提供外部 IM/推送服务的私密凭证并对外开放 Agent 会话内容元数据，需谨慎保管 webhook/API key 配置；卸载需手动编辑 ~/.dsh/cordis.patch.yml 删除对应条目 |
| [tencent-connect/dsh-qqbot](https://github.com/tencent-connect/dsh-qqbot) | Official QQ Bot IM channel plugin for dsh: QQ WebSocket transport, QR扫码 credential binding, per-peer isolated agents, Markdown chunked replies, slash commands, preset mounting | `npx @deepseek-ai/dsh plugin --profile qqbot add @tencent-connect/dsh-qqbot; export QQBOT_APPID/QQBOT_SECRET; npx @deepseek-ai/dsh --profile qqbot` | MIT；IM 机器人接收外部消息并驱动 agent 工具，注意会话权限与敏感操作边界 |
| [THEWOLFWALKER/dsh-notifier](https://github.com/THEWOLFWALKER/dsh-notifier) | Native Cordis plugin: notify() API + auto event push (turn/end, approval/asked, agent/error) to 27 channels; 6 inbound channels for phone remote approval/conversation, stall alerts with stop button. | dsh plugin add dsh-notifier --profile <profile-name>; then add channel config (botToken/webhook) to cordis.patch.yml; see README | MIT；27 渠道含 IM bot/webhook 凭据；6 路入站支持手机远程审批/续聊/steer，靠 HMAC 一次性 token + 成员绑定，需自行加固 |
| [zhuiyueya/dsh-im-gateway](https://github.com/zhuiyueya/dsh-im-gateway) | Aggregated IM gateway: drive dsh agents from WeChat, Feishu, Telegram, Discord, QQ, WhatsApp and 20+ channels; per-chat sessions, remote approval bridge, whitelist defaults, media send (im_send_file), Web GUI channel connector | `dsh plugin --profile web add dsh-im-gateway ; restart dsh web ; connect channels in Settings -> IM 网关 (config via cordis.patch.yml)` | MIT；接入微信/WhatsApp 需扫码（个人号），其余渠道需 bot token；支持远程审批与远程驱动 agent，凭据与白名单须妥善配置 |
| [AX1202/ax-feishu-bridge](https://github.com/AX1202/ax-feishu-bridge) | 飞书/Lark 机器人消息桥接，扫码或凭据接入，私聊/群聊/话题独立会话、流式回复与聊天内命令，同时支持 Pi 与 DSH 双平台 | `dsh plugin --profile web add ax-feishu-bridge --ignore-scripts（DSH 侧）；配置存 ~/.dsh/feishu/config.harness.json` | MIT；飞书/IM 消息可触发本机 agent 会话；持有 App Secret/Bot 凭据，建议仅授权可信联系人与群 |
| [xmanrui/dsh-im](https://github.com/xmanrui/dsh-im) | 把 IM 机器人接入 DSH：统一管理飞书/微信/钉钉/企业微信/QQ/Telegram/Discord/WhatsApp 八个渠道，扫码或凭据接入、流式回复与设置页管理 | `dsh plugin --profile web add @xmanrui/dsh-im（或 npx -y github:xmanrui/dsh-im install）；重启 dsh web 后在 设置→插件→IM机器人 配置` | MIT；八个 IM 渠道消息可触发本地 agent；凭据仅提交本机 Host 并写受保护存储；卡片 webhook 默认监听 0.0.0.0:3001 |
| [amlyczz/dsh-lark-link](https://github.com/amlyczz/dsh-lark-link) | 飞书/Lark 双向桥：扫码 30 秒建应用，多模式 Agent 每会话独立，卡片化命令，零丢失 Outbox + Inbound WAL 补发，图片/文件多媒体进出，/doctor 诊断包；默认 Full access 沙箱 + 审批 never | `dsh plugin --profile web add dsh-lark-link --ignore-scripts; dsh web; 会话内 /lark setup 扫码后 /lark start` | MIT；飞书消息可驱动本机 agent；默认 Full access + 审批 never，持 App Secret 凭据且诊断包含会话日志出站，务必收紧权限 |
| [agent-plaza/agent-plaza](https://github.com/agent-plaza/agent-plaza) | Zero-signup public commons for AI agents: exposes plaza_list_posts / plaza_create_post / identity / flowers HTTP tools to the dsh model; also ships skills/agent-plaza SKILL.md for Codex/Cursor/Claude Code/Hermes. | npx -y @deepseek-ai/dsh plugin --profile web add github:agent-plaza/agent-plaza (or `add .` in checkout); skill: npx skills add agent-plaza/agent-plaza --skill agent-plaza -g -y | MIT；Primary project is a Cloudflare Workers service (D1 DB); the DSH part is the tool bundle. |

> 该分类共 **65** 个已核验条目，[查看完整清单 →](docs/categories/chat-im.md)

### 命令行与终端

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [wuwuzhige-sudo/dsh-terminal-panel](https://github.com/wuwuzhige-sudo/dsh-terminal-panel) | Manual Terminal tab inside DSH web conversation view: run host commands from the browser, persistent cwd, sudo password prompt, command history. | dsh plugin --profile web add <your-account>/dsh-terminal-panel   (then append `- id: dsh-terminal-panel / name: 'dsh-terminal-panel'` to cordis.patch.yml) | MIT；Treat as full remote shell on the host; restrict network exposure of the dsh web port. |

> 该分类共 **1** 个已核验条目，[查看完整清单 →](docs/categories/cli.md)

### 语音

> 暂无已核验条目。

### 清单与资源

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [bruc3van/dsh-desktop-safe-market](https://github.com/bruc3van/dsh-desktop-safe-market) | 先审后装插件市场 | `` | MIT |
| [qichuang321/dsh-plugin-browser](https://github.com/qichuang321/dsh-plugin-browser) | 插件市场入口+运维面板 | `` | MIT |

> 该分类共 **2** 个已核验条目，[查看完整清单 →](docs/categories/lists.md)

### 用量与计费

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [bpc-oss/dsh-web-billing](https://github.com/bpc-oss/dsh-web-billing) | RMB/USD token-billing for dsh web: official-policy auto pricing with peak/off-peak hours, per-message ledger, account balance polling, locale-driven currency display; host /billing route + hand-written client fee badge/panel (read-only over session/event). | `dsh plugin --profile web add github:bpc-oss/dsh-web-billing  (or dsh plugin --profile web add dsh-web-billing after publish); restart dsh web` | MIT |
| [brittanistrehlowll-oss/dsh-quota-panel](https://github.com/brittanistrehlowll-oss/dsh-quota-panel) | Provider quota/balance corner panel for the dsh web surface: server-side credential proxies plus a config-driven page badge; shipped defaults overridable in the profile's cordis.patch.yml. | `dsh plugin --profile web add "github:brittanistrehlowll-oss/dsh-quota-panel" ; restart dsh web (bundle layers apply at boot)` | MIT；Review which provider keys the credential proxies touch. |
| [dshiq04/dsh-deepseek-balance](https://github.com/dshiq04/dsh-deepseek-balance) | 余额查看 (API balance widget): web UI 侧边栏底部（Settings 上方）展示 DeepSeek API 余额，悬停显示币种/总额/赠送/充值，可配置颜色与手动刷新；API key 存 $DSH_HOME/settings.yaml 或 DEEPSEEK_API_KEY env。 | dsh plugin --profile web add dsh-deepseek-balance --link <path-to-this-package>, plus `- id: dsh-deepseek-balance` loader entry in $DSH_HOME/profiles/web/cordis.patch.yml (package must be resolvable from the profile node_modules) | MIT；Cross-device setup needs 4 manual steps; on this machine it relies on a local junction into the dsh installation's @deepseek-ai dir. |
| [Ghost011118/dsh-balance-meter](https://github.com/Ghost011118/dsh-balance-meter) | 余额与会话成本面板：Web GUI 显示 DeepSeek 账户余额与按会话 token 成本；account balance and session-cost readout for the DSH Web GUI | `dsh plugin --profile web add https://github.com/Ghost011118/dsh-balance-meter   (or dsh plugin --profile web add link:$(pwd)/dsh-balance-meter)` | BSD-3-Clause；Needs Harness 0.1.0-rc.6+ web profile; pairs with dsh-autostart for stable hosting |
| [Han-1413141/dsh-cost-meter](https://github.com/Han-1413141/dsh-cost-meter) | 会话费用统计（中英双语）：本会话/当日费用、历史记录与官方价格同步；会话徽章、侧边栏余额与预算图框、设置页 | `dsh plugin --profile web add github:Han-1413141/dsh-cost-meter` | MIT |
| [hccccc01333/dsh-analytics](https://github.com/hccccc01333/dsh-analytics) | Agent FinOps/Token 用量分析：从会话 Engine+Cache 收集用量，webServer 挂载时提供只读 /analytics JSON 路由与浏览器 client bundle，含 skill/sub-agent ROI 分析 | `dsh plugin --profile web add dsh-analytics (或 add github:you/dsh-analytics#<sha> / 本地目录)` | MIT |
| [hnmrxz/dsh-plugin-deepseek-balance](https://github.com/hnmrxz/dsh-plugin-deepseek-balance) | 底部状态栏实时显示 DeepSeek 账户余额（同源路由 /dsh-deepseek-balance，credentials seam 实时解析 API Key，10 秒缓存） | `npm install dsh-plugin-deepseek-balance 后，在 ~/.dsh/profiles/web/cordis.patch.yml 插入 name: dsh-plugin-deepseek-balance` | MIT；Not yet published to npm - use local install until published. |
| [hnmrxz/dsh-plugin-usage-dashboard](https://github.com/hnmrxz/dsh-plugin-usage-dashboard) | 底部状态栏 DeepSeek 用量与估算花费：按会话聚合 token/成本，余额预算告警（复用与余额插件同一条凭据链路） | `npm install dsh-plugin-usage-dashboard 后，在 ~/.dsh/profiles/web/cordis.patch.yml 插入 name: dsh-plugin-usage-dashboard` | MIT |
| [hurry060215-tech/dsh-api-usage-bar](https://github.com/hurry060215-tech/dsh-api-usage-bar) | Web UI 轻量 API token 用量条：按缓存输入/未缓存输入/输出三分段显示用量构成与数值，纯前端不新增模型工具或 token 开销 | `dsh plugin --profile web add github:hurry060215-tech/dsh-api-usage-bar#v0.1.0，重启 dsh web 并刷新页面` | MIT；适用于 DSH >=0.1.0-rc.6 <0.2.0；条形表达的是用量构成而非账户余额进度 |
| [imeepos/dsh-billing-plugin](https://github.com/imeepos/dsh-billing-plugin) | 实时计费：Service+Consumer+Policy 三角色，价格/峰谷窗口/预算全部配置化，超预算时下一步被拒绝并记录预算耗尽通知 | `在 profile 的 cordis.patch.yml(或自有 cordis.yml) 添加挂载行 name: "dsh-billing"，用 dsh --profile <p> --dump-config 确认已入插件树` | MIT；教材随书代码(第 11–15 章)，配置价格/预算需自行核对；仓库无独立 LICENSE 文件(仅 package.json 声明) |

> 该分类共 **38** 个已核验条目，[查看完整清单 →](docs/categories/billing.md)

### Agent、自动化与工作流

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [ChongCyrus/Vibe-Mathematics](https://github.com/ChongCyrus/Vibe-Mathematics) | Natural-language multi-agent math solving: explorer/solver/verifier/planner collaboration, independent review-debate-adjudicate cross-validation, resume, per-project isolation. | `dsh plugin --profile <profile> add github:ChongCyrus/Vibe-Mathematics (or npm dsh-vibe-math)` | MIT；Depends on ~21 @deepseek-ai/dsh-* host plugin rows; missing rows break preset mounting; very new repo. |
| [chumingjun/harness-one](https://github.com/chumingjun/harness-one) | Canvas-based DAG workflow editor embedded in dsh UI: agent nodes, QuickJS sandbox script nodes, HTTP nodes, cron/webhook triggers, Feishu doc read/write. | `dsh plugin --profile web add dsh-ccpg-one && dsh web` | MIT；Requires Node.js >= 22.15.0; embedded canvas depends on DSH-better-sidebar (standalone /wf1/ canvas still works). |
| [KelaoHu/dsh-lowtide](https://github.com/KelaoHu/dsh-lowtide) | Queue tasks during the day, run them in off-peak low-price windows, produce morning reports; L1-L3 adjudication levels. | `dsh plugin --profile web add https://github.com/KelaoHu/dsh-lowtide/releases/latest/download/dsh-lowtide.tgz` | MIT；Do not expose port 3080 publicly; enable file whitelist and daily budget for unattended L3 usage. |
| [SeaOf0/dsh-redteam-model](https://github.com/SeaOf0/dsh-redteam-model) | Security-workflow automation: stage-gate enforcement, scanner tool wrappers, webshell management, asset hunting, cross-session campaign memory. | `dsh plugin --profile web add github:SeaOf0/dsh-redteam-model` | MIT；Offensive security tool — webshell generation, AV-evasion and credential handling included; authorized redteam use only. |
| [Unclecheng-li/DeepSec](https://github.com/Unclecheng-li/DeepSec) | Agent tools for defensive code security audit and authorized penetration testing as DSH native bundles. | `dsh plugin --profile <profile> add /path/to/DeepSec/dsh-plugins/deepsec-shield; ... deepsec-spear` | MIT；Spear is offensive security tooling — strictly for authorized targets/CTFs; signed scope mandatory. |
| [amlyczz/dsh-agy-link](https://github.com/amlyczz/dsh-agy-link) | Registers 'antigravity' as a native DSH model provider streaming Gemini/Claude/GPT-OSS via agy CLI; quota HUD; /agy commands. | `dsh plugin --profile web add dsh-agy-link` | MIT；Multi-account quota rotation may violate Google Antigravity ToS; requires system proxy/TUN in restricted regions. |
| [guo6x/dsh-pilot](https://github.com/guo6x/dsh-pilot) | Browser automation for DSH agents: open pages, DOM snapshots, click/type, navigation, JS eval, screenshots, form filling and uploads. | `dsh plugin --profile web add github:guo6x/dsh-pilot` | MIT；Browser control tools (pilot_eval, pilot_upload) should be scoped by host permissions. |
| [HiWhaleW/dsh-toolbox](https://github.com/HiWhaleW/dsh-toolbox) | Installs 31 DSH tools across 4 bundles: URL/text research, bounded context routing, preflight bundle scanning, compatibility reports. | `git clone ... && npm pack --workspace @dsh-toolbox/<component> (x4) && dsh plugin --profile toolbox add ./dist/*.tgz && dsh --profile toolbox` | PolyForm-Noncommercial-1.0.0；PolyForm Noncommercial license (no commercial use); experimental MVP targeting DSH 0.1.1-rc.2. |
| [CC19990113/dsh-plugin-codegraph](https://github.com/CC19990113/dsh-plugin-codegraph) | Lets the agent answer structural code questions (where declared, who calls it, impact, reachability) via 10 read-only codegraph operations. | `dsh plugin --profile <name> add dsh-plugin-codegraph` | MIT；dsh is in developer preview; indexer tied to schema v4 of the codegraph CLI. |
| [ExElectron/dsh-tool-hongtou](https://github.com/ExElectron/dsh-tool-hongtou) | Generates standard red-header official documents (/hongtou) as Word 2003 XML with deterministic numbering and formatting. | `dsh plugin --profile web add dsh-tool-hongtou` | MIT；China-specific official-document formatting; requires Node >=22.19 and DSH web profile restart after mount. |

> 该分类共 **231** 个已核验条目，[查看完整清单 →](docs/categories/agents-workflows.md)

### 集成与分享

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [kinyokun/dsh-session-import](https://github.com/kinyokun/dsh-session-import) | 会话日志导入：解析 /export 导出的 zip/裸 .jsonl 为新会话，导入前做结构真实性验证 + SHA-256 指纹校验，可同步模型/预设/权限等状态；自带浏览器端「导入对话」按钮与对话框，导入/删除实时推送免刷新 | 手动安装：mkdir -p "$PROFILE_DIR/node_modules/dsh-session-import" && cp host.js client.js package.json 目录，再在 $PROFILE_DIR/cordis.patch.yml 追加 `name: dsh-session-import` 行，重启 dsh web | MIT；导入内容来自外部 zip/jsonl，校验逻辑是唯一防线；删除内存活跃且非本插件导入的会话会被拒（409 live） |
| [omdsh-dev/dsh-shuttle](https://github.com/omdsh-dev/dsh-shuttle) | 在 DSH 与 Codex、Claude Code、Pi、Reasonix、OpenCode 之间双向迁移对话记录，支持 CLI 与 Web UI；CLI 示例 node lib/cli.js export --to opencode --session <id> --destination /tmp/dsh-opencode --apply。 | `通过 DSH 常规插件流程安装（bundle 自带 cordis.patch.yml，挂载 ctx.shuttle 与 migrate-conversations skill）；本地 pnpm build 后 dsh plugin add；CLI 可独立 node lib/cli.js` | MIT；导出文件含完整对话内容，导入目标工具前注意其存储与可见性。 |

> 该分类共 **2** 个已核验条目，[查看完整清单 →](docs/categories/integrations-sharing.md)

### 开发者工具

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [263311487-ux/dsh-verify](https://github.com/263311487-ux/dsh-verify) | 智能体交付物的独立浏览器验收测试：JSON 清单驱动真实 Chromium，断言计算样式与像素差异，输出 HTML 报告与 0/1 退出码（npm CLI / GitHub Action / MCP Server） | `dsh plugin --profile web add dsh-verify` | MIT；Playwright 需下载 Chromium，会真实访问目标页面 |
| [Akimiya-z/codex-guard](https://github.com/Akimiya-z/codex-guard) | Pre-submit quality gate for AI-generated PRs: scans diffs for TODO/FIXME leftovers, hardcoded secrets, non-conventional commit subjects, failing CI; exposes checks to DSH agents via a codex_guard tool | `Mount the DSH bundle in dsh/ (apply dsh/cordis.patch.yml as a profile layer per dsh.bundle.patch manifest); tool shells out to npx --yes codex-guard --git at runtime` | MIT；README gives no explicit `dsh plugin --profile` command string; install requires pointing a DSH profile at dsh/cordis.patch.yml or mounting the dsh/ dir |
| [xiajiajun516/dsh-config-manager](https://github.com/xiajiajun516/dsh-config-manager) | Backup, restore, export, import, migrate and sync a full DSH configuration (settings, plugins, MCP servers, skills, presets, workspaces) as ZIP, with optional encrypted backup (scrypt + AES-256-GCM), rollback snapshots, Git/WebDAV sync, multi-profile, config marketplace, rescue CLI | `dsh plugin --profile web add dsh-config-manager@latest (rescue CLI: npm install -g dsh-config-manager@latest --omit=peer)` | MIT；Sole author project (~14 stars); marketplace pulls community-shared configs — review before importing |
| [yjh051108/dsh-routing-suite](https://github.com/yjh051108/dsh-routing-suite) | Runtime injector for DSH (hot-load/unload/reload plugins without restart, dev_* tool family, self-healing) bundled with a task-aware thinking-mode router preset that classifies tasks and injects matched persona + guidance per request | `git clone --recurse-submodules https://github.com/yjh051108/dsh-routing-suite.git && cd dsh-routing-suite && ./install.ps1 ; manual: dsh plugin --profile web add .\injector + Copy-Item preset dirs to ~/.dsh/.agent-presets` | MIT；Brand-new repo (~2 weeks old) yet ~6.7k stars is implausibly high; author publishes retraction notes on parts of the routing theory; Windows-oriented installers |
| [ericshang98/Perfect-Web-Clone](https://github.com/ericshang98/Perfect-Web-Clone) | Pixel-perfect webpage cloning: agent-driven capture -> section plan -> clean React authoring -> Vite build -> measured fingerprint/weight/SSIM scoring -> evidence-based repair, via a deterministic pwc CLI; ships a DSH skill plus optional MCP server | `dsh plugin --profile web add github:ericshang98/Perfect-Web-Clone (plus pip install git+https://github.com/ericshang98/Perfect-Web-Clone.git && playwright install chromium)` | MIT；README also pitches the same skill for Claude Code/Codex; DSH load path exists and is authoritative but is not the headline |
| [PKUfudawei/dsh-capability-menu](https://github.com/PKUfudawei/dsh-capability-menu) | Unified capability menu for DSH: Exposed/Progressive/Blocked policy management for MCP tools & skills, meta_search/meta_invoke metatools, and a web settings tab for live classification control | `dsh plugin --profile web add @daweifu/capability-menu && dsh plugin --profile web add @daweifu/capability-menu-web` | Apache-2.0；Project at v0.1.0, very new (first commits 2026-08-21); default policy keeps everything Exposed; native tools must stay in tools.exposed |
| [WM-CODER/custom-first-control-prompt](https://github.com/WM-CODER/custom-first-control-prompt) | 部署配置的提示词前缀：在部署人格之前按顺序渲染系统提示词段落，并将配置的参考 user/assistant 对话作为真实交替消息注入每个普通对话请求（llm/stream 请求路径拦截，零会话日志写入，保持 KV 前缀缓存复用）；附带浏览器设置面板与 LLM 监听器用于验证 | `dsh plugin --profile web add github:WM-CODER/custom-first-control-prompt（或 npm：dsh plugin --profile web add @wm-coders/dsh-custom-first-control-prompt）` | MIT；插件 2026-08 新发布（0.2.x），历史上有作用域改名等破坏性变更；profile 补丁中残留同 id 的 - insert: 行会导致 web 启动失败；seed 文本为模型可见，非可信通道；聊天 UI 不显示注入的历史消息 |
| [Ephemeral-AI-Lab/dsh-plugins](https://github.com/Ephemeral-AI-Lab/dsh-plugins) | Adds DSH tools: interactive shell exec (codex-shell), session-scoped recurring loops + web UI (loop), deterministic mock turns via real AgentLoop (mock), and session discovery/create/message + /sessions side-chat (sessions) | `dsh plugin --profile web add dsh-codex-shell@0.1.2 ; dsh plugin --profile web add dsh-loop@0.1.3 ; dsh plugin --profile web add dsh-sessions@0.1.1 ; dsh plugin --profile web add dsh-mock@0.1.0` | MIT；codex-shell grants arbitrary shell execution in the DSH host environment (PTY/persistent sessions) — high privilege; mock is marked unstable (0.1.0, API may change); review each plugin's cordis.patch.yml before installing into sensitive profiles |
| [memorax-ai/dsh-harmony](https://github.com/memorax-ai/dsh-harmony) | Runtime patch-coordination library for DSH: patch/replace/decorate other plugins' source via TSQuery AST transforms without forking or touching installed files | `npm install -g dsh-harmony` | MIT；Modifies other plugins' runtime code in memory — only install Patches from trusted sources; mis-patched targets can break or alter plugin behavior |
| [MoFeng2223/dsh-claude-provider](https://github.com/MoFeng2223/dsh-claude-provider) | Adds an explicit Claude provider type to DSH with correct reasoning-parameter mapping per Claude model, model discovery, and adaptive-thinking conversion | `npx @deepseek-ai/dsh plugin --profile web add @mofeng2223/dsh-claude-provider` | MIT；Requires an Anthropic/Claude API key; sends prompts to external Claude endpoints |

> 该分类共 **218** 个已核验条目，[查看完整清单 →](docs/categories/developer-tools.md)

### 知识与研究

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [agentscope-ai/ReMe](https://github.com/agentscope-ai/ReMe) | Long-term memory for DSH agents: automatic conversation capture, BM25+vector search, daily memory consolidation, proactive memory guidance. | `dsh plugin --profile web add @agentscope-ai/reme` | Apache-2.0；ReMe HTTP service has no API-key authentication; keep it bound to localhost. |
| [398894496-arch/runtime36](https://github.com/398894496-arch/runtime36) | Deterministic knowledge retrieval for DSH: short-noun to canonical Obsidian page mapping, read-only krouter_* tools, optional daily self-evolution writer. | `dsh plugin --profile web add github:398894496-arch/runtime36` | MIT；Repo is days old (~13 stars); `dsh plugin add` only mounts read-only tools; verify with test-bridge.mjs before adding. |
| [Soren-ABT/dsh-knowledge](https://github.com/Soren-ABT/dsh-knowledge) | Full knowledge-base/RAG for DSH: multi-format doc import, OCR, per-base embedding config, hybrid retrieval with rerank, 14 knowledge tools. | `dsh plugin --profile <name> add dsh-knowledge` | AGPL-3.0；Intel Macs lack local embedding/OCR; pnpm allowBuilds config required before install. |
| [JingxuanC/causal-memory](https://github.com/JingxuanC/causal-memory) | Gives DSH agents causal memory: record_decision/record_fact, search_causal/search_facts, intervention/counterfactual queries. | `cd <repo> && cargo build --release --bin causal-memory && dsh plugin --profile web add "$PWD/dsh-plugin"` | Apache-2.0；Requires building the Rust binary before install; mutually exclusive with @deepseek-ai/dsh-mcp-client bridge. |
| [TsFreddie/dsh-compaction-instant](https://github.com/TsFreddie/dsh-compaction-instant) | Compacts session history deterministically in milliseconds with byte-exact token preservation, pointer-based recall, recall/search tools and /recall command. | `dsh plugin --profile web add dsh-compaction-instant` | MIT；Very new project (v0.1.4); method 2 auto-bundle path still requires AI-generated preset copy. |
| [vshulcz/deja-vu](https://github.com/vshulcz/deja-vu) | Cross-agent session memory/recall for coding agents: indexes on-disk session history from 20+ harnesses (incl. DSH), exposes MCP recall tools, auto-recall at session start, credential redaction, multi-machine sync | `dsh plugin add dsh-deja (npm package in extensions/dsh); or curl -fsSL https://raw.githubusercontent.com/vshulcz/deja-vu/main/install.sh \| sh && deja install deepseek` | MIT；MCP recall is silent-on-failure by design; credential redaction depends on index-time patterns |
| [zilliztech/memsearch](https://github.com/zilliztech/memsearch) | Persistent cross-agent memory for DSH: auto-captures turns, pre-step memory injection, memory-recall skill, PROJECT.md maintenance. | `uv tool install "memsearch[onnx]" && dsh plugin --profile web add @zilliz/memsearch-dsh` | MIT；Summarization may send conversation content to configured LLM providers; embedding via local ONNX by default (~558MB model). |
| [seriousz158/dsh-memory](https://github.com/seriousz158/dsh-memory) | 本地 Git 托管的长期记忆插件：记忆持久化、事务性同步/回滚、全文搜索、启动注入 summary_snapshot、只读工具（memory_search/memory_context）、备份导出导入、DSH 设置页 UI | `dsh plugin --profile web add github:seriousz158/dsh-memory（npm 版本: dsh plugin --profile web add dsh-git-memory；源码集成见 ./integrations/dsh/install.sh）` | MIT；仅官方支持 macOS(Node 22.x)，Windows 不支持；需重启 profile 生效；npm 名 dsh-git-memory 避免与已占用的 dsh-memory 冲突 |
| [Tencent/WeKnora](https://github.com/Tencent/WeKnora) | 向 DSH agent 注册 4 个只读知识库工具：weknora_search（混合检索）、weknora_read_document、weknora_ask（带引用的合成回答）、weknora_list_knowledge_bases；让企业文档可被检索 | `dsh plugin --profile web add @wxg-prc-cpg/dsh-weknora（或本地: dsh plugin --profile web add ./packages/dsh-weknora），随后 export WEKNORA_BASE_URL / WEKNORA_API_KEY / WEKNORA_KNOWLEDGE_BASE_IDS 并运行 dsh web` | MIT；仓库本身是独立高 star 的 RAG 平台，与 dsh-plugin topic 无关；DSH 集成是官方插件入口，请用最小权限 API key（仅 retrieve） |
| [pypcfx-glitch/risk-rule-design](https://github.com/pypcfx-glitch/risk-rule-design) | 风控规则挖掘工具：对指定数据集做数据质检、单规则挖掘、并行规则集最优组合搜索（F1 平衡），输出自包含 HTML 分析报告；附带 risk-rule-design 专家技能 | `dsh plugin --profile web install dsh-plugin-risk-rule-design（或 dsh plugin --profile web add "github:pypcfx-glitch/risk-rule-design"，GitHub 直装需手动注册 bundle）` | MIT；作者自述为『第一个 dsh 插件，还在完善中』；homepage 字段指向付费课程页而非项目主页；GitHub 直装方式不会自动注册 bundle，需手动编辑 profile package.json；仓库创建于 2026-08-19 |

> 该分类共 **118** 个已核验条目，[查看完整清单 →](docs/categories/knowledge-research.md)

### 设计、媒体与视觉

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [corrinehu/dsh-chat-imagine](https://github.com/corrinehu/dsh-chat-imagine) | Inline image generation with bundled cli-image-gen recovery skill; analyze_image reads local/URL images into structured JSON evidence; set_image_default for channel selection. | `dsh plugin --profile web add dsh-chat-imagine` | MIT；Tested only on DSH Web profile; images live in process memory only (links die on restart). |
| [fandc520/dsh-comfyui](https://github.com/fandc520/dsh-comfyui) | Agent tools comfyui_run/comfyui_object_info/comfyui_workflow submit and inspect ComfyUI workflows, render results in-chat. | `dsh plugin --profile web add dsh-comfyui` | MIT；Works best when DSH and ComfyUI share a filesystem; beta version 0.3.0-beta.4. |
| [dickpy/dsh-imagegen](https://github.com/dickpy/dsh-imagegen) | AI image generation workbench for the DSH web GUI — text-to-image and image-to-image via configurable OpenAI-compatible endpoints, agent-callable tools (generate_image, edit_image), background task queue, multi-model comparison, persistent gallery | `dsh plugin --profile web add @dickpy/dsh-imagegen (or from GitHub Releases tgz), then restart dsh web` | Apache-2.0；Brand-new project (first release Aug 15, 2026); model detection returns a candidate list, not compatibility certification |
| [shanliuling/dsh-image-gen](https://github.com/shanliuling/dsh-image-gen) | Adds in-chat multimodal image generation via a `generate_image` tool with multi-provider support (Gemini/OpenAI/Seedream), interactive preview, copy/download, and session-attached results. | `pnpm dsh plugin --profile web add dsh-image-gen@latest` | MIT；Requires user-owned external provider API keys; outbound calls to third-party image APIs; provider/base URL configurable in settings. |
| [dundunhan/dsh-video-lens](https://github.com/dundunhan/dsh-video-lens) | Two tools that let text-only DSH agents understand local video: frame extraction + vision captioning and ASR transcription, provider-configurable | `dsh plugin --profile web add dsh-video-lens` | MIT；Requires ffmpeg/ffprobe on PATH and external vision/ASR API keys; reads local video files — mind filesystem access scope |
| [MJorgin/dsh-media-skills](https://github.com/MJorgin/dsh-media-skills) | Two free skills: paste-image reading in any (even text-only) session via a free vision failover chain, and image generation (Kolors) — three-engine fault tolerance, no-key entry | `dsh plugin --profile web add github:MJorgin/dsh-media-skills` | MIT；Requires external model API keys (GLM_API_KEY etc.); paste-image reading needs a DSH core build with the api-proxy image-admission patch; keys read from ~/.dsh/secrets or DSH credential store |
| [jing-hy/picturereader](https://github.com/jing-hy/picturereader) | Gives text-only models vision: image_scan (pixel/color/hue/structure analysis), image_ocr (built-in Windows + optional PaddleOCR), image_sample (material/texture pixel sampling), and vision_analyze (unified multi-evidence analysis with optional external VLM semantic bridge). Cross-validates VLM vs. pixel/OCR evidence to suppress hallucination. | `dsh plugin --profile web add picturereader` | MIT；Enabling SEE_BASE routes image content to an external/cloud vision endpoint (API key exposure risk); PaddleOCR setup spawns a local Python interpreter; plugin auto-launches a local llama-server if SEE_SERVER_* vars are set. Default config is fully local/offline. |
| [Yts1919/dsh-vision-complete](https://github.com/Yts1919/dsh-vision-complete) | Windows skill pack: SKILL.md + vision.py (image/OCR/object-detect/video/voice/PDF via cloud Qwen), registers qwen-mm-plugins MCP into cordis.patch.yml, clipboard screenshot tool. | Windows only: git clone + run install.bat (needs DASHSCOPE_API_KEY); uninstall via uninstall.bat; see README | MIT；非 dsh plugin 包：脚本把 skill 复制到 ~/.dsh/skills 并在 cordis.patch.yml 追加 MCP 条目；需阿里云 API Key；仅 Windows |
| [121103qwq/dsh-vision-sidecar](https://github.com/121103qwq/dsh-vision-sidecar) | Adds deepseek-vision/deepseek-with-vision to the bundle so text-only models receive image understanding via a hosted vision sidecar; no-build ESM, durable session evidence. | `dsh plugin --profile web add github:121103qwq/dsh-vision-sidecar#v0.1.3 (remove: dsh plugin --profile web remove dsh-vision-sidecar)` | MIT |
| [237229953-create/dsh-vision](https://github.com/237229953-create/dsh-vision) | Automatically routes images to a vision model when the active model is text-only (e.g. DeepSeek-V4); uses the official settings seam (settings.yaml dsh-vision section), cache-friendly, leaves human transcript untouched; no-op when the model natively supports images. | `dsh plugin --profile web add link:D:/dsh-plugins/dsh-vision (or via Settings→插件 extra-plugins card; config in settings.yaml / bundle cordis.patch.yml)` | MIT；README example path is Windows-specific (D:/dsh-plugins/dsh-vision). |

> 该分类共 **78** 个已核验条目，[查看完整清单 →](docs/categories/media-vision.md)

### 网页与浏览器

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [ma-pony/deepspider](https://github.com/ma-pony/deepspider) | AI 原生网页抓取与 JavaScript 逆向：用 Patchright/CDP 观察真实请求与运行时事实，沿调用栈定位参数写入边界，通过独立 Node 语义运行时 (sdenv) 重新生成 Cookie 并以真实请求 (CycleTLS) 验证，导出可脱离浏览器重跑的 Solver | `dsh plugin --profile web add deepspider` | MIT；高权限：浏览器 Cookie/Session 恢复、脚本执行、向任意站点真实出站请求。仅应在自己拥有或已获授权的目标上使用，并遵守目标条款与法律；postinstall 会自动下载 Patchright Chromium |
| [heartleo/hn-cli](https://github.com/heartleo/hn-cli) | Exposes Hacker News tools to DeepSeek Harness agents: ranked feeds (top/new/best/ask/show/job), item comment trees, Algolia search, and user profiles, all via public HN APIs. | `dsh plugin --profile <name> add -w dsh-hacker-news` | MIT；Network egress to third-party HN APIs; query text is sent to hn.algolia.com. The separate Go TUI `hn` binary has an optional translation feature requiring an OpenAI-compatible API key, but that is unrelated to the DSH plugin. |
| [cocofhu/anime-find](https://github.com/cocofhu/anime-find) | 对话内多源搜番（Mikan/AniBT/AnimeGarden）：卡片展示 Bangumi 评分与详情、按字幕组浏览、复制磁力/种子；可选流媒体解析播放 Tab | `dsh plugin --profile web add github:cocofhu/anime-find（本地: dsh plugin --profile web add /abs/path）；更新: dsh plugin --profile web update anime-find` | MIT；向第三方来源站点发搜索/详情请求并经 Host 代理媒体流，含磁力/种子下载能力，需遵守来源条款与版权 |
| [wxkingstar/SpecFusion](https://github.com/wxkingstar/SpecFusion) | Zero-config fused search over 65,600+ API docs from 20 Chinese open platforms (WeCom/Feishu/DingTalk/Taobao/Douyin etc); ships both DSH native plugin and SKILL.md for Claude/Cursor/Codex | dsh plugin --profile web add @wxkingstar/specfusion-dsh; 或 curl SKILL.md 装入 ~/.claude/skills/ (见 README) | MIT；文档检索走云端服务（SPECFUSION_BASE_URL），注意查询内容外发 |
| [anysearch-team/anysearch-dsh](https://github.com/anysearch-team/anysearch-dsh) | AnySearch 实时 web 搜索 Provider：接管 DSH 原生 web_search，另供能力发现 anysearch_capabilities、垂直 anysearch_search、1-5 路批量搜索 | `npx -y @deepseek-ai/dsh plugin --profile web add @anysearch/anysearch-dsh` | MIT；经第三方 API；匿名配额有限，常规使用需配 ANYSEARCH_API_KEY（存 $DSH_HOME/.credentials.yaml） |
| [Tabbit-Browser/dsh-plugin](https://github.com/Tabbit-Browser/dsh-plugin) | DSH bundle 随插件加载 tabbit-browser Skill：模型经 skill({name:"tabbit-browser"})/\/tabbit-browser 控制 Tabbit 浏览器 (tabbit-cli Runtime)，自动检测/下载国内国际正式版安装包，多实例支持 | `dsh plugin --profile web add github:Tabbit-Browser/dsh-plugin; 需 Tabbit 浏览器 >=1.9.0` | MIT；控制本机 GUI 浏览器并自动下载/安装浏览器安装包；Windows Runtime 需会话切 Full Permission，浏览器页面数据可被模型读取 |
| [awesome-dsh-plugin/dsh-find-plugin](https://github.com/awesome-dsh-plugin/dsh-find-plugin) | In-agent plugin discovery: live GitHub repository search scoped to the official `dsh-plugin` topic, star-ranked; every result comes with a ready-to-run `dsh plugin add` command. | `dsh plugin --profile web add dsh-find-plugin  (or: dsh plugin --profile web add github:awesome-dsh-plugin/dsh-find-plugin)` | MIT；Requires network access to GitHub at runtime. |
| [canghai666x/dsh-news-plugin](https://github.com/canghai666x/dsh-news-plugin) | 新闻采集工具插件：注册 news_fetch 工具抓取 RSS 新闻源并解析为结构化条目（Node 原生 fetch + 正则，零第三方依赖），五维评分/筛选/简报编排交给模型；附 dsh-news-briefing Skill。 | 将仓库放入 Harness 项目，在 cordis.yml 组合中声明 `- name: './index.ts'`（参考官方 cordis-tutorial/07 第 7 章），node --import tsx ../../vendor/cordis/bin.js 启动 | MIT；仓库根目录无 LICENSE 文件（仅 package.json 声明 MIT）；无 dsh.bundle，安装为非标准组合式（手写 cordis.yml）；基于 2026-08 官方教程，v0.1 API 可能变更。 |
| [ch1bug/dsh-mimo-agent-tools](https://github.com/ch1bug/dsh-mimo-agent-tools) | 把小米 MiMo API 封装为 DSH Cordis 模型工具：mimo_search / vision / audio / video / asr / tts（Python 驱动，MIMO_DRIVER 指向默认安装路径），与 @deepseek-ai/dsh-tools 共存不重复加载。 | `dsh plugin --profile web add /path/to/dsh-mimo-agent-tools（或 github:ch1bug/dsh-mimo-agent-tools）；安装 python 驱动后重启 dsh web，工具自动挂载` | MIT；依赖 MiMo API 可用性与密钥配置。 |
| [Clizo1209/dsh-playwright-browser](https://github.com/Clizo1209/dsh-playwright-browser) | Semantic, multi-tab browser automation for DeepSeek Harness powered by Playwright: abort-aware page operations, Cordis-owned lifecycle cleanup, configurable screenshotDir (default .dsh-browser/screenshots); ships sanitized real-world test suite on public demo sites. | dsh plugin --profile web add dsh-playwright-browser  (or tarball: dsh plugin --profile web add ./dsh-playwright-browser-0.1.3.tgz; headless: dsh plugin --profile headless add ./dsh-playwright-browser-0.1.3.tgz); needs `npx playwright install chromium` | MIT；Requires Playwright Chromium install; pnpm 10+ may need allowBuilds in profile pnpm-workspace.yaml for git installs. |

> 该分类共 **53** 个已核验条目，[查看完整清单 →](docs/categories/web-browser.md)

### 生态与资源

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [zenstory-ai/oh-story-dsh](https://github.com/zenstory-ai/oh-story-dsh) | Fiction/short-drama writing workbench: 23 skills, roles, markdown/JSONL preview, live file-follow. | `npx -y @deepseek-ai/dsh@0.1.1-rc.1 plugin --profile web add @oh-story/dsh@0.1.4 && npx -y @deepseek-ai/dsh@0.1.1-rc.1 web` | MIT；Requires Node.js 24+ and DSH 0.1.1-rc.1; Drama Skills 0.6.0 is a breaking upgrade. |
| [titanwings/distilly](https://github.com/titanwings/distilly) | Meta-skill turning source material into a versioned Person Profile skill with incremental merge, correction layer, rollback, per-host install. | `Clone repo as a skill; for DSH install of generated skills: python3 tools/install_generated_skill.py --skill-dir <dir> --host deepseek-harness --force (defaults to ~/.dsh/skills, honors $DSH_HOME)` | MIT；Handles private personal data — grant chat-history/browser access cautiously. Repo renamed from colleague-skill; default branch dot-skill. |
| [worldwonderer/oh-story-dsh](https://github.com/worldwonderer/oh-story-dsh) | 小说与短剧创作工作台：13 个 Oh Story 小说 Skills + 7 专业 Roles 与 10 个 Drama 短剧 Skills，DSH 原生三栏工作台（项目文件树/编辑器/官方 Chat 同屏）、实时文件跟随、会话作用域创作文件路由、安全原子编辑 | `npx -y @deepseek-ai/dsh@0.1.1-rc.1 plugin --profile web add @oh-story/dsh@0.1.2 && npx -y @deepseek-ai/dsh@0.1.1-rc.1 web（需 Node.js 24+）` | MIT；建议仅从官方 npm 或 GitHub Release 校验过的 tarball 安装，注意其信任边界（loopback 默认信任、trustedHosts 需显式声明） |
| [EverMind-AI/SkillCorpus](https://github.com/EverMind-AI/SkillCorpus) | 将分散的 SKILL.md 文件聚合并整理成可检索的技能语料库，通过 skill-search 插件在 DSH 每轮应答前自动检索并注入技能到上下文，附检索模型（bi-encoder+reranker）与评估基准 | `cd <harness-workspace> && cp -r <repo>/engine-typescript packages/skill/skill-search && 在 tsconfig.host.json 的 references 加 {"path":"./packages/skill/skill-search"}，pnpm install，再在 cordis.yml 加 skill-search 配置（详见 skillcorpus_plugin/INSTALL.agent.md）` | Apache-2.0；项目极新（2026-08-11 创建）；DSH 安装为手动复制源码+改配置，非官方 registry 分发；如已挂载 dsh-tool-skill 会重复发布技能需自行处理 |
| [PensiveFei/deep-read-summarize](https://github.com/PensiveFei/deep-read-summarize) | DSH 深度精读工作流：输入书籍（PDF/EPUB/MOBI）、论文（arXiv/PDF/HTML）、视频（yt-dlp 字幕）或网页，经解析器分块、并行子代理 MapReduce 精读、JSON Schema 约束输出、质量校验后，生成带 YAML frontmatter 的可直接存入 Obsidian 的结构化 Markdown 笔记 | `npm install deep-read-summarize；或在 dsh profile 目录 pnpm add ./deep-read-summarize-0.3.0.tgz，然后在 dsh.profile.bundles 追加 '- deep-read-summarize'，重启 dsh web` | MIT；作者自声明为 unofficial 第三方工具；DSH 仍为 developer preview，接口可能变化；视频类型依赖本机 yt-dlp |
| [bradeGithub/DSH-Plugins-Marketplace](https://github.com/bradeGithub/DSH-Plugins-Marketplace) | DSH Web 设置页内的插件市场：经 CI 构建的静态索引浏览 GitHub dsh-plugin topic 全量仓库（3900+ 插件、14000+ 通用 Skills），支持一键安装 / 版本检测 / 自动更新 / 已安装识别 | `dsh plugin --profile web install bradeGithub/DSH-Plugins-Marketplace` | MIT；会克隆并安装任意第三方仓库；第三方安装脚本与 npm 生命周期脚本仅在明确确认后执行；索引经 jsDelivr CDN 加载并以 GitHub 搜索 API 兜底 |
| [AwesomeHou/dsh-plugin-marketplace](https://github.com/AwesomeHou/dsh-plugin-marketplace) | DSH 插件市场：实时同步 GitHub dsh-plugin topic（1800+ 仓库）为设置页标签，提供一键安装/更新/停用/卸载及 market_search/market_install 等 agent 工具 | `dsh plugin --profile web add https://github.com/AwesomeHou/dsh-plugin-marketplace，安装后重启 harness` | MIT；market_install 经 host 侧以 shell 执行 pnpm/dsh 安装任意第三方插件（校验了 shell 元字符，仍有供应链风险） |
| [dhicoc/dsh-reverse-skill](https://github.com/dhicoc/dsh-reverse-skill) | reverse-skill 完整 DSH 插件版：把上游 85 个 SKILL.md（逆向/授权渗透/安全研究 + CTF 赛道）经 ctx.skills.registerProvider 注册为 DSH 技能库 | `dsh plugin add github:dhicoc/dsh-reverse-skill（读取 cordis.patch.yml 插入 reverse-skill 插件；安装后自动注册 85 个技能）` | MIT；打包 85 个逆向/渗透技能，仅供授权测试；技能可能驱动安全工具调用，且声明 allowed-tools 不被 dsh 强制 |
| [mishibeikejie/zat-dsh-engine](https://github.com/mishibeikejie/zat-dsh-engine) | DSH 可视化插件市场：Settings→Plugins 增加 Plugin Market 标签，GitHub dsh-plugin topic 1700+ 仓库浏览/搜索/一键安装-更新-卸载，AI 找插件 + 安装前健康与安全检查，断网自动镜像回退 | `dsh plugin --profile web add github:mishibeikejie/zat-dsh-engine; 移除: dsh plugin --profile web remove zat-dsh-engine` | MIT；本质是包管理器：执行 pnpm 安装第三方插件的 prepare/postinstall 脚本、读取本地 git 凭证（star/GitHub token）并写 profile 配置，务必先看其安全扫描结果 |
| [sikadi233-hub/minecraft-dev](https://github.com/sikadi233-hub/minecraft-dev) | Gives DSH agents Minecraft plugin/mod development: scaffold projects, run Gradle builds, load version-aware API references, delegate to a 4-subagent team. | `dsh plugin --profile web add minecraft-dev` | MIT；mc_gradle depends on taskkill (win32 only); local user skills with same names override bundled ones. |

> 该分类共 **115** 个已核验条目，[查看完整清单 →](docs/categories/ecosystem-resources.md)

### 纯属好玩

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [TongY1n/ui-muyu](https://github.com/TongY1n/ui-muyu) | 赛博木鱼：Web 悬浮小摆件，点击敲击累积功德、可拖拽，刷新不丢进度 | `dsh plugin --profile web add github:TongY1n/ui-muyu` | MIT；纯浏览器 UI；无网络请求、无 API Key、无文件/会话/凭据访问；仅 localStorage 存功德/位置/配色 |
| [Sutera-Diffusus/dsh-whale-musume](https://github.com/Sutera-Diffusus/dsh-whale-musume) | 在 DSH Web 界面右下角提供可拖拽看板娘：监听工具运行状态切换工作/待机立绘（90+ 张，含节日换装与 13 种梗表情）、530+ 条台词与定时闲聊、摸头/分区互动特效、养成（心情/好感/等级/签到/每日任务）与 39 个成就墙、戳泡泡小游戏、可选天气陪伴与全屏天气特效，设置项集成进 DSH 设置页。 | `dsh plugin --profile web add github:Sutera-Diffusus/dsh-whale-musume` | MIT；官方测试环境仅 Windows 10/11 + Edge/Chrome，绑定 DSH 0.1.0-rc.6 前端结构，DSH 升级后注入点可能失效；脚本模式修改内置前端文件（务必保留备份目录，勿与 bundle 模式混用）；启用天气需联网并可能填入第三方 API Key；package.json 标记 private:true，仅能经 github: 源安装。 |
| [QCYTSN/dsh-dafeiyu](https://github.com/QCYTSN/dsh-dafeiyu) | Windows 桌面原生 Agent 伴侣：由 DSH 会话真实事件驱动的透明无边框始终置顶窗口，展示思考/工作/等待/完成/错误状态；随 DSH 启停 | `pnpm exec dsh plugin --profile web add dsh-dafeiyu@alpha（Windows/WSL2；或 GitHub Release .tgz: dsh plugin --profile web add "...tgz"）` | MIT |
| [PC2005-cloud/dsh-pet](https://github.com/PC2005-cloud/dsh-pet) | DSH Web 界面桌面宠物：51 个透明 webm 动画随机链播、屏幕漫游、点击/拖拽；附提示词配方+AI 视频素材生成链可自造宠物 | `dsh plugin --profile web add dsh-pet (本地包: dsh plugin --profile web add file:D:/path/to/dsh-pet)` | MIT |
| [c3ll256/dsh-toy](https://github.com/c3ll256/dsh-toy) | DSH plugin controlling toy hardware via Buttplug/Intiface (BLE/serial/USB, auto-downloaded pinned engine) and MonsterParty shared links, with intensity/duration/timeout guardrails | `npx -y @deepseek-ai/dsh plugin --profile web add github:c3ll256/dsh-toy` | BSD-3-Clause；成人向硬件控制；需蓝牙/串口权限与外部分享令牌，注意使用授权与保险丝 |
| [cakeni/harness-pet](https://github.com/cakeni/harness-pet) | 桌面宠物：一只住在 DeepSeek Harness 里的小鲸鱼——像素精灵内嵌 client bundle（Canvas 鲸鱼兜底），按当前活动工具展示 working 状态，不认识的工具只报 working、绝不伪造工具名。 | `dsh plugin --profile web add github:cakeni/harness-pet（或 dsh plugin --profile web add harness-pet / link:../harness-pet）` | MIT；要求 Harness 0.1.0-rc.6 + pnpm；Git 依赖触发 prepare 构建，被 pnpm 拦截时需在 profile 的 pnpm-workspace.yaml 加 allowBuilds；安装/移除后需重启 dsh web。 |
| [Fromlan/dsh-godot-tool](https://github.com/Fromlan/dsh-godot-tool) | 驱动 Godot 4.x 编辑器：回环 TCP JSON-lines 桥 + 27 个 godot_* 工具（开/停场景、播放错误、场景树、lint、导出构建）；drive the Godot 4.x editor from the agent via loopback TCP bridge | `Install addons/agent_rpc into the Godot project; mount @deepseek-ai/dsh-godot-tool from the harness workspace (packages/extensions/tool-godot) or via '--patch' overlay pointing at dsh-godot-tool/src/index.ts + compose dsh-tools` | MIT；Mirror of the official harness extension with workspace-scoped peer deps; cleanest install is inside the deepseek-harness monorepo or an explicit patch overlay |
| [HomophonicFate/rpg-maker-mac-skill](https://github.com/HomophonicFate/rpg-maker-mac-skill) | DSH 技能：在 macOS 上原生运行 RPG Maker MV/MZ 游戏并套用 MTool 翻译文件（环境搭建/翻译整合/插件注册/启动器创建）；触发 /rpg-maker-mac-skill 或自然语言 | `把安装指南 URL 发给 DSH agent（'帮我安装这个 skill: …/docs/install.md'）-> 装入 ~/.dsh/skills/rpg-maker-mac-skill/` | 未发现；No LICENSE detected in repo metadata; MTool has no macOS version so only existing translation files can be loaded; upstream plugin attribution kept (knowlet/RPGDynamicTranslation). |
| [liyupi/dsh-kun-like-pet](https://github.com/liyupi/dsh-kun-like-pet) | 桌面宠物「小坤宠」：Web 界面右下角随 Agent 工作状态切换 9 种动画，任务完成播放「你干嘛~哎哟」音效；host 状态机 + client shell.overlay 渲染 + 拖动/点击互动。 | node build-kunpet-package.mjs 生成载荷 → DSH 会话内调 `cordis_define`（kind:new，提供 spritePath/voicePath）→ `cordis_run` 激活 | MIT；动态插件会话级绑定，仅注入激活它的会话页面；状态事件经轮询 agents 服务获取（事件监听实测不可靠，见 CHANGELOG v3/v4）。 |
| [lvyuchuiyi/dsh-funpack](https://github.com/lvyuchuiyi/dsh-funpack) | 趣味插件包:夸夸(/praise)、运势(/fortune)、摸鱼战报(/report)、番茄钟(/pomodoro)、休息提醒(/break),右下角鲸鱼娘桌宠(自定义形象/台词/互动键,支持 HatchPet/Codex 宠物包),/persona 切换说话人设;单文件零依赖零构建。 | `dsh plugin --profile web add github:lvyuchuiyi/dsh-funpack (或 dsh plugin --profile web add ./dsh-funpack)` | MIT；桌宠素材来自 dsh-pet(BSD-3) 与 Taffy 宠物包,随插件打包供个人/爱好者使用。 |

> 该分类共 **37** 个已核验条目，[查看完整清单 →](docs/categories/fun.md)
## 官方内置能力（不是社区插件）

官方仓库中已有大量随运行时分发的包；它们属于 DSH 的可组合系统组件，不宜与独立社区扩展混为一谈。官方架构文档列出了模型、工具、Session、Agent Loop 等可替换缝隙。[2] 下表列出用户最常接触的官方能力入口。

| 官方模块 / 族 | 作用 | 来源 |
| --- | --- | --- |
| `dsh-base`、`dsh-web-app`、`dsh-headless` | 基础、Web 与无界面 Profile Bundle | [官方源码 packages/bundle](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/bundle) |
| `llm-deepseek`、`llm-pi-ai`、`llm-retry` | 模型适配与重试 | [官方源码 packages/llm](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/llm) |
| `tool-web`、`web-search-deepseek`、`web-search-exa`、`web-search-perplexity` | Web 工具与搜索 Provider | [官方源码 packages/web](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/web) |
| `skill-filesystem`、`tool-skill` | Skill 发现与调用 | [官方源码 packages/skill](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/skill) |
| `sandbox-*`、`fs-*`、`shell-*` | 沙箱、文件系统与命令执行边界 | [官方源码 packages](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages) |
| `session-*`、`subagent-*`、`schedule`、`workflow-*` | 会话、子 Agent、日程与工作流 | [官方源码 packages](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages) |

## 相关项目与观察名单（不计入主目录）

以下项目与 DSH 或 DeepSeek 生态相关，但**不是本次已核验的可装载原生插件**，或主仓库本身并非插件。它们被刻意放在主目录之外，以便后续独立核验。

| 项目 | 定位 | 原因 |
| --- | --- | --- |
| [whiteguo233/OpenBiliClaw](https://github.com/whiteguo233/OpenBiliClaw) | 本地内容发现 Agent | 主仓库指向独立的 `whiteguo233/dsh-openbiliclaw` 客户端插件；应审核该独立仓库后再纳入 |
| [Anionex/agent-vision-toolkit](https://github.com/Anionex/agent-vision-toolkit) | 通用视觉 CLI 与 Skill | DSH 原生 Bundle 位于独立的 `Anionex/dsh-vision-toolkit` 仓库，待单独核验 |
| [paean-ai/deeptide](https://github.com/paean-ai/deeptide) | 独立 macOS 编程 Agent | 未发现 DSH Bundle、Patch 或 DSH 安装步骤 |
| [yejiming/MuseAI](https://github.com/yejiming/MuseAI) | AI 角色与文字冒险桌面应用 | 支持 DeepSeek API 不等于支持 DSH 插件协议 |
| [PM-Shawn/Abu-Cowork](https://github.com/PM-Shawn/Abu-Cowork) | 本地优先桌面 Agent | 未核验到 DSH Profile/Bundles 挂载方式 |
| [cofy-x/axern](https://github.com/cofy-x/axern) | Agent 沙箱与持久化服务 | 是可关联基础设施，不是 DSH 插件 |

## 安装与安全

先安装 DSH 并启动一个 Profile。官方快速开始方式是：

```bash
npx @deepseek-ai/dsh web
```

随后使用项目说明中给出的 `dsh plugin --profile <profile> add …` 命令。安装前应锁定版本或 commit、阅读 `package.json`、`cordis.patch.yml` 与依赖安装脚本；不要在不了解代码的情况下执行 `curl \| bash`、`pnpm` 生命周期脚本或授予系统级凭据。

| 风险级别 | 涉及项目示例 | 安装前的最低措施 |
| --- | --- | --- |
| 高 | `dsh-better-browser`、`dsh-ssh`、`jumpserver-dsh`、飞书桥接 | 使用隔离 Profile、最小权限凭据、主机/域名白名单与人工审批；不得将生产密钥写入仓库 |
| 中 | 搜索 Provider、视觉插件、长时记忆、自动化、费用查询 | 了解请求/图像/会话会发送到哪里；将 API Key 放入环境变量；设置预算和数据留存规则 |
| 低到中 | UI、TUI、通知、主题、知识链接 | 审核浏览器权限、客户端注入与通知内容；留意升级后兼容性 |

详细检查清单见 [docs/SECURITY.zh-CN.md](docs/SECURITY.zh-CN.md)。

## 贡献与维护

欢迎提交新增插件、兼容性报告和失效链接修复。请先阅读 [贡献指南](docs/CONTRIBUTING.zh-CN.md) 和 [维护手册](docs/MAINTENANCE.zh-CN.md)。提交一个新条目时，必须给出公开源码、精确安装方法、DSH 原生证据、许可和风险说明；仅凭 GitHub topic、DeepSeek API 支持或宣传文案的项目会进入观察名单，而不是主目录。

本仓库的插件数据为可机器读取的 [data/verified-plugins.csv](data/verified-plugins.csv)（主目录）与 [data/repositories.csv](data/repositories.csv)（全量聚合），主题页的未审核发现快照位于 [data/dsh-plugin-topic-candidates.csv](data/dsh-plugin-topic-candidates.csv)，其口径见 [数据集说明](data/README.md)。审查标准在 [data/curation-criteria.yaml](data/curation-criteria.yaml)。全量目录由 [scripts/aggregate.py](scripts/aggregate.py) 自动重建。本仓库内容以 [MIT License](LICENSE) 发布；各收录项目仍受其自身许可证约束。

## 参考资料

[1] [DeepSeek Harness Developer Preview — Everything is a plugin](https://deepseek.com/harness/en/)

[2] [DeepSeek Harness Architecture — Profiles and Bundles](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)

[3] [GitHub Topic: dsh-plugin](https://github.com/topics/dsh-plugin)

[4] [DeepSeek Harness 官方源码仓库](https://github.com/deepseek-ai/deepseek-harness)
