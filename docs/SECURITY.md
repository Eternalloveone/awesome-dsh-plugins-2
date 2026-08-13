# DSH Plugin Installation Security Guide

DeepSeek Harness plugins can expose tools to agents, inject Web UI, access local files, call network services, or mount into the shared Cordis context. DSH profiles retain installed out-of-tree plugins and user patches as part of their composition.[1] Treat a plugin installation as **local code execution plus a permission expansion**, not as a cosmetic theme install.

> **“Verified” in this directory means that a public DSH loading signal and an installation or mounting path were inspected. It does not mean a complete security audit, author verification, endorsement, or stability guarantee.**

## Minimum pre-installation review

| Check | Action | Reason |
| --- | --- | --- |
| Pin the source | Use a release tag, commit SHA, or trusted package version and record the URL | Default branches can change without notice |
| Read the entry points | Inspect `package.json`, `dsh.plugin.json`, `cordis.patch.yml`, `apply` entry points, and dependencies | Learn which services and tools are actually mounted |
| Audit lifecycle scripts | Check `preinstall`, `install`, `postinstall`, and `prepare` | Package lifecycle scripts can execute arbitrary local commands |
| Use least privilege | Create a separate test profile, unprivileged API key, and non-production workspace | Limits data exposure and destructive tool calls |
| Trace data egress | Identify endpoints receiving prompts, code, images, logs, or tool results | Vision, search, memory, and IM extensions commonly send data externally |
| Preserve a rollback | Export profile configuration and record dependency/patch changes before install | Preview APIs can change and may require a fast rollback |

## High-risk permission matrix

| Permission surface | Representative extensions | Primary concern | Recommended controls |
| --- | --- | --- | --- |
| Signed-in browser | `dsh-better-browser` | Cookies, sessions, form input, uploads, page actions | Use a dedicated browser profile; do not log in to sensitive accounts; require approval |
| SSH / SFTP / remote commands | `dsh-ssh`, `jumpserver-dsh` | Remote execution, file access, key exposure | Dedicated low-privilege account, explicit known hosts, ACLs, and audit logs |
| IM channels | `dsh-lark`, `dsh-lark-bridge`, QQ-related plugins | Untrusted messages can drive an agent; data leakage | User/group allowlists, approval, and no untrusted direct messages |
| Files, memory, and notes | Skills, memory plugins, `dsh-wikilink` | Workspace material is injected or uploaded | Mount only required paths; define filtering and retention rules |
| External APIs | Search, vision, model gateway, balance extensions | Key leakage, data transfer, uncontrolled spending | Environment variables, separate keys, spend limits, and alerts |
| Client injection and local CLI | UI, notification, VS Code, TUI extensions | Browser permissions, command abuse, output leakage | Use trusted sources and explicit executable paths |

## Suggested isolated test workflow

Export the target profile with `dsh --profile <name> --dump-config`, create a separate test profile, and install one extension at a time. Review newly added dependencies, `cordis.patch.yml` rows, and Web-client injection points. Run the smallest functional test before moving an extension into a daily profile.[1]

For sensitive environments, favor local models, local LM Studio, and configurations with no cloud sync. For browser, remote-execution, IM, or third-party API extensions, keep credentials, targets, and human-confirmation policy outside source control.

## Reporting unsafe entries

If a listed project appears malicious, leaks credentials, contains a supply-chain risk, gives misleading installation guidance, or is wrongly classified, do not post secrets, internal URLs, chat content, or exploit detail in a public issue. Submit minimal reproducible evidence with the project URL, affected version, risk type, and disclosure state. Maintainers can add a warning, move the item to the watchlist, or remove it.

## Reference

[1] [DeepSeek Harness Architecture — Profiles and Bundles](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)
