#!/usr/bin/env python3
"""Tests for registry_select.py."""

import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import registry_select


class RegistrySelectTest(unittest.TestCase):

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.modules_root = pathlib.Path(self._tmpdir.name) / "modules"
        self.add_module("foo", ["1.0.envoy", "2.0.envoy"])
        self.add_module("bar", ["3.0.envoy"])
        # Version listed in metadata without a version directory
        # (mirrored upstream entry).
        self.add_module("baz", ["0.9", "1.1.envoy"], dirs=["1.1.envoy"])

    def add_module(self, name, versions, dirs=None):
        module_dir = self.modules_root / name
        module_dir.mkdir(parents=True)
        (module_dir / "metadata.json").write_text(
            json.dumps({"versions": versions}))
        for version in (versions if dirs is None else dirs):
            (module_dir / version).mkdir()

    def select(self, event, changed_files=(), **kwargs):
        return registry_select.select(
            event, list(changed_files), self.modules_root, **kwargs)

    @property
    def latest_all(self):
        return {
            ("foo", "2.0.envoy"),
            ("bar", "3.0.envoy"),
            ("baz", "1.1.envoy")}

    def test_testable_versions_latest_is_last_entry(self):
        self.assertEqual(
            registry_select.testable_versions(["2.0", "1.0.envoy"]),
            ["1.0.envoy"])
        self.assertEqual(registry_select.testable_versions([]), [])

    def test_pr_module_change_runs_changed_only(self):
        self.assertEqual(
            self.select(
                "pull_request",
                ["modules/foo/1.0.envoy/source.json"]),
            {("foo", "1.0.envoy")})

    def test_pr_all_relevant_path_classes_run(self):
        for path in (
                "modules/foo/1.0.envoy/source.json",
                "modules/foo/1.0.envoy/MODULE.bazel",
                "modules/foo/1.0.envoy/presubmit.yml",
                "modules/foo/1.0.envoy/patches/fix.patch",
                "modules/foo/1.0.envoy/overlay/BUILD.bazel",
                "modules/foo/1.0.envoy/test_module/BUILD.bazel"):
            self.assertEqual(
                self.select("pull_request", [path]),
                {("foo", "1.0.envoy")},
                path)

    def test_pr14_test_module_file_set_selects_liburing_pair(self):
        self.add_module("liburing", ["2.15.envoy"])
        self.assertEqual(
            self.select(
                "pull_request",
                [
                    "modules/liburing/2.15.envoy/test_module/MODULE.bazel",
                    "modules/liburing/2.15.envoy/test_module/BUILD.bazel",
                    "modules/liburing/2.15.envoy/test_module/liburing_test.cc",
                ]),
            {("liburing", "2.15.envoy")})

    def test_pr_metadata_only_change_skips(self):
        self.assertEqual(
            self.select("pull_request", ["modules/foo/metadata.json"]),
            set())

    def test_pr_irrelevant_version_file_skips(self):
        self.assertEqual(
            self.select(
                "pull_request",
                ["modules/foo/1.0.envoy/README.md"]),
            set())

    def test_pr_deleted_version_skips(self):
        self.assertEqual(
            self.select(
                "pull_request",
                ["modules/foo/9.9.envoy/source.json"]),
            set())

    def test_pr_non_module_paths_skip(self):
        self.assertEqual(
            self.select("pull_request", ["README.md", "VERSION"]),
            set())

    def test_pr_infra_change_fans_out(self):
        for path in (
                ".github/workflows/bazel-registry.yml",
                ".github/workflows/_bazel_registry.yml",
                ".github/workflows/registry_integrity.sh",
                ".github/workflows/registry_select.py",
                "verify/verify.sh"):
            self.assertEqual(
                self.select("pull_request", [path]),
                self.latest_all,
                path)

    def test_pr_infra_change_includes_module_changes(self):
        self.assertEqual(
            self.select(
                "pull_request",
                ["verify/verify.sh", "modules/foo/1.0.envoy/source.json"]),
            self.latest_all | {("foo", "1.0.envoy")})

    def test_push_runs_latest_plus_changed(self):
        self.assertEqual(
            self.select("push", ["modules/foo/1.0.envoy/source.json"]),
            self.latest_all | {("foo", "1.0.envoy")})

    def test_push_no_changes_runs_latest(self):
        self.assertEqual(self.select("push"), self.latest_all)

    def test_schedule_runs_latest_only(self):
        self.assertEqual(self.select("schedule"), self.latest_all)

    def test_dispatch_module_and_version(self):
        self.assertEqual(
            self.select(
                "workflow_dispatch", module="foo", version="1.0.envoy"),
            {("foo", "1.0.envoy")})

    def test_dispatch_module_only_runs_latest_of_module(self):
        self.assertEqual(
            self.select("workflow_dispatch", module="foo"),
            {("foo", "2.0.envoy")})

    def test_dispatch_no_inputs_runs_latest_of_every_module(self):
        self.assertEqual(
            self.select("workflow_dispatch"),
            self.latest_all)

    def test_no_diff_basis_yields_no_changed_files(self):
        self.assertEqual(registry_select.git_changed_files("", "HEAD"), [])
        self.assertEqual(
            registry_select.git_changed_files("0" * 40, "HEAD"), [])

    def test_invalid_diff_basis_fails(self):
        with self.assertRaises(RuntimeError):
            registry_select.git_changed_files("f" * 40, "HEAD")


if __name__ == "__main__":
    unittest.main()
