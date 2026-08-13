# Contributing

Thank you for helping maintain the DeepSeek Harness (DSH) ecosystem. This project is not a list of every repository that added a `dsh-plugin` topic. Its purpose is to keep a **loadable, verifiable, and permission-aware** directory.

## Inclusion threshold

A project must satisfy every requirement below before it enters the README’s native DSH extension directory.

| Requirement | Acceptable evidence |
| --- | --- |
| Public source | A publicly accessible source repository with an identifiable project name |
| Native DSH relationship | A `dsh.bundle` / `dsh.profile` declaration, `cordis.patch.yml`, `dsh.plugin.json`, a Cordis `apply` entry, or explicit documented DSH mounting evidence |
| Reproducible loading | A copyable `dsh plugin --profile … add …` command or clear profile-patch/bundle-mount instructions |
| Identifiable function | A concise, verifiable functional description rather than only promotional copy |
| License information | An SPDX identifier, or an explicit `Not found` status |
| Permission disclosure | A note covering API keys, network calls, browser sessions, local files, chat data, remote commands, or privileged credentials |

A project that only uses a DeepSeek model/API, only carries a `dsh` or `dsh-plugin` topic, or is merely a tutorial, launcher, desktop shell, generic library, or another directory does not enter the native section. It may be placed in the watchlist after its purpose is confirmed. A DSH Skill may enter the skills section only when labelled as a skill, never as a Cordis-native bundle.

## Submission template

Add the item to `data/verified-plugins.csv` and update the relevant README category. A proposed issue or pull request should contain the following information.

```markdown
### Project
- Repository: `owner/repo`
- URL: `https://github.com/owner/repo`
- Kind: `installable_dsh_plugin` / `dsh_skill_or_preset`
- Category: e.g. `vision`, `web_ui`, `remote_execution`

### DSH loading evidence
- Manifest / patch / apply URL:
- Exact installation command or profile configuration:

### Maintenance facts
- License:
- Last activity: YYYY-MM-DD
- Supported DSH release, if documented:

### Permissions and data flow
- Does it access local files, browser sessions, commands, network, or API keys?
- Which third parties receive data?
- What is the minimum-permission recommendation?
```

## Editorial principles

Write accurately and conservatively. Do not describe a project as secure, official, audited, best, or production-ready without strong primary evidence. Preserve the author’s original installation command; retain placeholders such as `<profile>`, `<repo>`, API key, and local-path values, and link to the upstream instructions. Never submit secrets, cookies, personal sessions, real host addresses, or internal configuration.

Retain uncertainty when an extension is early-stage, unreleased, lightly maintained, or tied to a breaking DSH preview API. If a project has no declared license, it can still be a research item, but must not be presented as freely redistributable.

## Statuses

| Status | Meaning |
| --- | --- |
| `verified` | Native DSH loading evidence and an install/mounting path were inspected |
| `skill` | DSH skill discovery/use path was inspected; native bundle status is not claimed |
| `watchlist` | Related project with incomplete or untested compatibility evidence |
| `related` | Ecosystem-adjacent project that is not a loadable DSH extension |
| `excluded` | Out of scope, unavailable, misleading, or unsuitable for inclusion |

## Updates and removals

Report broken installation paths, archived projects, license changes, security concerns, or dropped DSH support. Maintainers prefer factual traceability: a failing item is normally moved to `watchlist` or marked archived before removal, while confirmed malicious or high-risk supply-chain entries can be removed from the native directory immediately.
