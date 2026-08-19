# 集成与分享 / Integrations & Sharing

> 对应网站分类：[集成与分享 · Integrations & Sharing](https://deepseekharnessplugins.com/plugins/category/integrations-sharing)

| 插件 | 能力 | 安装或挂载方式 | 许可 / 风险 |
| --- | --- | --- | --- |
| [kinyokun/dsh-session-import](https://github.com/kinyokun/dsh-session-import) | 会话日志导入：解析 /export 导出的 zip/裸 .jsonl 为新会话，导入前做结构真实性验证 + SHA-256 指纹校验，可同步模型/预设/权限等状态；自带浏览器端「导入对话」按钮与对话框，导入/删除实时推送免刷新 | 手动安装：mkdir -p "$PROFILE_DIR/node_modules/dsh-session-import" && cp host.js client.js package.json 目录，再在 $PROFILE_DIR/cordis.patch.yml 追加 `name: dsh-session-import` 行，重启 dsh web | MIT；导入内容来自外部 zip/jsonl，校验逻辑是唯一防线；删除内存活跃且非本插件导入的会话会被拒（409 live） |
| [omdsh-dev/dsh-shuttle](https://github.com/omdsh-dev/dsh-shuttle) | 在 DSH 与 Codex、Claude Code、Pi、Reasonix、OpenCode 之间双向迁移对话记录，支持 CLI 与 Web UI；CLI 示例 node lib/cli.js export --to opencode --session <id> --destination /tmp/dsh-opencode --apply。 | `通过 DSH 常规插件流程安装（bundle 自带 cordis.patch.yml，挂载 ctx.shuttle 与 migrate-conversations skill）；本地 pnpm build 后 dsh plugin add；CLI 可独立 node lib/cli.js` | MIT；导出文件含完整对话内容，导入目标工具前注意其存储与可见性。 |

← [返回 README](../../README.md)
