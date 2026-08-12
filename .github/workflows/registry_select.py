#!/usr/bin/env python3
"""Select which {module, version} pairs registry CI should run.

Selection rules:

  trigger                  what runs
  -----------------------  ------------------------------------------------
  PR, module change        changed {module, version} only
  PR, infra change         latest of every module (+ any module changes)
  push (postsubmit)        latest of every module + changed-and-not-latest
  schedule (nightly)       latest of every module
  workflow_dispatch        requested module/version (latest of every module
                           if no module given, latest of the module if no
                           version given)

Diff basis:
  push  ->  the pushed range (`before..after`)
  PR    ->  merge base of `pull_request.base.sha` and HEAD

"latest" is the last entry in `metadata.json` `versions` - the array is
append-only so order is insertion order. The `.envoy` suffix is not
semver-comparable, so no sorting is attempted.

Path-class gating - a change under `modules/<mod>/<version>/` only counts
when it touches `source.json`, `MODULE.bazel`, `presubmit.yml`,
`patches/**` or `overlay/**`. A `metadata.json`-only change is skipped.

Infra changes (`verify/**`, the workflows) must fan out to the latest of
every module - otherwise a PR breaking the harness produces an empty
changed-modules diff and green-lights itself.

Output is a compact JSON array of `{"module": ..., "version": ...}`
objects, suitable for a GitHub Actions matrix `include`.
"""

import argparse
import json
import pathlib
import subprocess
import sys


INFRA_PREFIXES = (
    ".github/workflows/",
    "verify/",
)

# Files/dirs under modules/<mod>/<version>/ that affect what gets
# fetched, patched or built. Anything else (eg metadata.json, which
# lives at the module level) does not trigger verification.
RELEVANT_FILES = (
    "MODULE.bazel",
    "presubmit.yml",
    "source.json",
)
RELEVANT_DIRS = (
    "overlay",
    "patches",
    "test_module",
)


def testable_versions(versions):
    """Versions of a module that the full fan-out should exercise.

    Currently just the latest (last entry - `versions` is append-only).
    Single place to widen the set later, eg to fold in active
    non-latest versions pinned by release branches.
    """
    return list(versions[-1:])


def load_versions(modules_root, module):
    metadata = pathlib.Path(modules_root) / module / "metadata.json"
    return json.loads(metadata.read_text())["versions"]


def latest_of_every_module(modules_root):
    pairs = set()
    for metadata in sorted(pathlib.Path(modules_root).glob("*/metadata.json")):
        for version in testable_versions(json.loads(metadata.read_text())["versions"]):
            pairs.add((metadata.parent.name, version))
    return pairs


def infra_changed(changed_files):
    return any(
        path.startswith(INFRA_PREFIXES)
        for path in changed_files)


def changed_pairs(changed_files, modules_root):
    """Changed {module, version} pairs, path-class gated.

    Only pairs whose version directory still exists are returned -
    a deleted version cannot be checked.
    """
    root = pathlib.Path(modules_root).name
    pairs = set()
    for path in changed_files:
        parts = path.split("/")
        if len(parts) < 4 or parts[0] != root:
            continue
        module, version = parts[1], parts[2]
        changed = parts[3]
        if changed not in RELEVANT_FILES and changed not in RELEVANT_DIRS:
            continue
        if not (pathlib.Path(modules_root) / module / version).is_dir():
            continue
        pairs.add((module, version))
    return pairs


def is_all_zeros_sha(value):
    value = value.strip()
    return len(value) == 40 and set(value) == {"0"}


def git_changed_files(base, head, *, use_merge_base=False):
    """Changed files between base and head.

    Empty base and the all-zeros SHA sentinel mean there is no usable diff
    basis (eg branch creation push), so an empty changed set is returned.
    Any other resolution/diff failure is fatal.
    """
    if not base or is_all_zeros_sha(base):
        # No usable diff basis (eg branch creation push).
        return []
    diff_base = base
    if use_merge_base:
        merge_base = subprocess.run(
            ["git", "merge-base", base, head],
            capture_output=True,
            text=True)
        if merge_base.returncode != 0:
            raise RuntimeError(
                f"ERROR: unable to resolve merge base between {base} and {head}: "
                f"{merge_base.stderr.strip()}")
        diff_base = merge_base.stdout.strip()
        if not diff_base:
            raise RuntimeError(
                f"ERROR: merge base between {base} and {head} is empty")
    # Pushes intentionally diff `before..after` (pushed range). PRs diff
    # `merge_base(base, head)..head` via the branch above.
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{diff_base}..{head}"],
        capture_output=True,
        text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"ERROR: unable to diff {diff_base}..{head}: "
            f"{proc.stderr.strip()}")
    return [line for line in proc.stdout.splitlines() if line]


def select(event, changed_files, modules_root, module="", version=""):
    if event == "schedule":
        return latest_of_every_module(modules_root)
    if event == "workflow_dispatch":
        if not module:
            return latest_of_every_module(modules_root)
        if version:
            return {(module, version)}
        return {
            (module, v)
            for v in testable_versions(load_versions(modules_root, module))}
    changed = changed_pairs(changed_files, modules_root)
    if event == "push" or infra_changed(changed_files):
        return latest_of_every_module(modules_root) | changed
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--event",
        required=True,
        choices=["pull_request", "push", "schedule", "workflow_dispatch"])
    parser.add_argument("--base", default="")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--module", default="")
    parser.add_argument("--version", default="")
    parser.add_argument("--modules-root", default="modules")
    args = parser.parse_args()
    try:
        changed_files = (
            git_changed_files(
                args.base,
                args.head,
                use_merge_base=(args.event == "pull_request"))
            if args.event in ("pull_request", "push")
            else [])
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
    selected = select(
        args.event,
        changed_files,
        args.modules_root,
        module=args.module,
        version=args.version)
    json.dump(
        [
            {"module": module, "version": version}
            for module, version in sorted(selected)
        ],
        sys.stdout,
        separators=(",", ":"))


if __name__ == "__main__":
    main()
