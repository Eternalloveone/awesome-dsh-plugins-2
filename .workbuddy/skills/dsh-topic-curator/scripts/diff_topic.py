#!/usr/bin/env python3
"""Diff a GitHub `dsh-plugin` topic page dump against the local catalog CSVs.

Usage:
    python3 diff_topic.py <topic_repos.json> --catalog-dir data --star-floor 10

<topic_repos.json> format (one combined list across all scraped pages):
    [
      {"name": "owner/repo", "stars": 725},
      {"name": "owner/repo2", "stars": 13}
    ]

Behavior:
    - Loads repositories.csv and dsh-plugin-topic-candidates.csv from --catalog-dir.
    - Reports repos NOT present in either file (deduped, lowercased by name).
    - Splits into "above_floor" (stars > floor, to process) and "skipped"
      (stars <= floor, per the "10 个 star 内的先不处理" rule).
    - Writes /tmp/dsh_new_repos.json for downstream merging.

The default floor is 10: repos with stars <= 10 are skipped. To include 10-star
repos, pass --star-floor 9.
"""
import csv
import json
import argparse


def load_existing(catalog_dir):
    existing, cand = set(), set()
    with open(f"{catalog_dir}/repositories.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            existing.add(row["full_name"].strip().lower())
    with open(f"{catalog_dir}/dsh-plugin-topic-candidates.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cand.add(row["repository"].strip().lower())
    return existing, cand


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repos_json", help="JSON file of {name, stars} topic repos")
    ap.add_argument("--catalog-dir", default="data")
    ap.add_argument("--star-floor", type=int, default=10,
                    help="skip repos with stars <= floor (default 10)")
    args = ap.parse_args()

    with open(args.repos_json, encoding="utf-8") as f:
        data = json.load(f)

    existing, cand = load_existing(args.catalog_dir)

    seen = {}
    for r in data:
        seen.setdefault(r["name"].lower(), (r["name"], int(r["stars"])))

    new = [(n, s) for n, s in seen.values()
           if n.lower() not in existing and n.lower() not in cand]
    above = sorted([(n, s) for n, s in new if s > args.star_floor], key=lambda x: -x[1])
    skipped = sorted([(n, s) for n, s in new if s <= args.star_floor], key=lambda x: -x[1])

    print(f"Total unique topic repos: {len(seen)}")
    print(f"Already in catalog:      {len(seen) - len(new)}")
    print(f"NEW (not in catalog):    {len(new)}")
    print(f"\n=== NEW above floor (stars > {args.star_floor}): {len(above)} ===")
    for n, s in above:
        print(f"  {s:>6}  {n}")
    print(f"\n=== Skipped (stars <= {args.star_floor}, per floor): {len(skipped)} ===")
    for n, s in skipped:
        print(f"  {s:>6}  {n}")

    with open("/tmp/dsh_new_repos.json", "w", encoding="utf-8") as f:
        json.dump({"above_floor": above, "skipped": skipped}, f,
                  ensure_ascii=False, indent=2)
    print("\nWrote /tmp/dsh_new_repos.json")


if __name__ == "__main__":
    main()
