import csv
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scanner = load_module(
    "dsh_full_topic_scan",
    ROOT / ".workbuddy/skills/dsh-topic-curator/scripts/full_topic_scan.py",
)
merger = load_module("dsh_merge_audit_verdicts", ROOT / "scripts/merge_audit_verdicts.py")
aggregate = load_module("dsh_aggregate", ROOT / "scripts/aggregate.py")
docs = load_module("dsh_generate_docs", ROOT / "scripts/generate_docs.py")


class ScannerTests(unittest.TestCase):
    def test_actionable_plan_excludes_low_star_history(self):
        plan = scanner.build_plan(actionable_only=True)
        self.assertEqual(len(plan), len(scanner.STAR_TIERS))
        self.assertTrue(all(not is_split for _, _, is_split in plan))

    def test_full_plan_covers_pre_2025_history(self):
        labels = {label for label, _, _ in scanner.build_plan()}
        self.assertIn("<=10 2008", labels)
        self.assertIn("<=10 2024", labels)
        self.assertIn("<=10 2025-01", labels)

    def test_retryable_eof_is_retried(self):
        responses = [
            SimpleNamespace(returncode=1, stdout="", stderr="Get API: EOF"),
            SimpleNamespace(returncode=0, stdout="7\n", stderr=""),
        ]
        with (
                mock.patch.object(scanner.subprocess, "run", side_effect=responses) as run,
                mock.patch.object(scanner.time, "sleep"),
        ):
            output, error = scanner._gh("topic:dsh-plugin", ".total_count")
        self.assertEqual(output, "7\n")
        self.assertEqual(error, "")
        self.assertEqual(run.call_count, 2)

    def test_failed_run_overwrites_old_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            summary = tmp_path / "summary.json"
            out = tmp_path / "full.json"
            compat = tmp_path / "compat.json"
            summary.write_text(json.dumps({"coverage_ok": True}), encoding="utf-8")
            with mock.patch.object(scanner, "gh_total", return_value=(-1, "network")), \
                    mock.patch.object(scanner.time, "sleep"):
                rc = scanner.main([
                    "--execute", "--actionable-only", "--summary", str(summary),
                    "--out", str(out), "--compat", str(compat),
                ])
            payload = json.loads(summary.read_text(encoding="utf-8"))
            self.assertEqual(rc, 2)
            self.assertFalse(payload["coverage_ok"])
            self.assertEqual(payload["status"], "failed")
            self.assertEqual(len(payload["failures"]), len(scanner.STAR_TIERS))

    def test_zero_count_actionable_run_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            summary = tmp_path / "summary.json"
            with mock.patch.object(scanner, "gh_total", return_value=(0, "")), \
                    mock.patch.object(scanner.time, "sleep"):
                rc = scanner.main([
                    "--execute", "--actionable-only", "--summary", str(summary),
                    "--out", str(tmp_path / "full.json"),
                    "--compat", str(tmp_path / "compat.json"),
                ])
            payload = json.loads(summary.read_text(encoding="utf-8"))
            self.assertEqual(rc, 0)
            self.assertTrue(payload["coverage_ok"])
            self.assertEqual(
                payload["stats"]["completed_partitions"], len(scanner.STAR_TIERS)
            )


class MergeTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tempdir.name)
        self.data_dir = self.base / "data"
        self.data_dir.mkdir()
        for table_name, (filename, _) in merger.TABLES.items():
            with (self.data_dir / filename).open("w", newline="", encoding="utf-8") as handle:
                csv.DictWriter(handle, fieldnames=merger.TABLE_FIELDS[table_name]).writeheader()

    def tearDown(self):
        self.tempdir.cleanup()

    def review(self, repo, verdict="verified_plugin", main_dir=True):
        verified = verdict in {"verified_plugin", "verified_skill"}
        return {
            "repo": repo,
            "verdict": verdict,
            "main_dir": main_dir,
            "reason": "Primary evidence inspected",
            "description": "Fixture repository",
            "capability": "Fixture capability",
            "category": "ui" if verified else "other",
            "kind": "installable_dsh_plugin" if verified else "other",
            "install_or_usage": "dsh plugin --profile web add fixture" if verified else "",
            "license": "MIT",
            "language": "Python",
            "homepage": "",
            "dsh_load_path": "package.json dsh.bundle" if verified else "No native path",
            "risk_level": "low",
            "risk_note": "Local fixture only",
            "topics": ["dsh-plugin"],
            "pushed_at": "2026-08-29T00:00:00Z",
            "evidence": "README, package.json, and cordis.patch.yml",
            "caution": "",
            "checked_at": "2026-08-30",
        }

    def run_merge(self, repos, reviews):
        topic = self.base / "topic.json"
        review = self.base / "reviews.json"
        summary = self.base / "summary.json"
        topic.write_text(json.dumps({"above_floor": repos, "skipped": []}), encoding="utf-8")
        review.write_text(json.dumps(reviews), encoding="utf-8")
        rc = merger.main([
            "--topic-repos", str(topic), "--data-dir", str(self.data_dir),
            "--summary", str(summary), str(review),
        ])
        return rc, json.loads(summary.read_text(encoding="utf-8"))

    def rows(self, table_name):
        filename = merger.TABLES[table_name][0]
        with (self.data_dir / filename).open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def test_valid_batch_updates_all_four_tables(self):
        rc, payload = self.run_merge(
            [["owner/plugin", 20], ["owner/related", 12]],
            [self.review("owner/plugin"), self.review("owner/related", "related", False)],
        )
        self.assertEqual(rc, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(len(self.rows("repositories")), 1)
        self.assertEqual(len(self.rows("verified")), 1)
        self.assertEqual(len(self.rows("candidates")), 2)
        self.assertEqual(len(self.rows("audit")), 2)
        if payload.get("backup_dir"):
            shutil.rmtree(payload["backup_dir"])

    def test_missing_review_fails_without_mutation(self):
        before = {
            filename: (self.data_dir / filename).read_bytes()
            for filename, _ in merger.TABLES.values()
        }
        rc, payload = self.run_merge(
            [["owner/one", 20], ["owner/two", 15]],
            [self.review("owner/one")],
        )
        after = {
            filename: (self.data_dir / filename).read_bytes()
            for filename, _ in merger.TABLES.values()
        }
        self.assertEqual(rc, 2)
        self.assertFalse(payload["ok"])
        self.assertEqual(after, before)


class GeneratorTests(unittest.TestCase):
    def test_render_only_does_not_need_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            data.mkdir()
            fields = [
                "full_name", "html_url", "description", "category", "stars",
                "license", "language", "topics", "pushed_at", "homepage",
                "verified", "sources",
            ]
            with (data / "repositories.csv").open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow({
                    "full_name": "owner/plugin", "html_url": "",
                    "description": "Fixture", "category": "ui", "stars": "N/A",
                    "license": "MIT", "language": "Python", "topics": "dsh-plugin",
                    "pushed_at": "", "homepage": "", "verified": "True",
                    "sources": "fixture",
                })
            catalog = root / "CATALOG.md"
            with mock.patch.object(aggregate, "ROOT", root), \
                    mock.patch.object(aggregate, "fetch") as fetch:
                rc = aggregate.main(["--render-only"])
            self.assertEqual(rc, 0)
            fetch.assert_not_called()
            self.assertIn("owner/plugin", catalog.read_text(encoding="utf-8"))

    def test_current_verified_categories_are_mapped(self):
        _, _, unmapped, _, _ = docs.load()
        self.assertEqual(unmapped, [])


if __name__ == "__main__":
    unittest.main()
