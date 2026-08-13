# awesome-dsh-plugins

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
![Catalog](https://img.shields.io/badge/catalog-525-2563eb)
![Verified](https://img.shields.io/badge/verified-54-16a34a)
![License](https://img.shields.io/badge/license-MIT-f59e0b)

[English](README.en.md) | **简体中文**

> 一个面向 [DeepSeek Harness（DSH）][1] 的精选插件目录。项目优先收录**可由 DSH Profile 装载**、具备可复现安装说明且源码公开的社区扩展；技能、预设与相关应用会明确区分，不把“使用 DeepSeek API”或仅贴有 `dsh-plugin` 标签的项目误当作原生插件。

DeepSeek Harness 目前处于 **Developer Preview**。官方采用 Cordis 的“Everything is a plugin”架构：Profile 组合 Bundle，外部插件通常以 `package.json` 的 `dsh` 字段及 patch 文件声明挂载方式。[1] [2] 因此，本目录中的安装方法和兼容性应在你自己的 DSH 版本上先行验证。

**快照日期：2026-08-13。** 本版收录 **51 个经源码或安装清单核验的原生 DSH 插件**与 **3 个 DSH Skill**；同时提供 **全量聚合目录 [`CATALOG.md`](CATALOG.md)（525 个仓库）**，合并了 GitHub 搜索（`topic:dsh-plugin`、`topic:deepseek-harness`、名称搜索）与多个社区目录，去重后得到。**聚合 ≠ 可装载、可兼容、可安全运行**，标签本身并不代表可安装、可维护或安全；只有 `✅` 标记的核验子集才进入本页主目录。[3]

| 导航 | 内容 |
| --- | --- |
| [全量聚合目录](#全量聚合目录) | **525 个** DSH 相关仓库的完整聚合（含未审核候选） |
| [原生插件目录](#原生-dsh-插件) | 已核验、按能力分类的可装载 Bundle、Cordis 插件与 Web Client 扩展 |
| [技能与预设](#dsh-技能与预设) | 由 DSH Skill 目录发现的可复用能力 |
| [官方内置能力](#官方内置能力不是社区插件) | 随 DSH 源码发行的官方运行时构件 |
| [相关项目与观察名单](#相关项目与观察名单不计入主目录) | 相关但并非已核验原生插件的项目 |
| [安装与安全](#安装与安全) | 安装惯例、权限提示与审计建议 |
| [贡献规则](#贡献与维护) | 新项目的提交格式与审核门槛 |

## 全量聚合目录

[`CATALOG.md`](CATALOG.md) 是自动生成的**全量聚合目录**：它把 GitHub `dsh-plugin` / `deepseek-harness` 话题、名称搜索、[`dsh-plugin` 主题页候选快照](data/dsh-plugin-topic-candidates.csv)以及多个社区目录（[bruc3van/awesome-dsh-plugin](https://github.com/bruc3van/awesome-dsh-plugin)、[Alex-Yanggg/awesome-DSH-plugin](https://github.com/Alex-Yanggg/awesome-DSH-plugin)、[awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin)、[AdamPlatin123/awesome-dsh-plugins](https://github.com/AdamPlatin123/awesome-dsh-plugins)）中发现的**全部**仓库合并去重。机器可读版本是 [`data/repositories.csv`](data/repositories.csv)。

- 聚合池是**发现清单**，不是推荐或兼容性列表；只有 `✅` 已核验子集进入下方主目录。
- 用 [scripts/aggregate.py](scripts/aggregate.py) 重新拉取并重建 `CATALOG.md` 与 `data/repositories.csv`（需要 `gh` 登录）。

## 原生 DSH 插件

下列条目已核验至少一个原生特征：可复现的 `dsh plugin` 安装命令、`dsh.bundle` / `cordis.patch.yml` 声明，或 DSH/Cordis 可挂载的 `apply` 入口。**“已核验”不代表作者、代码质量或安全性背书。**

### 视觉与多模态

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [liustack/modlens](https://github.com/liustack/modlens) | OCR、版面与语义结构化视觉证据 | `npx -y @deepseek-ai/dsh plugin --profile web add @liustack/modlens` | MIT；依赖外部视觉引擎 |
| [Scorp1o117/dsh-tool-vision](https://github.com/Scorp1o117/dsh-tool-vision) | 为 Agent 注册 `inspect_image`，调用兼容 OpenAI 的视觉模型 | 将 `dsh-tool-vision` 写入 Profile 的 `cordis.patch.yml`；见 [README](https://github.com/Scorp1o117/dsh-tool-vision/blob/main/README.md) | MIT；图像会发送至配置的视觉 API |
| [TiankunDai/dsh-vision-LMstudio](https://github.com/TiankunDai/dsh-vision-LMstudio) | 使用本地 LM Studio 视觉模型 | `dsh plugin --profile web add link:<repo>/packages/dsh-lmstudio-vision` | BSD-3-Clause；读取本地图片或剪贴板 |

### Web UI、TUI 与开发者体验

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [zhu1090093659/dsh-web-ui](https://github.com/zhu1090093659/dsh-web-ui) | Web UI 插件与皮肤合集，包括任务板、Git 图、移动端和 Token 视图 | `dsh plugin --profile web add @linxin666/dsh-web-ui-all` | BSD-3-Clause；以各子包发布状态为准 |
| [Ericwong5021/dsh-kanban](https://github.com/Ericwong5021/dsh-kanban) | DSH Web UI 任务看板 | `dsh plugin --profile <profile> add github:Ericwong5021/dsh-kanban` | MIT；早期项目，建议本地回归测试 |
| [GooodWei/context-vista](https://github.com/GooodWei/context-vista) | `/context` 上下文占用、压缩与费用视图 | `npx @deepseek-ai/dsh plugin --profile web add github:GooodWei/context-vista` | MIT；未发布稳定版本 |
| [zhaoscsc/dsh-wikilink](https://github.com/zhaoscsc/dsh-wikilink) | Obsidian 风格 `[[wikilink]]`，引用笔记到提示词 | `dsh plugin --profile web add https://github.com/zhaoscsc/dsh-wikilink/archive/refs/heads/main.tar.gz` | MIT；重装 DSH 后可能需重打补丁 |
| [omdsh-dev/dsh-open-in-vscode](https://github.com/omdsh-dev/dsh-open-in-vscode) | 从 Web UI 直接在 VS Code 打开工作区 | `dsh plugin --profile web add https://github.com/omdsh-dev/dsh-open-in-vscode/archive/refs/tags/v0.1.5.tar.gz` | MIT；会调用本机编辑器 CLI |
| [omdsh-dev/dsh-notification](https://github.com/omdsh-dev/dsh-notification) | Turn 完成时的桌面通知与规则过滤 | `dsh plugin --profile web add https://github.com/omdsh-dev/dsh-notification/archive/refs/heads/main.tar.gz` | MIT；通知可能泄露会话标题或输出摘要 |
| [openguardrails/dsh-tui](https://github.com/openguardrails/dsh-tui) | Claude Code 风格的终端 UI 与会话恢复 | `dsh plugin --profile tui add github:openguardrails/dsh-tui` | MIT；预览期 API 可能破坏兼容性 |
| [ccch1mneyyy/dsh-cc-tui](https://github.com/ccch1mneyyy/dsh-cc-tui) | 全屏终端交互、流式思考和性能仪表 | `dsh plugin --profile cc-tui add dsh-cc-tui` | BSD-3-Clause；依赖 Node.js 22.19+ |

### 搜索、浏览与知识工作流

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [gxpppp/dsh-search-mcp](https://github.com/gxpppp/dsh-search-mcp) | 用 Tavily、Brave、Exa、Perplexity、DuckDuckGo 或自定义 MCP 取代内置搜索 | `dsh plugin --profile web add link:<repo>` | MIT；查询与密钥会交由外部搜索服务 |
| [yangzhe1003/dsh-web-search-firecrawl](https://github.com/yangzhe1003/dsh-web-search-firecrawl) | Firecrawl 搜索 Provider | `dsh plugin --profile web add @yangzhe1003/dsh-web-search-firecrawl` | MIT；需要 `FIRECRAWL_API_KEY` |
| [titanwings/dsh-better-browser](https://github.com/titanwings/dsh-better-browser) | 通过 Kimi WebBridge 操作用户已登录浏览器 | `dsh plugin --profile web add github:titanwings/dsh-better-browser#v0.3.5` | BSD-3-Clause；可触及 Cookie、登录态、上传和页面操作 |

### 自动化、会话、学习与记忆

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [titanwings/dsh-automation](https://github.com/titanwings/dsh-automation) | 在全新 Agent Session 中调度 coding 任务 | `pnpm dsh plugin --profile web add /absolute/path/to/dsh-automation` | MIT；可自动执行任务，应先限制工作目录和权限 |
| [Scorp1o117/dsh-tdai-memory](https://github.com/Scorp1o117/dsh-tdai-memory) | 腾讯云 Agent Memory 的 L0–L3 长期记忆与召回 | 在 `cordis.patch.yml` 挂载 `dsh-tdai-memory`；见 [README](https://github.com/Scorp1o117/dsh-tdai-memory) | MIT；需配置 LLM、Embedding 和存储端点 |
| [TecFancy/dsh-deeptutor](https://github.com/TecFancy/dsh-deeptutor) | DeepTutor 学习、知识库与笔记归档 Bridge Bundle | `dsh plugin --profile web add dsh-deeptutor`，并按 README 加入 `dsh.profile.bundles` | MIT；依赖可用的 DeepTutor 服务 |

### 协作通信、远程执行与可观测性

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [imetn/dsh-lark-bridge](https://github.com/imetn/dsh-lark-bridge) | 飞书双向控制器 | `dsh plugin --profile lark add github:imetn/dsh-lark-bridge` | MIT；需严格配置 IM 访问边界 |
| [Roy-oss1/dsh-lark](https://github.com/Roy-oss1/dsh-lark) | 飞书机器人频道、消息回复与审批卡片 | `dsh plugin --profile web add <repo-path-or-git-url>` | BSD-3-Clause；外部 IM 可驱动具有 shell 能力的 Agent |
| [UynajGI/dsh-ssh](https://github.com/UynajGI/dsh-ssh) | SSH、SFTP、远程子进程与 PTY | 安装 `dsh-ssh` 后在 Cordis 配置中挂载 | MIT；请启用主机密钥校验并保护私钥 |
| [jumpserver-east/jumpserver-dsh](https://github.com/jumpserver-east/jumpserver-dsh) | 经 JumpServer / KoKo 的受审计远程资产操作 | `dsh plugin --profile web add github:jumpserver-east/jumpserver-dsh` | MIT；高权限远程执行，必须收紧 ACL 与 Access Key |
| [TwotwoPiggy/dsh-balance](https://github.com/TwotwoPiggy/dsh-balance) | DeepSeek 余额、会话成本和峰谷价格视图 | `dsh plugin --profile web add dsh-balance` | 未发现 SPDX 许可；会读取 API Key 查询余额 |

## 个性化、会话与内容工作流

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [Scorp1o117/dsh-soul-md](https://github.com/Scorp1o117/dsh-soul-md) | 将 `soul.md` 角色卡注入全局系统提示词并支持热重载 | 在目标 `cordis.patch.yml` 挂载 `dsh-soul-md` | MIT；影响所有 Agent 提示词，需审查角色文本 |
| [codeAnqiang-ma/dsh-superpowers](https://github.com/codeAnqiang-ma/dsh-superpowers) | 将 Superpowers 方法论技能和 Session bootstrap 接入 DSH | `dsh plugin --profile web add dsh-superpowers` | MIT；会向每次请求注入 bootstrap 提示词 |
| [hellodigua/dsh-emoji](https://github.com/hellodigua/dsh-emoji) | 自动表情呈现、素材管理和输出改写 | 按 [README](https://github.com/hellodigua/dsh-emoji) 通过固定 RC 版本安装本地 Bundle | MIT；注入提示词、改写输出并支持素材 ZIP 上传 |
| [Xilin3/dsh-prompt-persona](https://github.com/Xilin3/dsh-prompt-persona) | 从 Settings 页面编辑部署 Persona | `dsh plugin --profile web add github:xilin3/dsh-prompt-persona`，再加入 Profile bundles | MIT；可持久化和替换系统提示词 |
| [SiYue-ZO/dsh-translator](https://github.com/SiYue-ZO/dsh-translator) | 聚焦翻译工作区与原生 Session 工作流 | `dsh plugin --profile web add github:SiYue-ZO/dsh-translator` | MIT；原文会发送给当前选择的模型 |
| [YYTbit/dsh-plugin-meta-memory](https://github.com/YYTbit/dsh-plugin-meta-memory) | 本地长期记忆、索引、检索和上下文注入 | `dsh plugin --profile <profile> add dsh-plugin-meta-memory` | MIT；敏感记忆会持久化并可能进入提示词 |
| [yyh-001/dsh-companion](https://github.com/yyh-001/dsh-companion) | Persona、长期记忆与可选 QQ 通道 | `pnpm add github:yyh-001/dsh-companion`，后配置 Agent preset | MIT；可写入记忆并收发 QQ 内容 |
| [yyh-001/dsh-expression](https://github.com/yyh-001/dsh-expression) | 表情包检索与 QQ 图片发送 | `pnpm add github:yyh-001/dsh-expression`，后配置 Agent preset | MIT；经 QQ 发送真实图片，需获得发送授权 |
| [humblebanana/dsh-record-replay](https://github.com/humblebanana/dsh-record-replay) | 从 macOS 演示录制生成 Agent Skill | 构建 tarball 后运行 `dsh plugin --profile web add ./dsh-record-replay-*.tgz` | MIT；需辅助功能/输入监控权限，会记录操作细节 |
| [titanwings/dsh-plannotator](https://github.com/titanwings/dsh-plannotator) | 计划逐条批注并将结构化反馈送回 Agent | `dsh plugin --profile web add github:titanwings/dsh-plannotator#v0.1.3` | MIT；会注入对话渲染链和结构化反馈 |
| [hellodigua/dsh-share](https://github.com/hellodigua/dsh-share) | 将当前对话生成 PNG 并复制/分享 | `dsh plugin --profile web add --ignore-scripts --config.auto-install-peers=false 'github:hellodigua/dsh-share#v0.1.0'` | MIT；会读取对话 DOM 和剪贴板 |

## 扩展 UI、模型与设备工具

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [dingyi222666/dsh-session-notification](https://github.com/dingyi222666/dsh-session-notification) | 会话状态通知和自定义提示音 | `dsh plugin --profile web add @dingyi222666/dsh-session-notification` | BSD-3-Clause；需要浏览器通知权限 |
| [dingyi222666/dsh-focus-chat](https://github.com/dingyi222666/dsh-focus-chat) | 聚焦最终产出的精简会话视图 | `dsh plugin --profile web add @dingyi222666/dsh-focus-chat` | BSD-3-Clause；注入第三方 Web UI 代码 |
| [omdsh-dev/DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) | 带文件、终端、Git、子代理和浏览器的侧栏工作台 | 详见 [README](https://github.com/omdsh-dev/DSH-better-sidebar)；其安装脚本为 `curl | bash`，请先审查 | MIT；能读写文件、执行 shell 和注入工具 |
| [BruceWu1126/dsh-web-background](https://github.com/BruceWu1126/dsh-web-background) | Web UI 背景自定义 | `git clone … && node install.mjs` | MIT；安装器会修改 DSH 本地安装文件 |
| [Proton1917/dsh-live-stats](https://github.com/Proton1917/dsh-live-stats) | Token 用量、流式 TPS 与实时统计 | 以本地 link 和 `--patch` 装载；见 [README](https://github.com/Proton1917/dsh-live-stats) | BSD-3-Clause；读取会话流与 Token 投影 |
| [XYZ1024-alt/dsh-side-panel](https://github.com/XYZ1024-alt/dsh-side-panel) | 文件浏览、会话历史、Git 状态和 Diff 面板 | `dsh plugin --profile web add github:XYZ1024-alt/dsh-side-panel` | MIT；可读取本地文件并运行 Git，勿暴露到不可信网络 |
| [rainforest888/dsh-plugins-raincode](https://github.com/rainforest888/dsh-plugins-raincode) | Raincode 模型网关、缓存/重试和 `/skills` 浏览 | `npm i dsh-plugins-raincode` 后在 `cordis.yml` 注册 | MIT；提示词与工具调用会经 gateway 到远端模型 API |
| [lin-cheng-lab/dsh-plugin-doctor](https://github.com/lin-cheng-lab/dsh-plugin-doctor) | 检查插件 peer 版本与兼容性 | `dsh plugin --profile web add github:<owner>/dsh-plugin-doctor` | MIT；会访问 GitHub/npm 并读取本地 DSH 版本 |
| [1na-ko/dsh-hdc-bridge](https://github.com/1na-ko/dsh-hdc-bridge) | 鸿蒙设备截图、安装、Shell 与验证闭环 | `dsh plugin --profile <profile> add github:1na-ko/dsh-hdc-bridge` | MIT；可操作本机设备、执行设备 Shell、安装 HAP |

## 计算机使用、诊断与专项工具

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [Anionex/dsh-computer-use](https://github.com/Anionex/dsh-computer-use) | macOS 辅助功能电脑操作、截图与 Agent 工具 | `git clone https://github.com/dsh-external/dsh-computer-use.git` 后以 `dsh plugin --profile web add <path>` 装载 | MIT；可控制鼠标键盘、读取屏幕与访问设备，必须严格审批 |
| [CanglongCl/dsh-web-review](https://github.com/CanglongCl/dsh-web-review) | 网页预览、元素控制与审阅证据 | `dsh plugin --profile web add @canglongcl/dsh-web-review` | 未发现许可证；页面内容会进入 Agent 上下文，应防注入 |
| [bobleer/dsh-acp-for-bitfun](https://github.com/bobleer/dsh-acp-for-bitfun) | 通过 ACP 调度 BitFun 子代理 | `dsh plugin --profile web add dsh-acp-for-bitfun` | MIT；会管理外部 Agent 进程与权限，默认应拒绝高权限操作 |
| [chen-001/dsh-grok-tui](https://github.com/chen-001/dsh-grok-tui) | grok-build TUI 作为 DSH 前端 | `npm install -g dsh-grok-tui && grok-dsh setup` | MIT；写入 `~/.dsh` 配置并桥接模型/工作目录 |
| [csyangwen/dsh-memory-evolve](https://github.com/csyangwen/dsh-memory-evolve) | 记忆、技能、待办和外部 Agent 编排 | 目前仅给出 Web client manifest，见 [README](https://github.com/csyangwen/dsh-memory-evolve) | MIT；文件访问、提示词注入和外部 CLI/API 默认应关闭 |
| [omdsh-dev/dsh-gomoku](https://github.com/omdsh-dev/dsh-gomoku) | DSH 演示 Profile 的五子棋插件 | `dsh plugin --profile demo add github:omdsh-dev/dsh-gomoku` | MIT；会向选定模型发送内容 |
| [omdsh-dev/dsh-security-audit](https://github.com/omdsh-dev/dsh-security-audit) | 本机 DSH 配置、插件和会话的只读安全审计 | `dsh plugin --profile web add <local-path>` | MIT；会读取本地凭据元数据与会话文件，勿在参数中输入秘密 |
| [omdsh-dev/dsh-session-health](https://github.com/omdsh-dev/dsh-session-health) | 会话目录、日志与解码器健康诊断 | `dsh plugin --profile web add <local-path>` | MIT；读取 `$DSH_HOME/sessions`，应核对路径围栏 |
| [omdsh-dev/dsh-toolkit](https://github.com/omdsh-dev/dsh-toolkit) | CSV、JSON、文本等确定性数据处理工具集合 | 构建后运行 `dsh plugin --profile web add <local-path>` | MIT；需审查聚合的本地工具代码 |

## DSH 技能与预设

Skill 可由 DSH 的技能文件系统发现，但不等同于 Cordis 原生插件。这里保留它们，是因为其安装路径和调用入口已在项目中明确说明。

| 项目 | 能力 | 安装与调用 | 许可 / 风险 |
| --- | --- | --- | --- |
| [titanwings/colleague-skill](https://github.com/titanwings/colleague-skill) | 从协作工具资料蒸馏工作风格与同事 Skill | `git clone … .dsh/skills/dot-skill`，后输入 `/dot-skill` | MIT；可能处理飞书、钉钉、Slack、微信等敏感材料 |
| [titanwings/ex-skill](https://github.com/titanwings/ex-skill) | 生成关系/人物相关 Skill | `git clone … .dsh/skills/ex-skill`，后输入 `/create-ex` | MIT；会处理聊天记录，使用前须取得授权 |
| [omdsh-dev/dsh-plugin-dev](https://github.com/omdsh-dev/dsh-plugin-dev) | DSH 插件开发 Skill 与验证流程 | 将 `skills/dsh-plugin-dev` 放入 Skills 目录或在 Agent 会话中引用 | MIT；开发流程可能涉及文件、网络、进程与权限设置 |

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

随后使用项目说明中给出的 `dsh plugin --profile <profile> add …` 命令。安装前应锁定版本或 commit、阅读 `package.json`、`cordis.patch.yml` 与依赖安装脚本；不要在不了解代码的情况下执行 `curl | bash`、`pnpm` 生命周期脚本或授予系统级凭据。

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
