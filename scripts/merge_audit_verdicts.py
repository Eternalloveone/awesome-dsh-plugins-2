#!/usr/bin/env python3
"""Merge audit verdict JSON files (from parallel audit agents) into
data/audit-results.csv (append) and data/verified-plugins.csv (append),
de-duplicating on repository name.

Each verdict file must be a JSON array of:
{
  "repo": "owner/name",
  "verdict": "verified_plugin|verified_skill|rejected|watchlist",
  "reason": "one-line summary of the decision",
  "capability": "short CN/EN capability text (used in verified-plugins + README)",
  "install_cmd": "installation/mount command or pointer",
  "license": "SPDX id or 'Not found'",
  "risk_level": "low|medium|high",
  "risk_note": "what data/permissions flow",
  "category": "canonical fine-grained category (e.g. web_ui, vision, automation, skills...)",
  "evidence": "which files were inspected and what was found",
  "caution": "optional caution text",
  "checked_at": "2026-08-14"
}
Usage: python3 scripts/merge_audit_verdicts.py <verdict1.json> [verdict2.json ...]
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_CSV = os.path.join(ROOT, "data", "audit-results.csv")
VERIFIED_CSV = os.path.join(ROOT, "data", "verified-plugins.csv")


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    verdict_files = sys.argv[1:]
    if not verdict_files:
        print("usage: merge_audit_verdicts.py <verdict1.json> [...]")
        return 1

    audit_rows = read_rows(AUDIT_CSV)
    verified_rows = read_rows(VERIFIED_CSV)
    audit_existing = {r["repo"].strip().lower() for r in audit_rows if r.get("repo")}
    verified_existing = {r["repository"].strip().lower() for r in verified_rows if r.get("repository")}

    audit_fields = list(audit_rows[0].keys())
    verified_fields = list(verified_rows[0].keys())

    new_audit = []
    new_verified = []
    seen = set()
    for vf in verdict_files:
        with open(vf, encoding="utf-8") as f:
            verdicts = json.load(f)
        for v in verdicts:
            repo = (v.get("repo") or "").strip()
            if not repo or repo.lower() in seen:
                continue
            seen.add(repo.lower())
            if repo.lower() in audit_existing:
                continue
            verdict = v.get("verdict", "rejected")
            verified = verdict in ("verified_plugin", "verified_skill")
            kind = "dsh_skill_or_preset" if verdict == "verified_skill" else "installable_dsh_plugin"
            audit_rows.append({
                "repo": repo,
                "verdict": verdict,
                "reason": v.get("reason", ""),
                "capability": v.get("capability", ""),
                "install_cmd": v.get("install_cmd", ""),
                "license": v.get("license", ""),
                "risk_level": v.get("risk_level", ""),
                "risk_note": v.get("risk_note", ""),
                "category": v.get("category", ""),
                "evidence": v.get("evidence", ""),
                "checked_at": v.get("checked_at", "2026-08-14"),
            })
            new_audit.append(repo)
            if verified and repo.lower() not in verified_existing:
                verified_rows.append({
                    "repository": repo,
                    "url": f"https://github.com/{repo}",
                    "kind": kind,
                    "category": v.get("category", ""),
                    "install_or_usage": v.get("install_cmd", ""),
                    "license": v.get("license", ""),
                    "last_activity": v.get("last_activity", ""),
                    "verification_status": "verified",
                    "risk_level": v.get("risk_level", ""),
                    "verification_source": v.get("evidence", ""),
                    "checked_at": v.get("checked_at", "2026-08-14"),
                    "capability": v.get("capability", ""),
                    "caution": v.get("caution", ""),
                })
                new_verified.append(repo)

    with open(AUDIT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=audit_fields)
        w.writeheader()
        w.writerows(audit_rows)
    with open(VERIFIED_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=verified_fields)
        w.writeheader()
        w.writerows(verified_rows)

    print(f"audit rows added    : {len(new_audit)} (total {len(audit_rows) - 1})")
    print(f"verified rows added : {len(new_verified)} (total {len(verified_rows) - 1})")


if __name__ == "__main__":
    sys.exit(main())