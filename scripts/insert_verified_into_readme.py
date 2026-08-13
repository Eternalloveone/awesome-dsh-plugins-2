#!/usr/bin/env python3
"""
insert_verified_into_readme.py — append newly verified plugin rows from
data/verified-plugins.csv into the verified tables of README.md (简体中文)
and README.en.md (English).

Idempotent: any row whose `[owner/repo](` link is already present in a section
is skipped, so re-running after adding more rows to verified-plugins.csv just
inserts the new ones. Only rows with a non-empty `capability` column are
considered (legacy rows keep their hand-written README text untouched).

Usage: python3 scripts/insert_verified_into_readme.py
"""

import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# canonical category -> section heading per language
CN_SECTIONS = {
    "vision": "### 视觉与多模态",
    "web_ui": "### Web UI、TUI 与开发者体验",
    "tui": "### Web UI、TUI 与开发者体验",
    "fun": "### Web UI、TUI 与开发者体验",
    "session_chat": "## 个性化、会话与内容工作流",
    "memory_persona": "## 个性化、会话与内容工作流",
    "search_browser": "### 搜索、浏览与知识工作流",
    "data_tools": "### 搜索、浏览与知识工作流",
    "automation": "### 自动化、会话、学习与记忆",
    "communication": "### 协作通信、远程执行与可观测性",
    "remote_device": "### 协作通信、远程执行与可观测性",
    "developer_tools": "## 计算机使用、诊断与专项工具",
    "diagnostics": "## 计算机使用、诊断与专项工具",
    "ecosystem": "## 计算机使用、诊断与专项工具",
    "uncategorized": "## 计算机使用、诊断与专项工具",
    "skills": "## DSH 技能与预设",
}
EN_SECTIONS = {
    "vision": "### Vision and multimodal",
    "web_ui": "### Web UI, TUI, and developer experience",
    "tui": "### Web UI, TUI, and developer experience",
    "fun": "### Web UI, TUI, and developer experience",
    "session_chat": "### Web UI, TUI, and developer experience",
    "search_browser": "### Search, browser, automation, and workflow",
    "data_tools": "### Search, browser, automation, and workflow",
    "automation": "### Search, browser, automation, and workflow",
    "memory_persona": "### Search, browser, automation, and workflow",
    "communication": "### Communication, infrastructure, and observability",
    "remote_device": "### Communication, infrastructure, and observability",
    "developer_tools": "### Computer use, diagnostics, and specialist tools",
    "diagnostics": "### Computer use, diagnostics, and specialist tools",
    "ecosystem": "### Computer use, diagnostics, and specialist tools",
    "uncategorized": "### Computer use, diagnostics, and specialist tools",
    "skills": "## DSH skills",
}


def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def insert_rows(text, heading, rows):
    """Insert table rows after the last `|` line of the section headed by
    `heading` (exact match on the trimmed line)."""
    lines = text.split("\n")
    h = next((i for i, l in enumerate(lines) if l.strip() == heading), None)
    if h is None:
        print(f"  ! heading not found: {heading!r}")
        return text, 0
    end = next((j for j in range(h + 1, len(lines))
                if lines[j].strip().startswith("#")), len(lines))
    table_idx = [j for j in range(h + 1, end) if lines[j].strip().startswith("|")]
    if table_idx:
        at = table_idx[-1] + 1
    else:
        at = end  # no table: insert right before the next heading
    lines[at:at] = rows
    return "\n".join(lines), len(rows)


def build_rows(rows, lang):
    out = []
    for r in rows:
        repo = r["repository"]
        cap = esc(r.get("capability"))
        if not cap:
            continue
        install = (r.get("install_or_usage") or "").strip()
        lic = r.get("license") or ""
        caution = esc(r.get("caution"))
        if lang == "cn":
            plain = re.search(r"(see README|见 README)", install)
            inst = install if plain else f"`{install}`"
            lic_txt = "未发现" if lic.lower() in ("not found", "none") else lic
            cell = f"{lic_txt}；{caution}" if caution else licence_text(lic, lang)
        else:
            plain = re.search(r"see README", install, re.I)
            inst = install if plain else f"`{install}`"
            cell = f"{lic}; {caution}" if caution else f"{lic}"
        out.append(f"| [{repo}]({r['url']}) | {cap} | {inst} | {cell} |")
    return out


def licence_text(lic, lang):
    lic = lic or ""
    if lic.lower() in ("not found", "none"):
        return "未发现" if lang == "cn" else "Not found"
    return lic


def main():
    with open(os.path.join(ROOT, "data", "verified-plugins.csv"),
              newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for lang, path, sections in (
        ("cn", os.path.join(ROOT, "README.md"), CN_SECTIONS),
        ("en", os.path.join(ROOT, "README.en.md"), EN_SECTIONS),
    ):
        text = open(path, encoding="utf-8").read()
        inserted_total = 0
        for cat, heading in sections.items():
            cands = [r for r in rows
                     if r.get("capability")
                     and r.get("category") == cat
                     and f"[{r['repository']}](" not in text]
            if not cands:
                continue
            section = text.split("\n")
            # only insert into this section if the repo is not already in the doc
            new_rows = build_rows(cands, lang)
            text, n = insert_rows(text, heading, new_rows)
            inserted_total += n
        open(path, "w", encoding="utf-8").write(text)
        print(f"{path}: inserted {inserted_total} rows")


if __name__ == "__main__":
    sys.exit(main())