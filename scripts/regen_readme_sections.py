#!/usr/bin/env python3
"""regen_readme_sections.py — rebuild the verified-plugin portion of the
awesome-dsh-plugins READMEs so its section structure matches the companion
website's 22 categories (deepseekharnessplugins.com/plugins/categories).

It reads data/verified-plugins.csv, maps each row's `category` slug onto one
of the 22 site categories, and regenerates the block between the
"Native DSH extensions / 原生 DSH 插件" heading and the
"Official built-in capabilities / 官方内置能力" heading. Header prose, the
aggregated-catalog section, and all post-verified sections are preserved.

Usage:
  python3 scripts/regen_readme_sections.py            # write in place
  python3 scripts/regen_readme_sections.py --dry /tmp # write to /tmp/README*.new.md
"""
import csv, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 22 categories in the website's order (id, zh, en)
CATEGORIES = [
    ("ui-experience",        "界面与体验",            "UI & Experience"),
    ("sessions-messages",    "会话与消息",            "Sessions & Messages"),
    ("utilities",            "其他",                  "Other"),
    ("desktop",              "桌面与应用",            "Desktop & Apps"),
    ("mcp",                  "MCP 与协议",            "MCP & Protocols"),
    ("plugin-tools",         "插件工具",              "Plugin Tooling"),
    ("web-ui",               "Web 界面与前端",        "Web UI & Frontend"),
    ("theme",                "主题与皮肤",            "Themes & Skins"),
    ("security",             "安全与鉴权",            "Security & Auth"),
    ("chat-im",              "聊天与 IM",             "Chat & IM"),
    ("cli",                  "命令行与终端",          "CLI & Terminal"),
    ("voice",                "语音",                  "Voice & Speech"),
    ("lists",                "清单与资源",            "Lists & Resources"),
    ("billing",              "用量与计费",            "Usage & Billing"),
    ("agents-workflows",     "Agent、自动化与工作流", "Agents, Automation & Workflows"),
    ("integrations-sharing", "集成与分享",            "Integrations & Sharing"),
    ("developer-tools",      "开发者工具",            "Developer Tools"),
    ("knowledge-research",   "知识与研究",            "Knowledge & Research"),
    ("media-vision",         "设计、媒体与视觉",      "Design, Media & Vision"),
    ("web-browser",          "网页与浏览器",          "Web & Browser"),
    ("ecosystem-resources",  "生态与资源",            "Ecosystem & Resources"),
    ("fun",                  "纯属好玩",              "Just for Fun"),
]
CAT_IDS = [c[0] for c in CATEGORIES]

# CSV `category` slug -> site category id
SLUG_MAP = {
    "vision": "media-vision",
    "web_ui": "web-ui",
    "tui": "ui-experience",
    "fun": "fun",
    "session_chat": "sessions-messages",
    "memory_persona": "sessions-messages",
    "search_browser": "web-browser",
    "data_tools": "knowledge-research",
    "automation": "agents-workflows",
    "communication": "chat-im",
    "remote_device": "desktop",
    "developer_tools": "developer-tools",
    "diagnostics": "plugin-tools",
    "ecosystem": "ecosystem-resources",
    "uncategorized": "utilities",
    "skills": "ecosystem-resources",
    "ui": "ui-experience",
    "other": "utilities",
    "model_gateway": "developer-tools",
    "agent_orchestration": "agents-workflows",
    "cost_observability": "billing",
    "agent-os": "agents-workflows",
    "memory": "knowledge-research",
    "security_audit": "security",
    "web_ui_customization": "web-ui",
    "mcp": "mcp",
    "context_management": "agents-workflows",
    "launcher": "desktop",
    "notifications": "chat-im",
    "developer_skills": "developer-tools",
    "task_management": "agents-workflows",
    "knowledge_management": "knowledge-research",
    "observability": "billing",
    "desktop": "desktop",
    "plugin_diagnostics": "plugin-tools",
    "deterministic_tools": "developer-tools",
    "long_term_memory": "knowledge-research",
    "education": "knowledge-research",
    "prompt_persona": "sessions-messages",
    "browser_automation": "web-browser",
    "game": "fun",
    "response_presentation": "ui-experience",
    "conversation_interface": "chat-im",
    "remote_execution": "desktop",
    "plugin_development_skill": "plugin-tools",
    "desktop_automation": "desktop",
    "developer_panel": "developer-tools",
    "conversation_sharing": "integrations-sharing",
    "computer_use": "desktop",
    "list": "lists",
    "session_diagnostics": "sessions-messages",
    "translation": "knowledge-research",
    "terminal_ui": "cli",
    "agent_memory_orchestration": "agents-workflows",
    "legal": "ecosystem-resources",
    # extra slugs discovered in the data
    "web_search": "web-browser",
    "chat_integration": "chat-im",
    "skill": "ecosystem-resources",
    "developer_tooling": "developer-tools",
    "plan_review": "agents-workflows",
    "sidebar_workbench": "ui-experience",
    "companion_memory": "knowledge-research",
    "qq_meme_sending": "fun",
    "device_bridge": "desktop",
    "web_review": "web-browser",
    "tui_bridge": "ui-experience",
}

SNAPSHOT_DATE = "2026-08-19"

# ---- markdown helpers -------------------------------------------------------
def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()

def anchor(h):
    s = h.strip().lower()
    s = re.sub(r"\s+", "-", s)
    # keep alphanumerics, CJK, hyphens; drop the rest
    s = re.sub(r"[^\w一-鿿\-]", "", s)
    return s

def build_row(r, lang):
    repo = r["repository"]
    cap = esc(r.get("capability"))
    if not cap:
        return None
    install = re.sub(r"\s*\n\s*", "; ", (r.get("install_or_usage") or "")).strip()
    install = esc(install)
    lic = esc(r.get("license"))
    caution = esc(r.get("caution"))
    if "`" in install or re.search(r"see README|见 README", install, re.I):
        inst = install
    else:
        inst = f"`{install}`"
    if lang == "cn":
        lic_txt = "未发现" if lic.lower() in ("not found", "none") else lic
        cell = f"{lic_txt}；{caution}" if caution else lic_txt
    else:
        cell = f"{lic}; {caution}" if caution else lic
    return f"| [{repo}]({r['url']}) | {cap} | {inst} | {cell} |"

# ---- per-language templates -------------------------------------------------
def regen(text, lang):
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "verified-plugins.csv"),
                                   encoding="utf-8")))
    cap_rows = [r for r in rows if (r.get("capability") or "").strip()]
    # one row per repo (first occurrence wins), assigned to a category
    seen = {}
    assigned = {cid: [] for cid in CAT_IDS}
    unmapped = []
    for r in cap_rows:
        repo = r["repository"]
        if repo in seen:
            continue
        seen[repo] = True
        slug = (r.get("category") or "").strip()
        cid = SLUG_MAP.get(slug)
        if cid is None:
            cid = "utilities"
            unmapped.append(slug)
        assigned[cid].append(r)
    for cid in assigned:
        assigned[cid].sort(key=lambda r: r["repository"].lower())

    verified_count = len(seen)

    # build the 22 sections
    if lang == "cn":
        intro = ("下列条目已核验至少一个原生特征：可复现的 `dsh plugin` 安装命令、"
                 "`dsh.bundle` / `cordis.patch.yml` 声明，或 DSH/Cordis 可挂载的 `apply` 入口。"
                 "**“已核验”不代表作者、代码质量或安全性背书。**\n")
        hdr_plugin, hdr_cap, hdr_inst, hdr_lic = "插件", "能力", "安装或挂载方式", "许可 / 风险"
        heading_prefix = "## "
    else:
        intro = ("An entry in this section has at least one verified native signal: a reproducible "
                 "`dsh plugin` command, a `dsh.bundle` / `cordis.patch.yml` declaration, or a "
                 "DSH-compatible Cordis `apply` entry. **Verified does not mean audited, endorsed, "
                 "safe, or stable.**\n")
        hdr_plugin, hdr_cap, hdr_inst, hdr_lic = "Plugin", "Capability", "Install or mount", "License / Risk"
        heading_prefix = "## "

    title = "已核验插件目录" if lang == "cn" else "Verified directory"
    section_blocks = [f"{heading_prefix}{title}\n\n{intro.rstrip(chr(10))}"]
    for cid, zh, en in CATEGORIES:
        name = zh if lang == "cn" else en
        block = [f"{heading_prefix}{name}\n"]
        table = assigned.get(cid, [])
        if table:
            block.append(f"| {hdr_plugin} | {hdr_cap} | {hdr_inst} | {hdr_lic} |")
            block.append("| --- | --- | --- | --- |")
            for r in table:
                row = build_row(r, lang)
                if row:
                    block.append(row)
        else:
            block.append("> 暂无已核验条目。\n" if lang == "cn" else "> No verified entries yet.\n")
        section_blocks.append("\n".join(block))

    new_body = "\n\n".join(section_blocks) + "\n"

    # ---- splice: replace region between start/end markers ----
    if lang == "cn":
        start_marker = "## 原生 DSH 插件"
        end_marker = "## 官方内置能力（不是社区插件）"
    else:
        start_marker = "## Native DSH extensions"
        end_marker = "## Official built-in capabilities (not community plugins)"

    lines = text.split("\n")
    si = next((i for i, l in enumerate(lines) if l.strip() == start_marker), None)
    ei = next((i for i, l in enumerate(lines) if l.strip() == end_marker), None)
    if si is None or ei is None:
        raise SystemExit(f"[{lang}] markers not found: start={si} end={ei}")
    # keep the start marker line? We replace from start_marker line through ei-1.
    lines[si:ei] = [new_body.rstrip("\n")]

    text = "\n".join(lines)

    # ---- nav table ----
    if lang == "cn":
        nav_header = "| 导航 | 内容 |"
        nav_intro = ("| [已核验插件目录](#已核验插件目录) | 按 22 个能力分类的已核验可装载扩展（与"
                     "[网站](https://deepseekharnessplugins.com)同构） |")
        cat_links = " · ".join(
            f"[{zh}](#{anchor(zh)})" for _, zh, _ in CATEGORIES)
        cat_row = f"| {cat_links} | 22 个分类锚点 |"
        preserved = [
            "| [全量聚合目录](#全量聚合目录) | **2296 个** DSH 相关仓库的完整聚合（含未审核候选）；[审计日志](data/audit-results.csv) |",
            nav_intro,
            cat_row,
            "| [官方内置能力](#官方内置能力不是社区插件) | 随 DSH 源码发行的官方运行时构件 |",
            "| [相关项目与观察名单](#相关项目与观察名单不计入主目录) | 相关但并非已核验原生插件的项目 |",
            "| [安装与安全](#安装与安全) | 安装惯例、权限提示与审计建议 |",
            "| [贡献规则](#贡献与维护) | 新项目的提交格式与审核门槛 |",
        ]
    else:
        nav_header = "| Navigation | Purpose |"
        nav_intro = ("| [Verified directory](#verified-directory) | Verified loadable extensions grouped into "
                     "22 capability categories (aligned with the [site](https://deepseekharnessplugins.com)) |")
        cat_links = " · ".join(
            f"[{en}](#{anchor(en)})" for _, _, en in CATEGORIES)
        cat_row = f"| {cat_links} | 22 category anchors |"
        preserved = [
            "| [Full aggregated catalog](#full-aggregated-catalog) | **All 2,296** DSH-related repositories, including unreviewed candidates; [audit log](data/audit-results.csv) |",
            nav_intro,
            cat_row,
            "| [Built-in DSH components](#official-built-in-capabilities-not-community-plugins) | Runtime components shipped in the official source tree |",
            "| [Watchlist and related projects](#watchlist-and-related-projects) | Related but unverified or non-loadable projects |",
            "| [Safety](#installation-and-safety) | Permission-aware installation guidance |",
        ]
    # replace nav block (from nav_header line to next blank line)
    ni = next((i for i, l in enumerate(lines) if l.strip() == nav_header), None)
    if ni is None:
        raise SystemExit(f"[{lang}] nav header not found")
    bi = next((j for j in range(ni + 1, len(lines)) if lines[j].strip() == ""), len(lines))
    new_nav = [nav_header, "| --- | --- |"] + preserved
    lines[ni:bi] = new_nav
    text = "\n".join(lines)

    # ---- badge + snapshot paragraph ----
    text = re.sub(r"verified-\d+", f"verified-{verified_count}", text)
    if lang == "cn":
        new_snap = (f"**快照日期：{SNAPSHOT_DATE}。** 本版主目录收录 **{verified_count} 个**"
                    "经源码或安装清单核验的插件与 Skill，按 22 个能力分类组织（与配套网站 "
                    "[deepseekharnessplugins.com](https://deepseekharnessplugins.com) 同构）；"
                    "同时提供 **全量聚合目录 [`CATALOG.md`](CATALOG.md)（2296 个仓库）**，合并 GitHub 搜索与多个社区目录去重后得到。"
                    "**聚合 ≠ 可装载、可兼容、可安全运行**；只有本目录核验子集进入主目录，证据见 "
                    "[data/verified-plugins.csv](data/verified-plugins.csv) 与 [data/audit-results.csv](data/audit-results.csv)。[3]")
    else:
        new_snap = (f"**Snapshot: {SNAPSHOT_DATE}.** This edition's main directory includes "
                    f"**{verified_count} verified plugins and skills whose source or install manifests were inspected**, "
                    "organized into 22 capability categories (aligned with the companion site "
                    "[deepseekharnessplugins.com](https://deepseekharnessplugins.com)); plus a **full aggregated catalog — "
                    "[`CATALOG.md`](CATALOG.md), 2,296 repositories** — merged and deduplicated from GitHub search and "
                    "several community directories. **Aggregation is not an installation, compatibility, maintenance, or "
                    "security certification**; only the verified subset enters the main directory, with evidence in "
                    "[data/verified-plugins.csv](data/verified-plugins.csv) and [data/audit-results.csv](data/audit-results.csv).[3]")
    text = re.sub(r"^\*\*快照日期：.*$", new_snap, text, flags=re.M, count=1)
    text = re.sub(r"^\*\*Snapshot:.*$", new_snap, text, flags=re.M, count=1)

    return text, verified_count, unmapped

def main():
    dry = "--dry" in sys.argv
    outdir = sys.argv[sys.argv.index("--dry") + 1] if dry else None
    targets = [("cn", "README.md"), ("en", "README.en.md")]
    for lang, fn in targets:
        path = os.path.join(ROOT, fn)
        text = open(path, encoding="utf-8").read()
        new_text, count, unmapped = regen(text, lang)
        if dry:
            out = os.path.join(outdir, fn.replace(".md", ".new.md"))
            open(out, "w", encoding="utf-8").write(new_text)
            print(f"[{lang}] {fn}: verified={count}, unmapped slugs={sorted(set(unmapped))}, -> {out}")
        else:
            open(path, "w", encoding="utf-8").write(new_text)
            print(f"[{lang}] {fn}: written, verified={count}, unmapped slugs={sorted(set(unmapped))}")

if __name__ == "__main__":
    main()
