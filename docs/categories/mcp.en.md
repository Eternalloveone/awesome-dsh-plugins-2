# MCP & Protocols / MCP 与协议

> Corresponding category on the site: [MCP & Protocols](https://deepseekharnessplugins.com/plugins/category/mcp)

| Plugin | Capability | Install or mount | License / Risk |
| --- | --- | --- | --- |
| [mrpulor-gh/nuphus-mcp](https://github.com/mrpulor-gh/nuphus-mcp) | 38 MCP tools (15 desktop + 23 browser): screenshots, window control, mouse/keyboard, clipboard, local OCR, BYOK vision, Chrome CDP automation incl. cookies/exec/snapshot. | `npm install -g @nuphus/nuphus-mcp  # prebuilt binary; or cargo build --release -p nuphus-mcp` | MIT; High risk: can take physical control of the machine and access browser cookies/clipboard. Run only in a trusted desktop session with --confirm-write. BYOK vision key is transmitted to an external provider. |
| [oomol-lab/dsh-oomol](https://github.com/oomol-lab/dsh-oomol) | Bridges OOMOL Connector Actions into DSH via progressive MCP discovery — discover connected apps and run Actions without exposing provider credentials | `dsh plugin --profile web add -w dsh-oomol` | MIT; Requires an OOMOL MCP API key; connects to an external Connector endpoint (hosted or self-hosted); self-hosted can run without auth |
| [ConsoleSun/Gemini-Eyes](https://github.com/ConsoleSun/Gemini-Eyes) | Gemini 网页端 MCP 桥接插件（逆向复用登录 Cookie 提供对话/识图/生图/生视频） | `` | MIT |
| [fly233338/dsh-overleaf](https://github.com/fly233338/dsh-overleaf) | 通过 OverleafMCP 把多个 Overleaf 项目接入 DSH 的插件（浏览/读取/写回） | `` | MIT |
| [inthepond/ff-toolkit](https://github.com/inthepond/ff-toolkit) | FFmpeg 操作封装为 CLI / MCP / DSH 插件工具集（dsh-ffkit） | `` | MIT |
| [jiezeng2004-design/dsh-chatgpt-bridge](https://github.com/jiezeng2004-design/dsh-chatgpt-bridge) | ChatGPT 经 MCP 连接并监督本地 DSH 代理会话的零侵入桥接插件（15 个 MCP 工具） | `` | MIT |
| [Js2Hou/dsh-mcp-manager](https://github.com/Js2Hou/dsh-mcp-manager) | MCP 可视化管理 | `` | MIT |
| [kairoz9/dsh-mcp-admin](https://github.com/kairoz9/dsh-mcp-admin) | Inspect MCP status via /mcp and manage MCP servers (add/edit/delete/enable) in DSH Settings, written back to cordis.patch.yml. | `` | MIT |
| [labmimors/dsh-mcp-lens](https://github.com/labmimors/dsh-mcp-lens) | DSH 的 MCP 检视/调试透镜插件。 | `` | MIT |
| [lmcsh9527/dsh-search-free](https://github.com/lmcsh9527/dsh-search-free) | DSH 免密钥搜索插件（外部搜索 API）。 | `` | MIT |
| [Momojie-S/dsh-workspace-mcp](https://github.com/Momojie-S/dsh-workspace-mcp) | DSH 工作区 MCP 插件（stdio/远程 MCP 服务器）。 | `` | MIT |
| [pazz11/Jnpz](https://github.com/pazz11/Jnpz) | Skills & MCP manager: paste JSON to add MCP servers (hot reload) and upload/parse/manage skills in Settings. | `` | MIT |
| [why913/dshx](https://github.com/why913/dshx) | DSH 扩展 (MCP/桥接) 插件 | `` | MIT |
| [xiongjiamu/dsh-atomgit](https://github.com/xiongjiamu/dsh-atomgit) | DSH 接入 AtomGit 的 MCP/服务插件。 | `` | MulanPSL-2.0 |
| [zebbkira/dsh-skills-mcp-manager](https://github.com/zebbkira/dsh-skills-mcp-manager) | DSH 技能与 MCP 服务管理器。 | `` | MIT |
| [ZSeven-W/dsh-crew](https://github.com/ZSeven-W/dsh-crew) | DSH Crew：把任务分发给 DSH agent 的插件（保留 Claude Code / Codex 原生子代理 UI） | `` | MIT |

← [Back to README](../../README.md)
