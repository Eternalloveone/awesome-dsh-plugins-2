# 贡献指南

感谢你帮助维护 DeepSeek Harness（DSH）插件生态。这个仓库的目标不是收集所有带 `dsh-plugin` topic 的项目，而是形成一个**可安装、可核验、可解释风险**的精选目录。

## 收录门槛

一个项目要进入 README 的「原生 DSH 插件」主目录，必须同时满足下表的所有要求。

| 要求 | 可接受证据 |
| --- | --- |
| 公开可访问 | 可公开访问的源码仓库和明确项目名称 |
| DSH 原生关联 | `package.json` 的 `dsh.bundle` / `dsh.profile`、`cordis.patch.yml`、`dsh.plugin.json`、Cordis `apply` 入口，或官方/项目 README 的明确 DSH 挂载说明 |
| 可复现安装 | 可复制的 `dsh plugin --profile … add …` 命令，或清晰的 Profile patch / Bundle 挂载步骤 |
| 可识别功能 | 一句可验证的功能说明，不使用纯宣传性文案 |
| 许可信息 | SPDX 许可证标识，或显式标注 `Not found` |
| 风险披露 | 至少说明是否需要 API Key、网络访问、浏览器登录态、文件系统、聊天数据、远程命令或高权限凭据 |

项目仅使用 DeepSeek 模型或 API、只贴有 `dsh` / `dsh-plugin` topic、只是桌面壳/教程/聚合列表，或没有任何 DSH 挂载证据时，不会列入主目录。它们可以在确认用途后进入「相关项目与观察名单」。DSH Skill 可以进入「技能与预设」区，但必须明确标注为 Skill，而非 Cordis 原生插件。

## 提交格式

请在提交前将项目加入 `data/verified-plugins.csv`，再按功能类别更新 README。建议用以下 Issue 或 Pull Request 模板提交资料：

```markdown
### 项目
- 仓库：`owner/repo`
- URL：`https://github.com/owner/repo`
- 类型：`installable_dsh_plugin` / `dsh_skill_or_preset`
- 分类：例如 `vision`、`web_ui`、`remote_execution`

### DSH 挂载证据
- manifest / patch / apply URL：
- 精确安装命令或 Profile 配置：

### 维护信息
- 许可证：
- 最近活动日期：YYYY-MM-DD
- 适配的 DSH 版本（如有）：

### 权限与数据流
- 是否读取本地文件、访问浏览器、执行命令、使用网络或 API Key：
- 数据会发送到哪些第三方服务：
- 最小权限建议：
```

## 编辑原则

请使用准确、克制的文字。不要声称“安全”“最佳”“官方认证”或“生产可用”，除非能给出强证据。安装命令应保持原作者的原始形式；若命令需要替换 `<profile>`、`<repo>`、API Key 或路径，应保留占位符并链接原文。不要提交密钥、Cookie、个人会话、真实主机地址或内部配置。

若插件处于早期预览、没有 release、只有极少提交或依赖破坏性 API，应保留这一事实并添加相应提醒。若一个插件没有明确许可证，仍可作为观察资料，但不得暗示其可自由再分发。

## 分类与状态

| 状态 | 含义 |
| --- | --- |
| `verified` | 核验到原生 DSH 挂载证据和安装路径 |
| `skill` | 核验到 DSH Skill 发现/使用路径，但不是原生 Bundle |
| `watchlist` | 相关或看似可用，但证据不足、未能复现或风险需要澄清 |
| `related` | 生态相关，但不是 DSH 可加载插件 |
| `excluded` | 明显误标、已删除、恶意、无公开来源或不符合目录范围 |

## 更新与移除

如果安装命令失效、项目归档、许可证变化、发现安全问题或项目不再支持 DSH，请提交纠正。维护者优先保留事实和历史可追溯性：失效项目通常会先标为 `watchlist` 或 `archived`，严重安全风险或恶意条目会从主目录移除。
