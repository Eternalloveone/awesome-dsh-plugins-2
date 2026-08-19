# 界面与体验 / UI & Experience

> 对应网站分类：[界面与体验 · UI & Experience](https://deepseekharnessplugins.com/plugins/category/ui-experience)

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [openma-ai/Martty](https://github.com/openma-ai/Martty) | Rust/ratatui terminal UI that renders the DeepSeek Harness agent timeline (streaming reasoning, tool calls, skills, subagents, token/cache metrics, persistent JSONL sessions, multi-image prompts) as a DSH surface plugin; extensible through Cordis plugins, themes, slots, commands and a Creator self-improvement loop | `dsh plugin --profile tui add @openma/deepseek-harness-tui@latest` | MIT；Local shell execution via `!cmd` and clipboard/image reads are user-initiated but bypass the agent sandbox; the Creator self-evolution loop can generate and load code — review any installed dynamic packages/skills |
| [alvinunreal/openpets](https://github.com/alvinunreal/openpets) | Animated desktop companion pets that react to DeepSeek Harness agent activity via a DSH Cordis plugin. | `npx -y @deepseek-ai/dsh plugin --profile web add @open-pets/dsh` | MIT；DSH install path not yet documented in root README; confirm `npx -y @deepseek-ai/dsh plugin --profile web add @open-pets/dsh` before publishing. Integrates with local desktop process over IPC. |
| [UNLINEARITY/dsh-code](https://github.com/UNLINEARITY/dsh-code) | Claude-Code/Codex 风格的 DSH 终端编码界面（树外 bundle 叠于 @deepseek-ai/dsh-base）：斜杠命令、会话恢复、模型/权限管理、审批条与 plan/goal 模式 | `dsh plugin --profile cli add dsh-code@0.8.0；启动命令 deepseek / dsh --profile cli / dsh-code` | MIT；TUI 内 /model 可管理与轮换 API key、读写工作区，依赖 DSH 权限预设与 sandbox 审批机制 |
| [wssfk12138/dsh-damage-pulse](https://github.com/wssfk12138/dsh-damage-pulse) | Game-style token-usage / balance damage-pulse visualization for DeepSeek/DSH. | `Copy plugins/dsh-token-monitor/ and packages/client/ui-token-monitor/ into a local DSH repo; mount via cordis.patch.yml: node --import tsx/esm apps/cli/src/bin.ts web --patch <dsh-root>/plugins/dsh-token-monitor/cordis.patch.yml --port 3080` | MIT；Install is drop-into-DSH-repo + patch, not a standalone dsh plugin add. Reads DEEPSEEK_API_KEY and polls DeepSeek balance (external API); modifies DSH ui-workspace files (filesystem writes). |
| [Aisland-SJL/dsh-reminder](https://github.com/Aisland-SJL/dsh-reminder) | Cross-window completion/approval notification popups for the DSH web GUI. | `npx -y @deepseek-ai/dsh plugin --profile web add dsh-reminder` | MIT；Brand-new (1-day-old, ~12 stars); npm publish of dsh-reminder not independently confirmed. Read-only (reminds, never acts), no external network calls or privileged creds. |
| [boxeryao/deepseek-harness-tui](https://github.com/boxeryao/deepseek-harness-tui) | DSH-TUI: lightweight, fast terminal UI plugin hooked into DSH's agent, tools, permission and session services; line-oriented interface (no card layouts); does not re-implement the harness runtime. | `dsh plugin --profile tui add .   (after pnpm install && pnpm run build; requires pnpm 11+ and DSH 0.1.0-rc.6)` | MIT |
| [ccch1mneyyy/dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) | Claude Code 风格全屏终端 TUI：像素鲸鱼顶栏、双流光大字、实时工作状态行、思考流式展开、双击 Esc 时间回溯、上下文进度条 + TPS 仪表；接入 Agent preset（standard/code/minimal/cordis）、Skills、MCP、Goals、Todos、子代理，/ 命令注册表与随附技能（audit/bug/review/practice/pr_comments/release-notes/vuln-check）；纯插件挂载零核心改动。 | `dsh plugin --profile cc-tui add dsh-cc-tui（仓库根目录 install.sh 已封装含 pnpm 预检；前置 npm install -g @deepseek-ai/dsh；Windows 用 dsh-cc.cmd --resume）` | MIT；功能面大（含 MCP 与 Shell 类工具），授予前确认会话信任边界；依赖可用 TTY。 |
| [dsh-tui/dsh-tui](https://github.com/dsh-tui/dsh-tui) | 终端 UI (terminal TUI): Claude Code 风格的 dsh 终端界面，复用官方 dsh-base 全部生态（shell/文件工具、技能、子代理、workflows、沙箱审批）；pi-tui 0.80.7 已打补丁并内联。 | `npm i -g @deepseek-ai/dsh@next;  dsh plugin --profile tui add @dsh-tui/dsh-tui   (requires Node ^22.19 \|\| >=24)` | MIT；Repackaged from recovered upstream UI code; peer deps pin a pre-release dsh rc. |
| [lanshuye123/DSH-Terminal](https://github.com/lanshuye123/DSH-Terminal) | VSCode 风格终端模拟器+文件管理器：宿主机真实 PTY（subprocess.spawnTerminal/node-pty）、多会话、自研 ANSI 渲染、工作区目录树+预览 | `动态部署：git clone 后 node scripts/build-payload.js 产出 dist/ 载荷，按 BOOTSTRAP.md 让 DSH Agent 用 cordis_define 提交 + cordis_run 激活（更新用 kind:existing）` | MIT；无 CLI 导入通道、依赖 DSH dynamic-plugin 会话与 node-pty 私有细节，DSH 升级需回归。 |
| [liuup/dsh-latex-tools](https://github.com/liuup/dsh-latex-tools) | 在 DeepSeek Harness 中悬停任意 LaTeX 公式即可复制 TeX 源码或导出独立 SVG 文件；MathJax 由插件自身 host half 提供，首次按需加载后浏览器缓存，完全离线。 | `npx @deepseek-ai/dsh plugin --profile web add dsh-latex-tools （或 github:liuup/dsh-latex-tools）；验证 npx @deepseek-ai/dsh --profile web --dump-config 出现 '# == dsh-latex-tools' 层` | MIT |
| [realchenwenqiao/dash](https://github.com/realchenwenqiao/dash) | 终端的 agent 前端：复用 dsh-base 内核（Cordis/agent loop/工具/会话），pi-tui 界面 + 行为账本 + 内置技能命令 / Terminal-native DSH frontend (pi-tui) reusing the dsh-base agent stack. | `npm install -g @deepseek-ai/dsh && dsh plugin --profile tui add @realchenwenqiao/dash` | 未发现；No license declared. |
| [realguan/dsh-mermaid-preview](https://github.com/realguan/dsh-mermaid-preview) | 把 Markdown 的 mermaid 围栏代码块在 dsh Web 界面渲染为图表（客户端动态插件/原生 bundle 两种形态）/ Renders mermaid fenced code blocks as diagrams in the dsh web chat. | `dsh plugin --profile web add github:realguan/dsh-mermaid-preview` | MIT |
| [songqikong/dash](https://github.com/songqikong/dash) | 终端 TUI 客户端（oh-my-pi 键位 + DSH 完整 agent 内核）：/plan /goal /compact、模型角色体系、会话持久化、raw-ANSI 渲染 | `git clone https://github.com/songqikong/dash.git && cd dash && sh install.sh（创建 ~/.dsh/profiles/dash + ~/.local/bin/dash）；启动: dash` | MIT；默认全权限无审批，谨慎在不可信环境使用 |
| [xiaoshihou514/dsh-tui](https://github.com/xiaoshihou514/dsh-tui) | DSH 终端 TUI：覆在 Harness base bundle 上的交互式终端界面；tui-startup 负责 CLI 解析、tui-runtime 持有根 agent 与终端生命周期，接入 code-runtime（worker-thread）。 | `dsh plugin --profile web add dsh-tui（或本地 pnpm install && pnpm build 后 dsh plugin --profile web add <repo路径>）` | MIT；ALPHA 阶段（readme 提示 stay tuned）；TUI 直接操作根 agent 与代码运行时。 |
| [PerryLink/dsh-output-styles](https://github.com/PerryLink/dsh-output-styles) | Session-scoped, durable, runtime-switchable model output styles: /style command, output_style storage domain, systemPrompt injection; stylesDir config ('' = bundled styles/). | dsh plugin --profile <name> add dsh-output-styles (then add `name: 'dsh-output-styles'` row to the profile cordis.patch.yml) | Apache-2.0 |
| [rabbitknight/dsh-tui](https://github.com/rabbitknight/dsh-tui) | 基于 dsh-base 的交互式终端界面（dsh --profile tui），含 /skills 技能目录 / Interactive terminal UI bundle for dsh running on dsh-base. | `dsh plugin --profile tui add "<path>/packages/dsh-tui-app" (or npx @deepseek-ai/dsh plugin --profile tui add ...), then npx @deepseek-ai/dsh --profile tui` | 未发现；No license declared. |
| [ZgblKylin/dsh-terminal](https://github.com/ZgblKylin/dsh-terminal) | VSCode 风格内置终端面板：xterm.js（浏览器端）+ node-pty（宿主端）实现的独立 dsh 插件，随桌面外壳（dsh-gui）在 web 组合中运行。 | `pnpm install && pnpm run build；dsh plugin --profile web add link:./plugins/terminal，再在 .dsh/profiles/web/cordis.patch.yml 加一行 name: dsh-terminal 并重启外壳；README 要求用仓库固定 .toolchain pnpm（11.7.0）` | Unlicense；文档针对个人 dsh-gui 工程（E:/Git/dsh-gui）编写，安装路径带环境耦合；终端权限面高，谨慎开放。 |
| [13071301808/dsh-composer-expand](https://github.com/13071301808/dsh-composer-expand) | DSH 输入框展开 UI 插件。 | `` | MIT |
| [147228/dsh-black-whale](https://github.com/147228/dsh-black-whale) | DSH 主题/皮肤插件（黑鲸皮肤），修改 Web UI 外观。 | `` | N/A |
| [147228/dsh-xiaoyao-skins](https://github.com/147228/dsh-xiaoyao-skins) | DSH 逍遥皮肤包，提供多套 Web UI 主题。 | `` | N/A |
| [1841220388zzzcccxxx-star/dsh-git-graph](https://github.com/1841220388zzzcccxxx-star/dsh-git-graph) | Embedded git graph visualizer for DSH web GUI (history, diff, branch ops). | `` | MIT |
| [2768651338/dsh-plugin-manager](https://github.com/2768651338/dsh-plugin-manager) | 图形化插件管理标签页 | `` | MIT |
| [a903067276-rgb/dsh-file-mentions](https://github.com/a903067276-rgb/dsh-file-mentions) | DSH 文件提及/引用展示 UI 插件。 | `` | MIT |
| [aaravarr/dsh-subagent-max](https://github.com/aaravarr/dsh-subagent-max) | subagent_with_model tool plus a live multi-panel subagent viewer for DSH. | `` | MIT |
| [Abyss-Seeker/dsh-plugin-working-status](https://github.com/Abyss-Seeker/dsh-plugin-working-status) | DSH 轻量插件：点击即改「Deep diving...」状态文字，全局持久化 | `` | N/A |
| [aceice01/dsh-whale-pet](https://github.com/aceice01/dsh-whale-pet) | 鲸鱼娘桌宠 | `` | Non-Commercial |
| [AcidGr/dsh-web-mobile-fix](https://github.com/AcidGr/dsh-web-mobile-fix) | DSH Web 移动端适配修复插件，优化小屏布局。 | `` | MIT |
| [AdamPlatin123/dsh-tonghuashun](https://github.com/AdamPlatin123/dsh-tonghuashun) | 同花顺 (THS) terminal-style skin + code-volume K-line market panel (packages ui-skin-ths + ui-market). | `cordis.patch.yml: - id: ui-skin-ths (name '@deepseek-ai/dsh-client-ui-skin-ths'), - id: ui-market (name '@deepseek-ai/dsh-client-ui-market')` | MIT；Client UI skin + market display panel only; no network or API keys; settings registered to settings.general.item slot. |
| [Aisland-SJL/dsh-usage](https://github.com/Aisland-SJL/dsh-usage) | Persistent balance/usage dock + heatmap for DSH web GUI. | `` | MIT |
| [AKS1st/dsh-cyber-particle](https://github.com/AKS1st/dsh-cyber-particle) | DSH 赛博粒子动效/主题插件，增强界面视觉效果。 | `` | MIT |
| [AKS1st/model-usage-plugin](https://github.com/AKS1st/model-usage-plugin) | 模型消耗统计 (musage-stats) | `` | MIT |
| [AngelosZou/dsh-multi-folder](https://github.com/AngelosZou/dsh-multi-folder) | 主工作区多次级目录 | `` | MIT |
| [asukasec/dsh-message-preview](https://github.com/asukasec/dsh-message-preview) | DSH 消息预览 UI 扩展。 | `` | MIT |
| [badai147/dsh-global-rules](https://github.com/badai147/dsh-global-rules) | Edit ~/.dsh/AGENTS.md global rules from DSH web settings panel. | `` | MIT |
| [baihejiangnan/dsh-session-context-menu](https://github.com/baihejiangnan/dsh-session-context-menu) | 更好的右键菜单 | `` | MIT |
| [bearllfleed/Dsh-FileExplorer](https://github.com/bearllfleed/Dsh-FileExplorer) | VS Code 风格文件浏览器+编辑器 | `` | MIT |
| [better-er/dsh-tool-autoexpand](https://github.com/better-er/dsh-tool-autoexpand) | 工具结果自动展开 | `` | MIT |
| [bobcat848/dsh-calculator](https://github.com/bobcat848/dsh-calculator) | Floating card showing DeepSeek API spend and live account balance in the DSH web GUI. | `` | MIT |
| [boxeryao/dsh-mini-tui](https://github.com/boxeryao/dsh-mini-tui) | DSH 极简终端 UI 插件（answer-first 工具输出 / 后台执行 / Windows 右键菜单） | `` | MIT |
| [buhuikongpan/dsh-pluginmanager](https://github.com/buhuikongpan/dsh-pluginmanager) | DSH Web 设置页插件管理器（三层架构视图 / 启停 / 卸载 / 补登记） | `` | MIT |
| [c-ling/dsh-plugin-pet](https://github.com/c-ling/dsh-plugin-pet) | Desktop e-pet in the DSH Web GUI reacting to agent state with built-in/custom/Codex sprite support. | `` | MIT |
| [caoyiwei850/dsh-client-ui-skins](https://github.com/caoyiwei850/dsh-client-ui-skins) | DSH 客户端 UI 皮肤/主题插件。 | `` | MIT |
| [Cassius0924/dsh-usage-dashboard](https://github.com/Cassius0924/dsh-usage-dashboard) | DSH 使用量/统计仪表盘插件，展示 token 与调用数据。 | `` | MIT |
| [charrywhite/dsh-sticky-notes](https://github.com/charrywhite/dsh-sticky-notes) | DSH 便签插件：可拖拽、文字/图片便签、9 款皮肤、AI 可读写。 | `` | MIT |
| [chi-hong22/dsh-mdbox](https://github.com/chi-hong22/dsh-mdbox) | DSH  Markdown 盒子插件，在 UI 中渲染/编辑 Markdown。 | `` | N/A |
| [cindyguyuehu123/dsh-mobile](https://github.com/cindyguyuehu123/dsh-mobile) | DSH 移动端界面适配插件。 | `` | MIT |
| [cindyguyuehu123/dsh-webchatlike](https://github.com/cindyguyuehu123/dsh-webchatlike) | DSH 仿网页聊天界面 UI 插件。 | `` | MIT |
| [Civitasv/dsh-plugin-diff-review](https://github.com/Civitasv/dsh-plugin-diff-review) | DSH Codex 风格 diff 评审 UI 插件。 | `` | MIT |
| [CocoSgt/dsh-attachments](https://github.com/CocoSgt/dsh-attachments) | DSH 第三方附件插件（统一文件暂存网关，任意类型零拒收） | `` | MIT |
| [CocoSgt/dsh-inspector](https://github.com/CocoSgt/dsh-inspector) | DSH 检查器/调试 UI 插件。 | `` | MIT |
| [culture-flask/dsh-aemeath-pet](https://github.com/culture-flask/dsh-aemeath-pet) | 像素风桌宠 | `` | Apache-2.0 |
| [Dasooul03/dsh-plugin-deepseek-pricing](https://github.com/Dasooul03/dsh-plugin-deepseek-pricing) | DSH DeepSeek 计费/价格展示插件。 | `` | MIT |
| [Dbi-Eshuh/dsh-thinking-status-customizer](https://github.com/Dbi-Eshuh/dsh-thinking-status-customizer) | DSH 思考状态（thinking status）自定义 UI 插件。 | `` | MIT |
| [dclichang2022/dsh-green-meter](https://github.com/dclichang2022/dsh-green-meter) | Energy/carbon/cost metering for DSH from token accounting. | `` | MIT |
| [dfkai/dsh-board](https://github.com/dfkai/dsh-board) | DSH 看板/面板插件，提供可视化信息板。 | `` | MIT |
| [Dpf555/dsh-workbench](https://github.com/Dpf555/dsh-workbench) | DSH 工作台插件，提供集成化的工具面板 UI。 | `` | MIT |
| [dream12347/dsh-session-manager](https://github.com/dream12347/dsh-session-manager) | DSH 会话管理器 UI 插件。 | `` | MIT |
| [DViridescent/dafy-whale-theme](https://github.com/DViridescent/dafy-whale-theme) | DSH 鲸鱼主题/皮肤插件。 | `` | MIT |
| [e2mcc/dsh-popout-sidebar](https://github.com/e2mcc/dsh-popout-sidebar) | DSH 侧边栏弹出（popout）UI 插件。 | `` | MIT |
| [elviszhang007/dsh-moyan](https://github.com/elviszhang007/dsh-moyan) | DSH 墨言：侧边栏名言/古诗词/游戏台词展示插件，语料可外置自定义。 | `` | MIT |
| [enchangcui340-cloud/dsh-whale-balance](https://github.com/enchangcui340-cloud/dsh-whale-balance) | DSH 鲸鱼余额展示 UI 插件。 | `` | MIT |
| [eric-song-dev/dsh-ikun-pet](https://github.com/eric-song-dev/dsh-ikun-pet) | DSH 坤宠动画进度插件（deep dive 状态行下方进度条 + 完成音效） | `` | MIT |
| [Ericwong5021/dsh-taskboard](https://github.com/Ericwong5021/dsh-taskboard) | DSH Web UI 任务看板插件（仓库原名为 dsh-taskboard，后重命名为 dsh-kanban）。 | `` | MIT |
| [euuuuuuzer/dsh-loop-dock](https://github.com/euuuuuuzer/dsh-loop-dock) | DSH 循环/任务停靠栏（dock）UI 扩展。 | `` | MIT |
| [f0909172434/dsh-deepseek-girl-pet](https://github.com/f0909172434/dsh-deepseek-girl-pet) | deepseek 娘桌宠 | `` | MIT |
| [fengzhiyushui/dsh-desktop-window](https://github.com/fengzhiyushui/dsh-desktop-window) | DSH 独立应用窗口插件，以 --app 模式弹出隔离的桌面窗口。 | `` | MIT |
| [gameswu/dsh-notifacation-frame](https://github.com/gameswu/dsh-notifacation-frame) | Notification framework letting derivative plugins register notifiers with config cards in Settings. | `` | MIT |
| [gameswu/dsh-plugin-vscode-sidebar](https://github.com/gameswu/dsh-plugin-vscode-sidebar) | DSH 的 VS Code 风格侧边栏插件，扩展编辑器侧栏 UI。 | `` | MIT |
| [gameswu/dsh-pref-kit](https://github.com/gameswu/dsh-pref-kit) | DSH 偏好/设置工具包 UI 插件。 | `` | MIT |
| [Gin-7/dsh-pet-remielle](https://github.com/Gin-7/dsh-pet-remielle) | Zenless Zone Zero 'Remielle' desktop-pet skin for DSH web GUI. | `` | MIT |
| [GLFzr/dsh-file-upload](https://github.com/GLFzr/dsh-file-upload) | DSH 文件上传 UI 插件。 | `` | MIT |
| [GLFzr/dsh-opencode-go-quota](https://github.com/GLFzr/dsh-opencode-go-quota) | DSH opencode Go 配额展示插件，显示额度使用情况。 | `` | MIT |
| [gxinxing/deepseek-harness-tui](https://github.com/gxinxing/deepseek-harness-tui) | Interactive terminal chat UI (Ink/React) for DeepSeek Harness — folded tool calls, thinking folding, and OSC-11 adaptive theme. | `dsh plugin --profile tui add /path/to/deepseek-harness-tui` | MIT；TUI/UI only; routes llm-deepseek through the TokenDance gateway (needs TOKENDANCE_API_KEY) and requires a one-time manual runtime patch to the harness llm-deepseek adapter (lost on upgrade). |
| [haxi8/dsh-JujutsuKaisen-rainlove](https://github.com/haxi8/dsh-JujutsuKaisen-rainlove) | DSH 主题/趣味装饰插件（动漫主题）。 | `` | MIT |
| [Highjobop/dsh-gadgets](https://github.com/Highjobop/dsh-gadgets) | DSH 轻量合集：dsh-skin 外观、dsh-tidy 对话整理、dsh-task-alerts 任务提醒。 | `` | MIT |
| [Hilbert-beinghappy/seektty](https://github.com/Hilbert-beinghappy/seektty) | 可插拔 DeepSeek 风格终端 TUI 插件（dsh --profile tui，会话/主题/中英界面） | `` | N/A |
| [HongMing-Huang/dsh-file-upload](https://github.com/HongMing-Huang/dsh-file-upload) | DSH 文件消息插件：拖拽/回形针上传、文档转 Markdown(MarkItDown)、图片 OCR、语音输入、read_document 工具。 | `` | MIT |
| [Hotsteel2901/dsh-client-ui-mobile-adapt](https://github.com/Hotsteel2901/dsh-client-ui-mobile-adapt) | DSH Web 移动端适配客户端插件（Termux/手机单栏布局、抽屉、全屏面板） | `` | MIT |
| [HR2AY/DSH-Plan-Graph](https://github.com/HR2AY/DSH-Plan-Graph) | DSH 会话工具调用/消息交互式流程图插件（Plan Graph 标签、收藏、定位） | `` | MIT |
| [huahai0202/dsh-better-archive](https://github.com/huahai0202/dsh-better-archive) | DSH 会话归档改进 UI 插件。 | `` | MIT |
| [huanyuLv/dsh-balance-tide](https://github.com/huanyuLv/dsh-balance-tide) | DSH 余额趋势展示 UI 插件。 | `` | MIT |
| [huguangyu666/dsh-plugin-notify](https://github.com/huguangyu666/dsh-plugin-notify) | Notification outlet: desktop toast / Chinese voice broadcast / sound so the agent can proactively reach the user. | `` | MIT |
| [huiliyi37/dsh-tianshu-tui](https://github.com/huiliyi37/dsh-tianshu-tui) | DeepSeek Harness 交互式终端 UI 插件：会话工作区、图片端到端（剪贴板/视觉桥）、slash 下拉、审批卡片、推理可视化，纯展示层 | `npx -y @deepseek-ai/dsh plugin --profile tui add @huiliyi37/dsh-tianshu-tui` | Apache-2.0；UI 纯展示层，不注册 prompt/工具/上下文面，所有状态派生自会话事件流；无网络/凭据/文件访问 |
| [hxyz486/dsh-archived-conversations](https://github.com/hxyz486/dsh-archived-conversations) | DSH 归档会话浏览 UI 插件。 | `` | MIT |
| [iyllyt/dsh-btw](https://github.com/iyllyt/dsh-btw) | DSH 旁注/批注(btw)交互 UI 插件。 | `` | MIT |
| [jesse-njx/dsh-voice](https://github.com/jesse-njx/dsh-voice) | DSH 语音输入/输出插件。 | `` | MIT |
| [jjxjjjjiik-bot/dsh-chat-timeline](https://github.com/jjxjjjjiik-bot/dsh-chat-timeline) | 1:1 复刻 DeepSeek 官网右侧对话导航栏的 DSH 插件 | `` | MIT |
| [JuneLearn/dsh-reasoning-settings](https://github.com/JuneLearn/dsh-reasoning-settings) | 推理强度设置 | `` | MIT |
| [kaziii/dsh-github-connector](https://github.com/kaziii/dsh-github-connector) | GitHub 连接器（PR 状态条） | `` | MIT |
| [kc0ed/dsh-bottom-bar](https://github.com/kc0ed/dsh-bottom-bar) | DSH 底部状态栏/工具栏插件，扩展界面底部 UI。 | `` | MIT |
| [KeLearns/dsh-navigation-bar](https://github.com/KeLearns/dsh-navigation-bar) | DSH 导航栏插件，扩展界面顶部/侧边导航。 | `` | MIT |
| [LAN-TINA-WS/dsh-gui-customization](https://github.com/LAN-TINA-WS/dsh-gui-customization) | DSH web GUI theme customizer (colors, ambiance light, dynamic backgrounds). | `` | MIT |
| [Lanxing6480/dsh-galgame](https://github.com/Lanxing6480/dsh-galgame) | DSH Web 聊天界面 GalGame 模式插件（立绘 + 思考气泡 + 打字机，纯视觉层） | `` | MIT |
| [le-soleil-se-couche/dsh-token-cost](https://github.com/le-soleil-se-couche/dsh-token-cost) | DSH token 成本统计插件，展示消耗与费用。 | `` | MIT |
| [leavestring/awesome-dsh-background-plugin](https://github.com/leavestring/awesome-dsh-background-plugin) | DSH Web 背景个性化插件（上传图片/预设）。 | `` | MIT |
| [left0ver/dsh-file-review](https://github.com/left0ver/dsh-file-review) | Diff/review panel for files an agent just changed in DSH web, with undo. | `` | N/A |
| [LemCAE/dsh-balance](https://github.com/LemCAE/dsh-balance) | DSH 余额/配额展示插件，显示账户余额信息。 | `` | MIT |
| [LiangYin233/dsh-provider-model-configurator](https://github.com/LiangYin233/dsh-provider-model-configurator) | DSH web UI model configurator (provider model entries, thinking levels). | `` | MIT |
| [liliuCourier/dsh-chat-outline](https://github.com/liliuCourier/dsh-chat-outline) | Persistent left-side chat outline listing each question and its last reply with one-click jump. | `` | MIT |
| [LingyeSoul/dsh-tavern](https://github.com/LingyeSoul/dsh-tavern) | DSH 的酒馆式（SillyTavern 风格）聊天前端插件，提供多角色对话界面。 | `` | MIT |
| [linshule/dsh-balance](https://github.com/linshule/dsh-balance) | DSH 余额展示插件，显示账户/额度信息。 | `` | MIT |
| [lj970926/dsh-plugin-mermaid](https://github.com/lj970926/dsh-plugin-mermaid) | Renders mermaid code blocks in chat with a chart/source toggle and live theme switching. | `` | MIT |
| [LJninse/dsh-open-in-ide](https://github.com/LJninse/dsh-open-in-ide) | DSH 在 IDE 中打开文件的交互插件。 | `` | CC BY-NC 4.0 |
| [loguhan/dsh-workshop](https://github.com/loguhan/dsh-workshop) | DSH workshop / 学习与演示向插件，提供 Web UI 扩展。 | `` | MIT |
| [lssyd20070106/dsh-ui-preset-enhance](https://github.com/lssyd20070106/dsh-ui-preset-enhance) | DSH WebUI 增强插件（背景/主题自定义 / Prompt 预设 / Token 查看 / 手动 Compact） | `` | MIT |
| [lzbaclz/dsh-conversation-outline](https://github.com/lzbaclz/dsh-conversation-outline) | 对话大纲侧栏 | `` | MIT |
| [magian1127/deepseek-harness-zh_pro](https://github.com/magian1127/deepseek-harness-zh_pro) | DSH 专业中文本地化/增强 UI 插件。 | `` | MIT |
| [Max-Samson/dsh-usage-chart](https://github.com/Max-Samson/dsh-usage-chart) | DSH 用量图表 UI 插件。 | `` | MIT |
| [maydaytyh/dshx-terminal](https://github.com/maydaytyh/dshx-terminal) | DSHx 终端界面插件。 | `` | MIT |
| [mengyun233/dsh-codex-pet](https://github.com/mengyun233/dsh-codex-pet) | Codex 桌宠迁移插件 | `` | MIT |
| [Mombrane/dsh-subagent-monitor](https://github.com/Mombrane/dsh-subagent-monitor) | Realtime subagent run-monitor panel for DSH web GUI. | `` | MIT |
| [monk233/dsh-plugin-manager](https://github.com/monk233/dsh-plugin-manager) | 插件管理（启用/禁用/删除） | `` | MIT |
| [Mooling0602/dsh-web-file-uploader](https://github.com/Mooling0602/dsh-web-file-uploader) | DSH Web 文件上传插件（模型感知注入 / SHA-256 去重 / 内容寻址） | `` | MIT |
| [Nanki-nn/dsh-answer-pet](https://github.com/Nanki-nn/dsh-answer-pet) | DSH Web 可扩展回答状态宠物框架（进度/模型轨迹卡，多会话并发） | `` | MIT |
| [NanmiCoder/dsh-plugin-market](https://github.com/NanmiCoder/dsh-plugin-market) | DSH 插件市场插件，提供插件浏览与安装界面。 | `` | MIT |
| [nextindie/deepseek-harness-for-vs-code](https://github.com/nextindie/deepseek-harness-for-vs-code) | VS Code 内 DSH 集成（含 dsh-git-rollback bundle）。 | `` | MIT |
| [No-PRM/dsh-explorer](https://github.com/No-PRM/dsh-explorer) | VS Code 风格文件树浏览器 | `` | MIT |
| [NoNameLeGo/dsh-catppuccin-theme](https://github.com/NoNameLeGo/dsh-catppuccin-theme) | Catppuccin theme plugin for DSH web GUI (4 flavours + glassmorphism). | `` | MIT |
| [noone89A/dsh-gauge](https://github.com/noone89A/dsh-gauge) | Precise cache-hit rate, token usage and cost estimates replacing the native DSH stats line. | `` | MIT |
| [OK-wx/dsh-ocgo-lite](https://github.com/OK-wx/dsh-ocgo-lite) | OpenCode Go 用量常驻条 | `` | MIT |
| [openma-ai/deepseek-harness-tui](https://github.com/openma-ai/deepseek-harness-tui) | DeepSeek Harness 终端 UI（TUI）。 | `` | MIT |
| [orriduck/dsh-tui](https://github.com/orriduck/dsh-tui) | Session-aware terminal UI for DeepSeek Harness (start/continue/resume sessions, permission-preset switching). | `npm install -g github:orriduck/dsh-tui` | MIT；Terminal UI driving DSH sessions; can switch permission preset incl. typed FULL ACCESS confirmation; optional Herdr bridge. |
| [PAKIKNOWLEDGE/dsh-client-ui-skin-claude](https://github.com/PAKIKNOWLEDGE/dsh-client-ui-skin-claude) | Claude 风格皮肤 | `` | MIT |
| [penguin-oo/dsh-bookmarks](https://github.com/penguin-oo/dsh-bookmarks) | DSH Web 回复书签插件（笔记/标签 / 跨会话中心 / 一键 Markdown 导出） | `` | MIT |
| [pitetow/dsh-notify-on-complete](https://github.com/pitetow/dsh-notify-on-complete) | Zero-dependency desktop notifications when a run finishes, the model asks a question, or approval is pending. | `` | MIT |
| [Player-MINEPIG/dsh-tavern](https://github.com/Player-MINEPIG/dsh-tavern) | DSH 酒馆式对话 UI 主题/界面插件。 | `` | MIT |
| [poplarity/dsh-science-workbench](https://github.com/poplarity/dsh-science-workbench) | 可复现科学工作台 | `` | MIT |
| [qing3a/dsh-event-auditor](https://github.com/qing3a/dsh-event-auditor) | DSH 事件审计/日志可视化插件 | `` | MIT |
| [QJAG1024/dsh-model-meta-autofill](https://github.com/QJAG1024/dsh-model-meta-autofill) | Auto-fills metadata (context window, output cap, display name, modalities) for custom-provider models from models.dev. | `` | MIT |
| [qjcnmd/dsh-reasoning-slider](https://github.com/qjcnmd/dsh-reasoning-slider) | DSH 推理强度（reasoning effort）滑块 UI 控件。 | `` | MIT |
| [R3alloc/dsh-session-deeplink](https://github.com/R3alloc/dsh-session-deeplink) | DSH 会话深度链接插件，支持通过链接直达特定会话。 | `` | MIT |
| [RealAlexandreAI/dsh-atuin](https://github.com/RealAlexandreAI/dsh-atuin) | Records every typed DSH prompt into atuin shell history (searchable via `atuin search`). | `dsh plugin --profile web add dsh-atuin` | MIT；Spawns the `atuin` binary as a subprocess and writes typed prompts into local atuin history DB; may capture sensitive input unless deny rules are set. No network exfiltration. |
| [rongzi5/dsh-whale-pet](https://github.com/rongzi5/dsh-whale-pet) | 3D 鲸鱼桌宠 | `` | N/A |
| [sanshanya/better-model-provider](https://github.com/sanshanya/better-model-provider) | Declarative settings page for per-model native vision input, reasoning level and token capacity in DSH. | `` | MIT |
| [schhaohao/dsh-file-explorer](https://github.com/schhaohao/dsh-file-explorer) | DSH 文件浏览器 UI 插件 | `` | MIT |
| [Scorp1o117/dsh-plugin-marketplace](https://github.com/Scorp1o117/dsh-plugin-marketplace) | DSH 插件市场 UI | `` | MIT |
| [SherUnlocked-4869/dsh-plugin-msg-nav](https://github.com/SherUnlocked-4869/dsh-plugin-msg-nav) | DSH 消息导航插件，提供会话内消息跳转/索引 UI。 | `` | MIT |
| [silencieuxzero/Better_Deepseek_Harness](https://github.com/silencieuxzero/Better_Deepseek_Harness) | Extension center UI for DSH managing skills/plugins/MCP with native settings integration. | `` | N/A |
| [skr311/dsh-codex-pet](https://github.com/skr311/dsh-codex-pet) | Codex 桌宠 | `` | MIT |
| [songoao25/dsh-bottom-info-bar](https://github.com/songoao25/dsh-bottom-info-bar) | DSH Web UI 底部信息栏扩展。 | `` | MIT |
| [SpookySandwich/dsh-plugin-smooth-stream](https://github.com/SpookySandwich/dsh-plugin-smooth-stream) | DSH 流式文字动画增强插件（淡入 + 平滑流式跟随） | `` | MIT |
| [springbrand-lab/dsh-skin-universe](https://github.com/springbrand-lab/dsh-skin-universe) | DSH 皮肤宇宙插件，提供多套界面主题切换。 | `` | MIT |
| [starslittle/dsh-blue-whale](https://github.com/starslittle/dsh-blue-whale) | DSH 蓝鲸主题/状态展示 UI 插件。 | `` | MIT |
| [stevenx65/dsh-balance-plugin](https://github.com/stevenx65/dsh-balance-plugin) | DSH 余额查询展示 UI 插件。 | `` | MIT |
| [Suiwan/whale-purse](https://github.com/Suiwan/whale-purse) | DSH 账户/余额钱包展示 UI 插件。 | `` | MIT |
| [taxueseek/dsh-files](https://github.com/taxueseek/dsh-files) | DSH 双面文件插件（会话隔离上传 + read_document 文档读取，内容嗅探） | `` | MIT |
| [TheTianzz/dsh-billing](https://github.com/TheTianzz/dsh-billing) | DSH 余额/账单可视化插件，提供用量与费用面板。 | `` | MIT |
| [tianyhjg-lab/dsh-font](https://github.com/tianyhjg-lab/dsh-font) | DSH 字体/显示主题调整插件。 | `` | N/A |
| [Tianyu209/dsh-browser-companion](https://github.com/Tianyu209/dsh-browser-companion) | Persistent visible browser for the agent with human-in-the-loop login, cookies and safe browser tools. | `` | MIT |
| [Tkingxiao/dsh-any-background](https://github.com/Tkingxiao/dsh-any-background) | DSH 自定义主题与壁纸插件（色轮选色 / 背景图 / 透明度模糊 / 文件系统持久化） | `` | MIT |
| [tomowang/dsh-tui](https://github.com/tomowang/dsh-tui) | Out-of-tree terminal (TUI) front door for DSH built on React + Ink, an alternative to dsh-web-app. | `` | MIT |
| [tsonglew/dsh-workspace-search](https://github.com/tsonglew/dsh-workspace-search) | DSH 工作区关键词搜索标签页插件，扩展 dsh-better-sidebar。 | `` | MIT |
| [turtle1999/turtle-ui](https://github.com/turtle1999/turtle-ui) | Former packages/ui/tui terminal UI as a dsh profile bundle (durable session TUI, --resume/--session). | `dsh plugin --profile tui add file:.` | BSD-3-Clause；Terminal UI for DSH driving one durable session; no network/keys beyond DSH itself. |
| [urzeye/dsh-outline](https://github.com/urzeye/dsh-outline) | Realtime conversation outline tree for DSH web GUI. | `` | MIT |
| [Vim0x3c/dsh-session-manager](https://github.com/Vim0x3c/dsh-session-manager) | DSH 会话管理器 UI 插件（Vim0x3c 版）。 | `` | MIT |
| [Vim0x3c/dsh-skin-appearance](https://github.com/Vim0x3c/dsh-skin-appearance) | 外观定制（八套主题+壁纸） | `` | MIT |
| [wangxiang0605qvq/dsh-deepseek-balance](https://github.com/wangxiang0605qvq/dsh-deepseek-balance) | DeepSeek 余额查询插件 | `` | MIT |
| [warmwine/dsh-ui-font](https://github.com/warmwine/dsh-ui-font) | Runtime font engine + settings page to change and scale every font/size in the DSH Web GUI. | `` | MIT |
| [watericetangcw/dsh-page-preview](https://github.com/watericetangcw/dsh-page-preview) | Renders generated HTML inline and provides a floating window to preview local pages or URLs. | `` | MIT |
| [wenzetan/dsh-llm-newapi](https://github.com/wenzetan/dsh-llm-newapi) | NewAPI LLM 提供方插件 | `` | MIT |
| [WhitePlusMS/dsh-input-plus](https://github.com/WhitePlusMS/dsh-input-plus) | DSH 输入框增强插件。 | `` | MIT |
| [wqty123/dsh-browser](https://github.com/wqty123/dsh-browser) | DSH 浏览器插件，提供内置网页浏览与会话访问能力。 | `` | MIT |
| [wx-yss/dsh-message-rail](https://github.com/wx-yss/dsh-message-rail) | DSH 消息轨道/通知 UI 插件。 | `` | MIT |
| [x2802490130-prog/dsh-balance-float](https://github.com/x2802490130-prog/dsh-balance-float) | Floating widget showing DeepSeek account balance with manual refresh and one-click graceful exit. | `` | MIT |
| [XavierMarquis93/dsh-plugin-conversation-outline](https://github.com/XavierMarquis93/dsh-plugin-conversation-outline) | 对话目录侧栏 | `` | MIT |
| [Xenia0922/dsh-opencode-go-usage](https://github.com/Xenia0922/dsh-opencode-go-usage) | OpenCode Go quota/usage dashboard plugin for DSH. | `` | MIT |
| [xiake595/touhou-hakurei](https://github.com/xiake595/touhou-hakurei) | Touhou Reimu Hakurei skin for DSH web GUI (pure display layer). | `` | CC BY-NC-SA 4.0 |
| [xingyingyuzhui/dsh-liquid-glass](https://github.com/xingyingyuzhui/dsh-liquid-glass) | DSH 液态玻璃皮肤插件（壁纸预设 + 可选玻璃岛模糊） | `` | MIT |
| [XMoon/dsh-pi-tui](https://github.com/XMoon/dsh-pi-tui) | 基于 pi-tui 分支的 DSH 第三方终端 UI 插件（dsh --profile pi-tui） | `` | MIT |
| [xxxxxxxyu/dsh-notify-sound](https://github.com/xxxxxxxyu/dsh-notify-sound) | DSH 通知提示音插件。 | `` | MIT |
| [yanglongyun/dsh-ramify](https://github.com/yanglongyun/dsh-ramify) | DSH 内存/资源可视化插件 | `` | MIT |
| [yascitom/dsh-opencode-go-box](https://github.com/yascitom/dsh-opencode-go-box) | DSH opencode 风格的 Go 语言调试/运行盒子 UI 插件。 | `` | MIT |
| [yejiming/dsh-museai-tavern](https://github.com/yejiming/dsh-museai-tavern) | 将 MuseAI 角色与页面搬进 DSH Web GUI 的插件（复用 DSH 模型，无密钥） | `` | MIT |
| [Yuer6327/NoLetMe](https://github.com/Yuer6327/NoLetMe) | DSH 推理轨迹统计面板 | `` | MIT |
| [yunxiiQwQ/dsh-maid-whale-webUI](https://github.com/yunxiiQwQ/dsh-maid-whale-webUI) | DSH Web 鲸鱼女仆主题皮肤插件（亮暗模式 / 海洋插画 / 常驻 pet） | `` | BSD-3-Clause |
| [Zalpha263/dsh-file-explorer](https://github.com/Zalpha263/dsh-file-explorer) | 文件浏览器面板 | `` | MIT |
| [zdjmrq/dsh-user-plugins-manager](https://github.com/zdjmrq/dsh-user-plugins-manager) | DSH 设置页插件管理器，三层架构视图管理插件挂载/启停。 | `` | MIT |
| [zh667/TokenLedger](https://github.com/zh667/TokenLedger) | Token-usage accounting for DSH web GUI with relay-site attribution. | `` | MIT |
| [Zhangbo-cn/dsh-voice-input-plugin](https://github.com/Zhangbo-cn/dsh-voice-input-plugin) | DSH 语音输入插件。 | `` | MIT |
| [zhangzheng25/dsh-timeline](https://github.com/zhangzheng25/dsh-timeline) | DSH 时间线 UI 插件。 | `` | MIT |
| [zhijun-dai/Catppuccin-dsh-theme](https://github.com/zhijun-dai/Catppuccin-dsh-theme) | DSH Catppuccin 四色系主题插件（Latte/Frappé/Macchiato/Mocha） | `` | MIT |
| [Zzzzkd/dsh-prompt-rail](https://github.com/Zzzzkd/dsh-prompt-rail) | 提示词快速跳转条 | `` | MIT |

← [返回 README](../../README.md)
