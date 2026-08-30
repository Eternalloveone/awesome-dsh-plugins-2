#!/usr/bin/env python3
"""Validate review JSON and merge one curator batch into all catalog CSVs.

The review set must exactly match ``above_floor`` from ``--topic-repos``. All
four tables are validated and built in memory before temporary files are
published. A failed validation never changes the catalog.
"""

import argparse
import csv
import datetime as dt
import io
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = ROOT / "data"
DEFAULT_SUMMARY = Path("/tmp/dsh_merge_summary.json")
STAR_FLOOR = 10

VERDICTS = {
    "verified_plugin", "verified_skill", "watchlist", "related", "rejected",
}
VERDICT_ALIASES = {
    "verified": "verified_plugin",
    "skill": "verified_skill",
    "excluded": "rejected",
}
RISK_LEVELS = {"low", "medium", "high"}
KINDS = {"installable_dsh_plugin", "dsh_skill", "cordis_bundle", "other"}
REVIEW_FIELDS = {
    "repo", "verdict", "main_dir", "reason", "description", "capability",
    "category", "kind", "install_or_usage", "license", "language",
    "homepage", "dsh_load_path", "risk_level", "risk_note", "topics",
    "pushed_at", "evidence", "caution", "checked_at",
}
REVIEW_CATEGORIES = {
    "ui", "vision", "automation", "desktop", "memory", "mcp",
    "agent_orchestration", "developer_tools", "data_tools", "security",
    "chat_integration", "skills", "launcher", "list", "legal", "other",
}
TABLES = {
    "repositories": ("repositories.csv", "full_name"),
    "candidates": ("dsh-plugin-topic-candidates.csv", "repository"),
    "audit": ("audit-results.csv", "repo"),
    "verified": ("verified-plugins.csv", "repository"),
}
TABLE_FIELDS = {
    "repositories": [
        "full_name", "html_url", "description", "category", "stars",
        "license", "language", "topics", "pushed_at", "homepage",
        "verified", "sources",
    ],
    "candidates": ["repository", "topic", "review_status"],
    "audit": [
        "repo", "verdict", "reason", "capability", "install_cmd",
        "license", "risk_level", "risk_note", "category", "evidence",
        "checked_at",
    ],
    "verified": [
        "repository", "url", "kind", "category", "install_or_usage",
        "license", "last_activity", "verification_status", "risk_level",
        "verification_source", "checked_at", "capability", "caution",
    ],
}


class MergeError(ValueError):
    """A validation error that must leave the catalog untouched."""


def clean(value):
    if value is None:
        return ""
    text = str(value).strip()
    return "" if text.upper() == "N/A" else text


def normalize_repo(value):
    repo = clean(value).strip("/")
    prefix = "https://github.com/"
    if repo.startswith(prefix):
        repo = repo[len(prefix):].strip("/")
    parts = repo.split("/")
    if len(parts) != 2 or any(not part for part in parts):
        raise MergeError(f"invalid repository name: {value!r}")
    return repo


def normalize_bool(value, field, repo):
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.strip().lower() in {"true", "yes"}:
        return True
    if isinstance(value, str) and value.strip().lower() in {"false", "no"}:
        return False
    raise MergeError(f"{repo}: {field} must be a boolean")


def normalize_topics(value, repo):
    if value in (None, ""):
        return []
    if isinstance(value, str):
        parts = value.replace(",", "|").split("|")
    elif isinstance(value, list):
        parts = value
    else:
        raise MergeError(f"{repo}: topics must be an array or delimited string")
    return sorted({clean(item) for item in parts if clean(item)})


def require(review, field, repo):
    value = clean(review.get(field))
    if not value:
        raise MergeError(f"{repo}: missing required field {field!r}")
    return value


def normalize_date(value, field, repo, required=False):
    text = clean(value)
    if not text:
        if required:
            raise MergeError(f"{repo}: missing required field {field!r}")
        return ""
    try:
        dt.date.fromisoformat(text[:10])
    except ValueError as exc:
        raise MergeError(f"{repo}: {field} must start with an ISO date") from exc
    return text


def load_topic_repos(path):
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("above_floor"), list):
        raise MergeError("--topic-repos must contain an above_floor array")
    stars = {}
    display = {}
    for item in payload["above_floor"]:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise MergeError(f"invalid above_floor item: {item!r}")
        repo = normalize_repo(item[0])
        key = repo.lower()
        if key in stars:
            raise MergeError(f"duplicate above_floor repository: {repo}")
        try:
            count = int(item[1])
        except (TypeError, ValueError) as exc:
            raise MergeError(f"{repo}: invalid star count {item[1]!r}") from exc
        if count <= STAR_FLOOR:
            raise MergeError(f"{repo}: above_floor star count must be > {STAR_FLOOR}")
        stars[key] = count
        display[key] = repo
    return stars, display


def load_reviews(paths):
    reviews = []
    for path in paths:
        with open(path, encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, list):
            raise MergeError(f"{path}: expected a top-level JSON array")
        reviews.extend(payload)
    return reviews


def normalize_review(review, stars_by_repo):
    if not isinstance(review, dict):
        raise MergeError(f"review must be an object, got {type(review).__name__}")
    fields = set(review)
    if fields != REVIEW_FIELDS:
        raise MergeError(
            "review fields mismatch: "
            f"missing={sorted(REVIEW_FIELDS - fields)}, "
            f"extra={sorted(fields - REVIEW_FIELDS)}"
        )

    repo = normalize_repo(review.get("repo"))
    key = repo.lower()
    if key not in stars_by_repo:
        raise MergeError(f"{repo}: not present in above_floor")

    raw_verdict = require(review, "verdict", repo).lower()
    verdict = VERDICT_ALIASES.get(raw_verdict, raw_verdict)
    if verdict not in VERDICTS:
        raise MergeError(f"{repo}: invalid verdict {raw_verdict!r}")
    main_dir = normalize_bool(review.get("main_dir"), "main_dir", repo)
    verified = verdict in {"verified_plugin", "verified_skill"}
    if main_dir != verified:
        raise MergeError(
            f"{repo}: main_dir must be {str(verified).lower()} for verdict {verdict}"
        )

    risk_level = require(review, "risk_level", repo).lower()
    if risk_level not in RISK_LEVELS:
        raise MergeError(f"{repo}: invalid risk_level {risk_level!r}")
    category = require(review, "category", repo).lower()
    if category not in REVIEW_CATEGORIES:
        raise MergeError(f"{repo}: invalid category {category!r}")
    kind = clean(review.get("kind")).lower()
    if kind and kind not in KINDS:
        raise MergeError(f"{repo}: invalid kind {kind!r}")
    if verified and not kind:
        raise MergeError(f"{repo}: verified entries require kind")

    pushed_at = normalize_date(review.get("pushed_at"), "pushed_at", repo)
    if verified and not pushed_at:
        raise MergeError(f"{repo}: verified entries require pushed_at")
    checked_at = normalize_date(
        review.get("checked_at"), "checked_at", repo, required=True
    )
    install_or_usage = clean(review.get("install_or_usage"))
    dsh_load_path = clean(review.get("dsh_load_path"))
    if verified and not dsh_load_path:
        raise MergeError(f"{repo}: verified entries require dsh_load_path")
    dsh_load_path = dsh_load_path or "N/A"
    if verified and not install_or_usage:
        raise MergeError(f"{repo}: verified entries require install_or_usage")
    if verified and dsh_load_path.lower().startswith(("no", "n/a")):
        raise MergeError(f"{repo}: verified entries require a positive dsh_load_path")

    return {
        "repo": repo,
        "repo_key": key,
        "stars": stars_by_repo[key],
        "verdict": verdict,
        "main_dir": main_dir,
        "reason": require(review, "reason", repo),
        "description": require(review, "description", repo),
        "capability": require(review, "capability", repo),
        "category": category,
        "kind": kind,
        "install_or_usage": install_or_usage,
        "license": clean(review.get("license")) or "Not found",
        "language": clean(review.get("language")),
        "homepage": clean(review.get("homepage")),
        "dsh_load_path": dsh_load_path,
        "risk_level": risk_level,
        "risk_note": require(review, "risk_note", repo),
        "topics": normalize_topics(review.get("topics"), repo),
        "pushed_at": pushed_at,
        "evidence": require(review, "evidence", repo),
        "caution": clean(review.get("caution")),
        "checked_at": checked_at,
    }


def read_table(path, key_field, expected_fields):
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected_fields:
            raise MergeError(
                f"{path}: header mismatch; expected {expected_fields!r}, "
                f"got {reader.fieldnames!r}"
            )
        rows = list(reader)
    seen = set()
    for row in rows:
        key = clean(row.get(key_field)).lower()
        if not key:
            raise MergeError(f"{path}: row with empty {key_field}")
        if key in seen:
            raise MergeError(f"{path}: duplicate key {key!r}")
        seen.add(key)
    return rows


def append_or_validate(rows, key_field, new_row, fields, table_name):
    key = clean(new_row[key_field]).lower()
    existing = next(
        (row for row in rows if clean(row.get(key_field)).lower() == key), None
    )
    if existing is None:
        rows.append(new_row)
        return True
    conflicts = [
        field for field in fields
        if clean(existing.get(field)).lower() != clean(new_row.get(field)).lower()
    ]
    if conflicts:
        raise MergeError(
            f"{table_name}: existing {new_row[key_field]} conflicts in "
            f"{', '.join(conflicts)}"
        )
    return False


def build_outputs(data_dir, reviews):
    table_data = {}
    for table_name, (filename, key_field) in TABLES.items():
        existing_rows = read_table(
            data_dir / filename, key_field, TABLE_FIELDS[table_name]
        )
        table_data[table_name] = {
            "rows": existing_rows,
            "existing_count": len(existing_rows),
        }

    added = {name: 0 for name in TABLES}
    for item in reviews:
        repo = item["repo"]
        url = f"https://github.com/{repo}"
        audit_row = {
            "repo": repo,
            "verdict": item["verdict"],
            "reason": item["reason"],
            "capability": item["capability"],
            "install_cmd": item["install_or_usage"],
            "license": item["license"],
            "risk_level": item["risk_level"],
            "risk_note": item["risk_note"],
            "category": item["category"],
            "evidence": item["evidence"],
            "checked_at": item["checked_at"],
        }
        if append_or_validate(
            table_data["audit"]["rows"], "repo", audit_row,
            TABLE_FIELDS["audit"], "audit-results.csv",
        ):
            added["audit"] += 1

        candidate_row = {
            "repository": repo,
            "topic": "dsh-plugin",
            "review_status": item["verdict"],
        }
        if append_or_validate(
            table_data["candidates"]["rows"], "repository", candidate_row,
            TABLE_FIELDS["candidates"], "dsh-plugin-topic-candidates.csv",
        ):
            added["candidates"] += 1

        if not item["main_dir"]:
            continue

        repository_row = {
            "full_name": repo,
            "html_url": url,
            "description": item["description"],
            "category": item["category"],
            "stars": str(item["stars"]),
            "license": item["license"],
            "language": item["language"],
            "topics": "|".join(item["topics"]),
            "pushed_at": item["pushed_at"],
            "homepage": item["homepage"],
            "verified": "True",
            "sources": "agent-review|topic-new|verified",
        }
        if append_or_validate(
            table_data["repositories"]["rows"], "full_name", repository_row,
            TABLE_FIELDS["repositories"], "repositories.csv",
        ):
            added["repositories"] += 1

        verified_row = {
            "repository": repo,
            "url": url,
            "kind": item["kind"],
            "category": item["category"],
            "install_or_usage": item["install_or_usage"],
            "license": item["license"],
            "last_activity": item["pushed_at"][:10],
            "verification_status": (
                "skill" if item["verdict"] == "verified_skill" else "verified"
            ),
            "risk_level": item["risk_level"],
            "verification_source": item["evidence"],
            "checked_at": item["checked_at"],
            "capability": item["capability"],
            "caution": item["caution"],
        }
        if append_or_validate(
            table_data["verified"]["rows"], "repository", verified_row,
            TABLE_FIELDS["verified"], "verified-plugins.csv",
        ):
            added["verified"] += 1
    return table_data, added


def write_csv(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        handle.flush()
        os.fsync(handle.fileno())


def write_csv_preserving_existing(path, original, fields, rows, existing_count):
    """Keep legacy CSV bytes intact and append new rows with LF endings."""
    original_bytes = original.read_bytes()
    appended = rows[existing_count:]
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writerows(appended)
    appended_bytes = buffer.getvalue().encode("utf-8")
    with path.open("wb") as handle:
        handle.write(original_bytes)
        if appended_bytes and original_bytes and not original_bytes.endswith((b"\n", b"\r")):
            handle.write(b"\n")
        handle.write(appended_bytes)
        handle.flush()
        os.fsync(handle.fileno())


def validate_staged(path, key_field, fields, expected_rows):
    rows = read_table(path, key_field, fields)
    if len(rows) != expected_rows:
        raise MergeError(
            f"{path}: staged row count {len(rows)} != expected {expected_rows}"
        )


def commit_outputs(data_dir, table_data):
    backup_dir = Path(tempfile.mkdtemp(prefix="dsh-curator-backup-", dir="/tmp"))
    staged = {}
    originals = {}
    try:
        for table_name, (filename, key_field) in TABLES.items():
            original = data_dir / filename
            originals[table_name] = original
            shutil.copy2(original, backup_dir / filename)
            fd, staged_name = tempfile.mkstemp(
                prefix=f".{filename}.", suffix=".tmp", dir=data_dir
            )
            os.close(fd)
            staged_path = Path(staged_name)
            staged[table_name] = staged_path
            write_csv_preserving_existing(
                staged_path,
                original,
                TABLE_FIELDS[table_name],
                table_data[table_name]["rows"],
                table_data[table_name]["existing_count"],
            )
            validate_staged(
                staged_path, key_field, TABLE_FIELDS[table_name],
                len(table_data[table_name]["rows"]),
            )
            shutil.copymode(original, staged_path)

        replaced = []
        try:
            for table_name in TABLES:
                os.replace(staged[table_name], originals[table_name])
                replaced.append(table_name)
        except Exception:
            for table_name in replaced:
                filename = TABLES[table_name][0]
                shutil.copy2(backup_dir / filename, originals[table_name])
            raise
    finally:
        for staged_path in staged.values():
            if staged_path.exists():
                staged_path.unlink()
    return backup_dir


def write_summary(path, payload):
    target = os.path.abspath(os.fspath(path))
    directory = os.path.dirname(target) or "."
    fd, temporary = tempfile.mkstemp(
        prefix=f".{os.path.basename(target)}.", suffix=".tmp", dir=directory
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic-repos", required=True,
                        help="diff_topic.py output containing above_floor")
    parser.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR))
    parser.add_argument("--summary", default=str(DEFAULT_SUMMARY))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("verdict_files", nargs="*",
                        help="review JSON array files")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        stars_by_repo, display = load_topic_repos(args.topic_repos)
        raw_reviews = load_reviews(args.verdict_files)
        reviews = []
        seen = set()
        for raw_review in raw_reviews:
            review = normalize_review(raw_review, stars_by_repo)
            if review["repo_key"] in seen:
                raise MergeError(f"duplicate review result: {review['repo']}")
            seen.add(review["repo_key"])
            reviews.append(review)

        expected = set(stars_by_repo)
        if seen != expected:
            missing = [display[key] for key in sorted(expected - seen)]
            extra = sorted(seen - expected)
            raise MergeError(
                f"review set mismatch: missing={missing or []}, extra={extra or []}"
            )

        data_dir = Path(args.data_dir).resolve()
        table_data, added = build_outputs(data_dir, reviews)
        summary = {
            "ok": True,
            "dry_run": args.dry_run,
            "reviewed": len(reviews),
            "verdicts": {
                verdict: sum(item["verdict"] == verdict for item in reviews)
                for verdict in sorted(VERDICTS)
            },
            "rows_added": added,
            "backup_dir": None,
        }
        if not args.dry_run and any(added.values()):
            summary["backup_dir"] = str(commit_outputs(data_dir, table_data))
        write_summary(args.summary, summary)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, MergeError) as exc:
        error_summary = {"ok": False, "error": str(exc)}
        try:
            write_summary(args.summary, error_summary)
        except OSError:
            pass
        print(f"merge failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
