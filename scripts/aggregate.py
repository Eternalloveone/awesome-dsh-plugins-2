#!/usr/bin/env python3
"""
aggregate.py — Build the full awesome-dsh-plugins catalog.

Merges every discoverable DeepSeek Harness plugin repository into
data/repositories.csv and CATALOG.md:

  * GitHub search: topic:dsh-plugin, topic:deepseek-harness, "dsh-plugin in:name"
  * data/dsh-plugin-topic-candidates.csv (topic crawl snapshot)
  * data/verified-plugins.csv (the curated, verified subset)
  * reference awesome lists (bruc3van, Alex-Yanggg, awesome-dsh-plugin, AdamPlatin123)

The verified subset stays flagged separately; the aggregated pool is a
discovery universe, not a recommendation or compatibility list.

Requirements: python3, gh CLI (authenticated), network access.
Usage:       python3 scripts/aggregate.py
"""

import csv
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from collections import Counter, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "data", "topic-snapshot")
UA = {"User-Agent": "awesome-dsh-plugins-aggregator/1.0"}

# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------

SEARCH_QUERIES = [
    "topic:dsh-plugin",
    "topic:deepseek-harness",
    "dsh-plugin in:name",
]

RAW_URLS = {
    "bruc3van_repositories.json": "https://raw.githubusercontent.com/bruc3van/awesome-dsh-plugin/HEAD/data/repositories.json",
    "bruc3van_curated.json": "https://raw.githubusercontent.com/bruc3van/awesome-dsh-plugin/HEAD/data/curated.json",
    "alex_plugins.json": "https://raw.githubusercontent.com/Alex-Yanggg/awesome-DSH-plugin/HEAD/catalog/plugins.json",
    "awesomedsh_README.md": "https://raw.githubusercontent.com/awesome-dsh-plugin/awesome-dsh-plugin/HEAD/README.md",
    "awesomedsh_README.zh.md": "https://raw.githubusercontent.com/awesome-dsh-plugin/awesome-dsh-plugin/HEAD/README.zh.md",
    "adam_PLUGINS.md": "https://raw.githubusercontent.com/AdamPlatin123/awesome-dsh-plugins/HEAD/PLUGINS.md",
}

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def gh(*args):
    out = subprocess.run(["gh", "api", *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"gh api failed: {args} -> {out.stderr[:300]}")
    return out.stdout


def fetch_repo(full_name, tries=4):
    """Fetch repo metadata, distinguishing genuine 404s from rate limits.

    Returns a dict on success, None on 404/410 (gone), and raises on a
    persistent rate limit so the run fails loudly instead of dropping real
    repositories.
    """
    token = subprocess.run(["gh", "auth", "token"], capture_output=True,
                           text=True).stdout.strip()
    for attempt in range(tries):
        raw = subprocess.run(
            ["curl", "-s", "-w", "\n%{http_code}", "-L",
             "-H", "Accept: application/vnd.github+json",
             "-H", f"Authorization: Bearer {token}",
             f"https://api.github.com/repos/{full_name}"],
            capture_output=True, text=True)
        body, _, status = raw.stdout.rstrip().rpartition("\n")
        try:
            code = int(status)
        except ValueError:
            code = 0
        if code == 200:
            j = json.loads(body)
            return {
                "full_name": j.get("full_name") or full_name,
                "html_url": j.get("html_url") or f"https://github.com/{full_name}",
                "description": (j.get("description") or "").strip(),
                "stars": j.get("stargazers_count") or 0,
                "license": (j.get("license") or {}).get("spdx_id") or "",
                "language": j.get("language") or "",
                "topics": j.get("topics") or [],
                "pushed_at": j.get("pushed_at") or "",
                "homepage": j.get("homepage") or "",
            }
        if code in (404, 410):
            return None
        if code in (403, 429):
            time.sleep(15 * (attempt + 1))  # secondary rate limit: back off
            continue
        if code >= 500:
            time.sleep(5 * (attempt + 1))  # transient server error
            continue
        return None  # unexpected status; treat as unreachable
    raise RuntimeError(f"persistent rate limit while fetching {full_name}")


def search_page(query, page):
    raw = gh("-X", "GET", "search/repositories",
             "-f", f"q={query}", "-f", "per_page=100", "-f", f"page={page}")
    return json.loads(raw)


def collect_search(query):
    repos, page = {}, 1
    while True:
        data = search_page(query, page)
        items = data.get("items", [])
        if not items:
            break
        for it in items:
            full = it.get("full_name") or ""
            if not full:
                continue
            repos[full.lower()] = {
                "full_name": full,
                "html_url": it.get("html_url")
                or f"https://github.com/{full}",
                "description": (it.get("description") or "").strip(),
                "stars": it.get("stargazers_count") or 0,
                "license": (it.get("license") or {}).get("spdx_id") or "",
                "language": it.get("language") or "",
                "topics": it.get("topics") or [],
                "pushed_at": it.get("pushed_at") or "",
                "homepage": it.get("homepage") or "",
                "_meta_ok": True,  # full metadata already present from search
            }
        print(f"  search {query!r} page {page}: {len(items)} items")
        if len(items) < 100:
            break
        page += 1
        if page > 12:
            break
        time.sleep(2)
    return repos


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# --------------------------------------------------------------------------
# category mapping
# --------------------------------------------------------------------------

CATS = OrderedDict([
    ("vision",          ("视觉与多模态", "Vision & Multimodal")),
    ("web_ui",          ("Web UI 增强", "Web UI Enhancements")),
    ("tui",             ("终端界面 TUI", "Terminal UI")),
    ("session_chat",    ("会话与聊天", "Sessions & Chat")),
    ("search_browser",  ("搜索与浏览器", "Search & Browser")),
    ("automation",      ("自动化与工作流", "Automation & Workflow")),
    ("memory_persona",  ("记忆与个性化", "Memory & Persona")),
    ("communication",   ("通信与集成", "Messaging & Integrations")),
    ("remote_device",   ("远程执行与设备", "Remote & Devices")),
    ("developer_tools", ("开发工具与基础设施", "Developer Tools & Infra")),
    ("data_tools",      ("数据与文档工具", "Data & Document Tools")),
    ("diagnostics",     ("诊断、审计与可观测性", "Diagnostics, Audit & Observability")),
    ("fun",             ("趣味与演示", "Fun & Demos")),
    ("skills",          ("DSH 技能与预设", "DSH Skills")),
    ("ecosystem",       ("官方与生态资源", "Official & Ecosystem")),
    ("uncategorized",   ("其他 / 未分类", "Other / Uncategorized")),
])

VERIFIED_CAT_MAP = {
    "vision": "vision", "web_search": "search_browser", "browser_automation": "search_browser",
    "terminal_ui": "tui", "tui_bridge": "tui",
    "web_ui": "web_ui", "notifications": "web_ui", "conversation_interface": "web_ui",
    "response_presentation": "web_ui", "sidebar_workbench": "web_ui",
    "web_ui_customization": "web_ui", "developer_panel": "web_ui",
    "conversation_sharing": "session_chat", "plan_review": "session_chat",
    "translation": "session_chat", "context_management": "session_chat",
    "long_term_memory": "memory_persona", "prompt_persona": "memory_persona",
    "companion_memory": "memory_persona", "agent_memory_orchestration": "memory_persona",
    "automation": "automation", "task_management": "automation",
    "desktop_automation": "automation", "agent_orchestration": "automation",
    "chat_integration": "communication", "qq_meme_sending": "communication",
    "remote_execution": "remote_device", "device_bridge": "remote_device",
    "computer_use": "remote_device",
    "developer_tooling": "developer_tools", "model_gateway": "developer_tools",
    "plugin_diagnostics": "developer_tools",
    "knowledge_management": "data_tools", "education": "data_tools",
    "deterministic_tools": "data_tools",
    "cost_observability": "diagnostics", "observability": "diagnostics",
    "security_audit": "diagnostics", "session_diagnostics": "diagnostics",
    "skill": "skills", "developer_skills": "skills", "plugin_development_skill": "skills",
    "game": "fun",
}

BRUC3VAN_CAT_MAP = {
    "ui-experience": "web_ui", "media-vision": "vision", "web-browser": "search_browser",
    "agents-workflows": "automation", "knowledge-research": "data_tools",
    "developer-tools": "developer_tools", "utilities": "data_tools",
    "integrations-sharing": "communication", "ecosystem-resources": "ecosystem",
}

ALEX_CAT_MAP = {
    "developer-tools": "developer_tools", "agent-automation": "automation",
    "productivity-collaboration": "session_chat", "data-research-knowledge": "data_tools",
    "cloud-devops-observability": "diagnostics", "ai-design-media": "vision",
    "business-finance-commerce": "uncategorized", "life-devices": "remote_device",
    "media-entertainment": "fun",
}

KEYWORD_RULES = [
    ("vision", ["vision", "ocr", "multimodal", "image", "screenshot", "visual",
                "识图", "视觉", "lmstudio", "看图"]),
    ("tui", ["tui", "terminal ui", "终端界面", "full-screen", "fullscreen", "终端"]),
    ("search_browser", ["search", "browser", "firecrawl", "tavily", "exa",
                        "perplexity", "duckduckgo", "搜索", "浏览器", "webbridge"]),
    ("remote_device", ["ssh", "sftp", "hdc", "computer-use", "计算机使用",
                       "设备", "远程", "device", "harmonyos", "鸿蒙"]),
    ("diagnostics", ["audit", "security", "health", "diagnostic", "审计", "诊断",
                     "安全", "observability", "monitor", "监控", "stats", "统计",
                     "usage", "balance", "余额", "dashboard", "指标"]),
    ("communication", ["lark", "feishu", "飞书", "qq", "telegram", "slack",
                       "discord", "wechat", "微信", "钉钉", "dingtalk", "bot",
                       "notification", "通知", "消息", "channel", "频道"]),
    ("memory_persona", ["memory", "记忆", "persona", "角色", "soul", "prompt",
                        "提示词", "context", "上下文"]),
    ("fun", ["game", "游戏", "emoji", "表情", "meme", "梗", "趣味", "pet",
             "宠物", "whale", "鲸鱼", "gomoku", "五子棋", "ads", "广告"]),
    ("automation", ["automation", "自动化", "workflow", "工作流", "schedule",
                    "定时", "loop", "agent", "代理", "orchestr", "编排",
                    "task", "任务", "sentinel"]),
    ("data_tools", ["csv", "json", "pdf", "docx", "xlsx", "database", "sql",
                    "数据", "文档", "excel", "mineru", "spreadsheet", "表格",
                    "toolkit", "工具集"]),
    ("developer_tools", ["plugin", "plugin", "registry", "注册中心", "cli", "sdk",
                         "dev", "开发", "make-dsh", "doctor", "脚手架", "scaffold",
                         "generator", "skeleton"]),
    ("session_chat", ["session", "会话", "chat", "对话", "conversation", "share",
                      "分享", "translator", "翻译", "wikilink", "annotation",
                      "批注", "nav", "navigation"]),
    ("web_ui", ["ui", "皮肤", "skin", "theme", "主题", "sidebar", "侧栏",
                "panel", "navbar", "界面", "background", "背景", "input",
                "宽", "width", "历史", "history"]),
    ("skills", ["skill", "技能"]),
    ("ecosystem", ["awesome", "hub", "目录", "directory", "list", "列表",
                   "harness", "aggregator"]),
]


def keyword_category(rec):
    if rec.get("full_name") == "deepseek-ai/deepseek-harness":
        return "ecosystem"
    text = " ".join([
        rec.get("full_name") or "",
        rec.get("description") or "",
        " ".join(rec.get("topics") or []),
    ]).lower()
    for cat, kws in KEYWORD_RULES:
        if any(k in text for k in kws):
            return cat
    return "uncategorized"


# --------------------------------------------------------------------------
# markdown link extraction (for README-derived sources)
# --------------------------------------------------------------------------

LINK_RE = re.compile(r"\[([^\]]+)\]\(https?://github\.com/([^/]+/[^/)\s#?]+)")


def extract_md_names(path):
    names = set()
    try:
        text = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        return names
    for label, full in LINK_RE.findall(text):
        full = full.rstrip("/")
        # skip cross-links to aggregator/portal/repo pages
        if full.lower().startswith(("topics/", "awesome-dsh-plugin/", "dsh-external/hub")):
            continue
        if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", full):
            names.add(full)
    return names


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------


def main():
    os.makedirs(SNAP, exist_ok=True)
    merged = {}
    sources_seen = Counter()

    # 1) GitHub search results (richest metadata source)
    for q in SEARCH_QUERIES:
        for k, v in collect_search(q).items():
            if k not in merged:
                merged[k] = {**v, "sources": []}
                sources_seen["github-search"] += 1
            for kw in ("dsh-plugin", "deepseek-harness", "dsh-plugin in:name"):
                if kw in q:
                    merged[k]["sources"].append("topic" if kw.startswith("topic") else "name-search")

    # 2) local snapshots / curated data
    cand_path = os.path.join(ROOT, "data", "dsh-plugin-topic-candidates.csv")
    if os.path.exists(cand_path):
        for row in read_csv(cand_path):
            name = (row.get("repository") or "").strip()
            if not name:
                continue
            k = name.lower()
            if k not in merged:
                merged[k] = {
                    "full_name": name,
                    "html_url": f"https://github.com/{name}",
                    "description": "", "stars": 0, "license": "",
                    "language": "", "topics": [], "pushed_at": "",
                    "homepage": "", "sources": [],
                }
                sources_seen["topic-candidates-snapshot"] += 1
            merged[k]["sources"].append("topic-candidate-snapshot")

    # 3) verified subset (kept flagged; keeps its fine-grained category)
    verified = {}
    verified_key = {}
    vp_path = os.path.join(ROOT, "data", "verified-plugins.csv")
    if os.path.exists(vp_path):
        for row in read_csv(vp_path):
            name = (row.get("repository") or "").strip()
            if not name:
                continue
            k = name.lower()
            verified[name] = row
            verified_key[k] = row
            if k not in merged:
                merged[k] = {
                    "full_name": name,
                    "html_url": row.get("url") or f"https://github.com/{name}",
                    "description": "", "stars": 0, "license": row.get("license") or "",
                    "language": "", "topics": [], "pushed_at": "",
                    "homepage": "", "sources": [],
                }
                sources_seen["verified-plugins"] += 1
            merged[k]["sources"].append("verified")

    # 4) reference awesome lists (download into gitignored snapshot dir)
    ref_names = set()
    for fname, url in RAW_URLS.items():
        dest = os.path.join(SNAP, fname)
        try:
            open(dest, "w", encoding="utf-8").write(fetch(url))
        except Exception as e:  # noqa: BLE001
            print(f"  ! failed to fetch {fname}: {e}")
            continue
        if fname.endswith(".json"):
            j = json.load(open(dest, encoding="utf-8"))
            if fname.startswith("bruc3van"):
                for it in j.get("repositories", []):
                    fn = it.get("full_name") or ""
                    if not fn:
                        continue
                    k = fn.lower()
                    cat = BRUC3VAN_CAT_MAP.get(it.get("category"), "")
                    if k not in merged:
                        lic = it.get("license")
                        lic_spdx = lic.get("spdx_id") if isinstance(lic, dict) else (
                            lic if isinstance(lic, str) else "")
                        merged[k] = {
                            "full_name": fn,
                            "html_url": it.get("html_url") or f"https://github.com/{fn}",
                            "description": (it.get("description") or "").strip(),
                            "stars": it.get("stargazers_count") or 0,
                            "license": lic_spdx,
                            "language": it.get("language") or "",
                            "topics": it.get("topics") or [],
                            "pushed_at": it.get("pushed_at") or "",
                            "homepage": it.get("homepage") or "",
                            "src_cat": cat, "sources": [],
                        }
                        sources_seen["bruc3van"] += 1
                    merged[k]["sources"].append("bruc3van")
                    if not merged[k].get("src_cat") and cat:
                        merged[k]["src_cat"] = cat
            elif fname.startswith("alex"):
                jd = json.load(open(dest, encoding="utf-8"))
                for it in jd.get("plugins", []):
                    url = it.get("url") or ""
                    m = re.search(r"github\.com/([^/]+/[^/)\s#?]+)", url)
                    if not m:
                        continue
                    fn = m.group(1).rstrip("/")
                    k = fn.lower()
                    cat = ALEX_CAT_MAP.get(it.get("category"), "")
                    if k not in merged:
                        merged[k] = {
                            "full_name": fn,
                            "html_url": f"https://github.com/{fn}",
                            "description": (it.get("description") or {}).get("en")
                            or (it.get("description") or {}).get("zh-CN") or "",
                            "stars": 0, "license": "", "language": "",
                            "topics": [], "pushed_at": "", "homepage": "",
                            "src_cat": cat, "sources": [],
                        }
                        sources_seen["alex-yanggg"] += 1
                    merged[k]["sources"].append("alex-yanggg")
                    if not merged[k].get("src_cat") and cat:
                        merged[k]["src_cat"] = cat
        else:
            ref_names |= extract_md_names(dest)

    for fn in ref_names:
        k = fn.lower()
        if k not in merged:
            merged[k] = {
                "full_name": fn, "html_url": f"https://github.com/{fn}",
                "description": "", "stars": 0, "license": "", "language": "",
                "topics": [], "pushed_at": "", "homepage": "", "sources": [],
            }
            sources_seen["awesome-lists-readme"] += 1
        merged[k]["sources"].append("awesome-lists-readme")

    # 5) fill metadata for records lacking API fields
    missing = [k for k, v in merged.items() if not v.get("_meta_ok")]
    print(f"\n{len(merged)} unique records after merge; "
          f"{len(missing)} need API metadata")
    dead = []
    for k in missing:
        v = merged[k]
        data = fetch_repo(v["full_name"])
        if data is None:
            if k in verified_key:
                print(f"  ! WARNING: verified record unresolved ({v['full_name']}), "
                      f"kept as-is")
                continue
            dead.append(k)
            time.sleep(0.4)
            continue
        canon = (data["full_name"] or v["full_name"])
        if canon.lower() != k:
            # repository was renamed/redirected: adopt the canonical name
            merged.pop(k)
            v["full_name"] = canon
            v["html_url"] = data["html_url"] or v["html_url"]
            v["verified"] = k in verified_key
            if canon.lower() in merged:
                merged[canon.lower()]["sources"] = sorted(set(
                    merged[canon.lower()].get("sources", []) + v.get("sources", [])))
                if k in verified_key:
                    merged[canon.lower()]["verified"] = True
            else:
                merged[canon.lower()] = v
        else:
            for field in ("html_url", "description", "stars", "license",
                          "language", "topics", "pushed_at", "homepage"):
                if not v.get(field) and data.get(field):
                    v[field] = data[field]
        time.sleep(0.4)
    for k in dead:
        merged.pop(k, None)
    if dead:
        print(f"  ! dropped {len(dead)} unreachable (404) records: "
              + ", ".join(dead))

    # 6) categorize
    for k, v in merged.items():
        name = v["full_name"]
        cat = ""
        vrow = verified_key.get(k)
        if vrow:
            cat = VERIFIED_CAT_MAP.get(vrow.get("category", ""), "") or \
                VERIFIED_CAT_MAP.get(vrow.get("kind", ""), "")
        if not cat:
            cat = v.get("src_cat") or ""
        v["category"] = cat or keyword_category(v)
        if v["category"] not in CATS:
            v["category"] = "uncategorized"
        v["verified"] = vrow is not None or v.get("verified")

    # 7) write repositories.csv
    fields = ["full_name", "html_url", "description", "category", "stars",
              "license", "language", "topics", "pushed_at", "homepage",
              "verified", "sources"]
    csv_path = os.path.join(ROOT, "data", "repositories.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for v in sorted(merged.values(), key=lambda r: (not r["verified"],
                                                        -r.get("stars", 0),
                                                        r["full_name"].lower())):
            w.writerow({**v, "topics": "|".join(v.get("topics") or []),
                        "sources": "|".join(sorted(set(v.get("sources") or []))),
                        "stars": v.get("stars", 0)})

    # 8) write CATALOG.md
    by_cat = OrderedDict((c, []) for c in CATS)
    for v in merged.values():
        (by_cat.setdefault(v["category"], [])).append(v)

    lines = []
    lines.append("# awesome-dsh-plugins 全量聚合目录 / Full Aggregated Catalog")
    lines.append("")
    lines.append(
        "> 本页聚合了 GitHub `dsh-plugin` / `deepseek-harness` 话题、名称搜索以及多个社区目录中的**全部**"
        "相关仓库。**聚合 ≠ 可装载、可兼容、可安全运行**；`✅` 标记表示该仓库已通过本目录的核验流程（见 "
        "[data/verified-plugins.csv](data/verified-plugins.csv)），其余条目均为未审核候选，用于持续筛选。"
        "本页由 [scripts/aggregate.py](scripts/aggregate.py) 自动生成。")
    lines.append("")
    lines.append("> This page aggregates **every** repository found under the GitHub `dsh-plugin` / "
                  "`deepseek-harness` topics, name search, and several community directories. "
                  "**Aggregation is not a loadability, compatibility, or safety certification.** "
                  "`✅` marks the verified subset "
                  "([data/verified-plugins.csv](data/verified-plugins.csv)); everything else is an unreviewed "
                  "candidate for ongoing screening. Generated by [scripts/aggregate.py](scripts/aggregate.py).")
    total = len(merged)
    verified_n = sum(1 for v in merged.values() if v["verified"])
    lines.append("")
    lines.append(f"**合计 / Total: {total}**（已核验 / Verified: {verified_n}）")
    lines.append("")
    for cat, items in by_cat.items():
        zh, en = CATS[cat]
        lines.append(f"## {zh} / {en} — {len(items)}")
        lines.append("")
        for v in sorted(items, key=lambda r: (not r["verified"], -r.get("stars", 0),
                                              r["full_name"].lower())):
            desc = (v.get("description") or "").strip()
            if not desc:
                desc = "*no description*"
            if len(desc) > 160:
                desc = desc[:157].rstrip() + "…"
            meta = []
            if v.get("stars"):
                meta.append(f"⭐{v['stars']}")
            if v.get("license"):
                meta.append(v["license"])
            if v.get("language"):
                meta.append(v["language"])
            flag = " ✅" if v["verified"] else ""
            meta_s = " · " + " · ".join(meta) if meta else ""
            lines.append(f"- [{v['full_name']}]({v['html_url']}) — {desc}{meta_s}{flag}")
        lines.append("")
    catalog_path = os.path.join(ROOT, "CATALOG.md")
    open(catalog_path, "w", encoding="utf-8").write("\n".join(lines))

    print("\n========== aggregate summary ==========")
    print(f"total unique repositories : {total}")
    print(f"verified (from CSV)       : {verified_n}")
    for src, n in sources_seen.most_common():
        print(f"  unique contributed by {src:<24}: {n}")
    print(f"category distribution     :")
    for cat, items in by_cat.items():
        if items:
            print(f"  {cat:<20} {len(items)}")
    print(f"\nwrote: data/repositories.csv ({total} rows)")
    print(f"wrote: CATALOG.md ({len(lines)} lines)")


if __name__ == "__main__":
    sys.exit(main())