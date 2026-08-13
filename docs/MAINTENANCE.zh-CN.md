# 维护手册

DeepSeek Harness 仍处于 Developer Preview，官方明确说明核心插件与 API 会继续演进。[1] 本目录应被维护为有时间边界的核验快照，而不是永久正确的安装保证。每次更新都应先刷新候选池，再验证 DSH 原生挂载证据，最后更新人类可读目录和机器可读数据集。

## 例行维护节奏

| 频率 | 工作 | 产物 |
| --- | --- | --- |
| 每周 | 浏览 GitHub `dsh-plugin` 主题、DSH Releases 与官方架构/迁移文档；抽查失效 URL 与归档仓库 | `data/verified-plugins.csv` 的 `last_activity`、`checked_at` 与状态更新 |
| 每个 DSH RC / 正式版 | 复测代表性插件的 Profile 安装、Bundle 装载和最小启动；重点检查 `dsh` manifest 与 patch schema | README 的兼容性警告、升级说明或降级为观察名单 |
| 新插件 PR | 审核公开源代码、挂载证明、安装命令、许可和数据流/权限 | 分类、风险级别、来源链接与审阅记录 |
| 安全报告 | 复核最小证据；必要时立即在 README 降级或移除；避免公开敏感细节 | 风险标记、观察名单或移除记录 |

## 建议的复核命令

以下命令仅用于在**隔离测试环境**中检查一个已知来源插件的安装结构；运行前仍应阅读项目代码并锁定版本。

```bash
# 查看当前 Profile 将加载的插件树与 patch。
dsh --profile web --dump-config

# 安装后确认该依赖是否位于指定 Profile。
dsh plugin --profile web list <package-name> --depth 0

# 检查 package metadata 与生命周期脚本；不要忽略输出中的 scripts 字段。
pnpm view <package-name> --json
```

不要把这些命令解释为通用安装脚本。对于 Git 仓库来源，应优先使用 release tag 或 commit SHA；对于本地 `link:` 安装，应记录本地路径、构建命令和 DSH 版本。对于浏览器、SSH、IM、云端搜索/视觉/记忆服务，必须按照 [安全指南](SECURITY.md) 重新确认权限与数据流。

## 候选池与误标处理

GitHub `dsh-plugin` topic 是官方网页给出的社区发现入口，但它不执行协议或安全验证。[2] 维护者可从主题页、GitHub Search API、项目 README、npm 包页和官方文档发现候选；但是只有具备收录标准中的原生证据时才能进入主目录。教程、启动器、普通 DeepSeek 应用和其他聚合列表应单独标注，不能为了增加条目数而进入「原生 DSH 插件」。

如果仓库被删除、转私有、明显误标、没有许可、没有 DSH 挂载方式，或在当前 DSH 版本中无法加载，优先标记为 `watchlist`。如确认存在恶意或高危供应链行为，应删除主目录链接并记录非敏感原因。不要在本仓库中复刻第三方插件源码、打包其未授权资产或传播 API Key。

## 全量目录刷新

[`CATALOG.md`](../CATALOG.md) 与 [`data/repositories.csv`](../data/repositories.csv) 由聚合脚本生成：它合并 GitHub 搜索（`topic:dsh-plugin`、`topic:deepseek-harness`、名称搜索）、本地主题快照与外部社区目录。每次快照前请重新生成（需要已登录的 `gh` CLI）：

```bash
python3 scripts/aggregate.py
```

聚合输出是**发现清单**而非审核结论：每个候选仍须按本手册的标准逐项复核后才能进入已核验子集。

## 参考资料

[1] [DeepSeek Harness Developer Preview](https://deepseek.com/harness/en/)

[2] [GitHub Topic: dsh-plugin](https://github.com/topics/dsh-plugin)
