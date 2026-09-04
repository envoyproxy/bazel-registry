#!/usr/bin/env python3
"""Audit version skew between envoy's WORKSPACE pins and this registry.

Reads `bazel/repository_locations.bzl` and `api/bazel/repository_locations.bzl`
from envoy at a given SHA, compares each entry against the current version of
the matching module in this registry, and prints a markdown report.

Usage: python3 docs/audit/workspace_skew.py --envoy-sha <sha> [> report.md]
"""

import argparse
import ast
import base64
import datetime
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

RAW = "https://raw.githubusercontent.com/envoyproxy/envoy/{sha}/{path}"
GH_API = "https://api.github.com"
BCR = "https://bcr.bazel.build/modules/{name}/metadata.json"
SPECS = ("bazel/repository_locations.bzl", "api/bazel/repository_locations.bzl")
MODULE_FILES = {
    "root": "MODULE.bazel",
    "api": "api/MODULE.bazel",
    "docs": "docs/MODULE.bazel",
    "mobile": "mobile/MODULE.bazel",
    "examples": "examples/filter-cc/MODULE.bazel",
    "examples-wasm": "examples/wasm-cc/MODULE.bazel",
}
GH_REPO_RE = re.compile(r"https://(?:codeload\.)?github\.com/([^/]+)/([^/]+)/")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REF_RES = (
    re.compile(r"/archive/refs/tags/(.+?)\.(?:tar\.gz|zip|tar\.xz)$"),
    re.compile(r"/archive/(.+?)\.(?:tar\.gz|zip|tar\.xz)$"),
    re.compile(r"/releases/download/([^/]+)/"),
    re.compile(r"/tar\.gz/refs/tags/(.+)$"),
)


def fetch(url, token=None):
    req = urllib.request.Request(url, headers={"User-Agent": "workspace-skew-audit"})
    if token and url.startswith(GH_API):
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError) as e:
        if not isinstance(e, urllib.error.HTTPError):
            print(f"warning: fetch failed {url}: {e}", file=sys.stderr)
        return None


def literal(node):
    """Evaluate the `dict(...)`/list/str subset used by repository_locations.bzl."""
    if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "dict":
        return {kw.arg: literal(kw.value) for kw in node.keywords}
    return ast.literal_eval(node)


def parse_spec(src):
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and node.targets[0].id == "REPOSITORY_LOCATIONS_SPEC":
            return literal(node.value)
    return {}


def workspace_deps(sha, token):
    deps = {}
    for path in SPECS:
        src = fetch(RAW.format(sha=sha, path=path), token)
        if src is None:
            sys.exit(f"error: cannot fetch {path} at {sha}")
        for name, spec in parse_spec(src).items():
            version = spec["version"]
            urls = [u.replace("{version}", version) for u in spec["urls"]]
            deps.setdefault(name, dict(
                name=name, version=version, sha256=spec.get("sha256", ""),
                url=urls[0], side="api" if path.startswith("api/") else "root"))
    return deps


def registry_modules(root):
    mods = {}
    for meta_path in sorted(pathlib.Path(root, "modules").glob("*/metadata.json")):
        meta = json.loads(meta_path.read_text())
        versions = meta.get("versions") or []
        if not versions:
            continue
        version = versions[-1]
        src_path = meta_path.parent / version / "source.json"
        source = json.loads(src_path.read_text()) if src_path.exists() else {}
        mods[meta_path.parent.name] = dict(
            name=meta_path.parent.name, version=version, url=source.get("url", ""),
            integrity=source.get("integrity", ""), patched=bool(
                source.get("patches") or source.get("overlay")),
            repository=(meta.get("repository") or [""])[0])
    return mods


def gh_repo(url):
    m = GH_REPO_RE.match(url or "")
    return (m.group(1).lower(), m.group(2).lower()) if m else None


def norm(name):
    name = re.sub(r"^(com|org|io|dev|net)_(github|google|googlesource|bazel|envoyproxy)_", "", name)
    name = re.sub(r"^(com|org|io|dev|net)_", "", name)
    return name.replace("-", "").replace("_", "").replace(".", "").lower()


def ref_of(url):
    for regex in REF_RES:
        m = regex.search(url or "")
        if m:
            return m.group(1)
    return None


def sri(hexdigest):
    try:
        return "sha256-" + base64.b64encode(bytes.fromhex(hexdigest)).decode()
    except ValueError:
        return ""


def version_tuple(ref):
    parts = re.findall(r"\d+", ref or "")
    return tuple(int(p) for p in parts) if parts else None


def compare(org, repo, base, head, token, cache):
    """GitHub compare base...head -> (status, count, base_date, head_date)."""
    key = (org, repo, base, head)
    if key in cache:
        return cache[key]
    raw = fetch(f"{GH_API}/repos/{org}/{repo}/compare/{base}...{head}", token)
    result = (None, None, None, None)
    if raw:
        data = json.loads(raw)
        status, commits = data.get("status"), data.get("commits") or []
        count = data.get("ahead_by") if status == "ahead" else data.get("behind_by")
        base_date = (data.get("base_commit") or {}).get("commit", {}).get("committer", {}).get("date")
        head_date = commits[-1]["commit"]["committer"]["date"] if commits else None
        result = (status, count, base_date, head_date)
    cache[key] = result
    return result


def short(ref, date=None):
    ref = ref or "?"
    out = ref[:7] if SHA_RE.match(ref) else ref
    return f"{out} ({date[:10]})" if date else out


def classify(ws, reg, token, cache, budget):
    """Return (status, delta string) for a mapped workspace/registry pair."""
    if ws["url"] == reg["url"]:
        if not reg["integrity"] or reg["integrity"] == sri(ws["sha256"]):
            return "match", ""
        return "hash-mismatch", f"workspace `{sri(ws['sha256'])}` vs registry `{reg['integrity']}`"
    ws_ref, reg_ref = ref_of(ws["url"]), ref_of(reg["url"])
    org_repo = gh_repo(ws["url"])
    if ws_ref and reg_ref and SHA_RE.match(ws_ref) and SHA_RE.match(reg_ref) and org_repo:
        if budget and budget[0] > 0:
            budget[0] -= 1
            status, count, reg_date, ws_date = compare(*org_repo, reg_ref, ws_ref, token, cache)
            if status == "ahead":
                return "registry-behind", (f"{count} commits", short(ws_ref, ws_date), short(reg_ref, reg_date))
            if status == "behind":
                status2, count2, ws_date2, reg_date2 = compare(
                    *org_repo, ws_ref, reg_ref, token, cache)
                return "registry-ahead", (f"{count2 or count} commits",
                                          short(ws_ref, ws_date2), short(reg_ref, reg_date2))
            if status == "identical":
                return "unordered", ("same commit, different url", short(ws_ref), short(reg_ref))
        return "unordered", ("not compared (github budget)", short(ws_ref), short(reg_ref))
    if ws_ref and reg_ref and SHA_RE.match(ws_ref or "") and ws_ref.startswith(reg_ref):
        return "unordered", ("same commit (registry url uses a short sha)",
                             short(ws_ref), reg_ref)
    ws_v, reg_v = version_tuple(ws_ref), version_tuple(reg_ref)
    if ws_v and reg_v and bool(SHA_RE.match(ws_ref or "")) == bool(SHA_RE.match(reg_ref or "")):
        if reg_v < ws_v:
            return "registry-behind", ("version bump", short(ws_ref), short(reg_ref))
        if reg_v > ws_v:
            return "registry-ahead", ("version bump", short(ws_ref), short(reg_ref))
        return "unordered", ("same version, different url", short(ws_ref), short(reg_ref))
    # tag on one side, commit on the other: fall back to the registry module version
    ws_v = version_tuple(re.match(r"[\d.]*", (ws["version"] or "")).group(0))
    reg_v = version_tuple(re.match(r"[\d.]*", reg["version"].split("-")[0]).group(0))
    if ws_v and reg_v:
        label = f"module version {reg['version']} vs workspace {ws['version']}"
        if reg_v < ws_v:
            return "registry-behind", (label, short(ws_ref), short(reg_ref))
        if reg_v > ws_v:
            return "registry-ahead", (label, short(ws_ref), short(reg_ref))
        return "unordered", (f"same version ({ws['version']}), registry pins a commit",
                             short(ws_ref), short(reg_ref))
    return "unordered", ("not orderable", short(ws_ref), short(reg_ref))


def in_bcr(name):
    return fetch(BCR.format(name=name)) is not None


def table(rows, header):
    if not rows:
        return "_none_\n"
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in sorted(rows)]
    return "\n".join(out) + "\n"


def report(args):
    token = os.environ.get("GITHUB_TOKEN")
    ws_deps = workspace_deps(args.envoy_sha, token)
    modules = registry_modules(args.registry_root)
    bazel_deps, aliases = {}, {}
    for label, path in MODULE_FILES.items():
        src = fetch(RAW.format(sha=args.envoy_sha, path=path), token)
        for call in re.findall(r"bazel_dep\([^)]*\)", src or ""):
            name = re.search(r'name\s*=\s*"([^"]+)"', call).group(1)
            bazel_deps.setdefault(name, []).append(label)
            repo_name = re.search(r'repo_name\s*=\s*"([^"]+)"', call)
            aliases[norm(repo_name.group(1) if repo_name else name)] = name

    by_repo = {}
    by_norm = {}
    for mod in modules.values():
        repo = gh_repo(mod["url"]) or gh_repo((mod["repository"] or "").replace(
            "github:", "https://github.com/") + "/")
        if repo:
            by_repo.setdefault(repo, []).append(mod["name"])
        by_norm.setdefault(norm(mod["name"]), mod["name"])

    pairs, unmapped, siblings = {}, [], {}
    for name, ws in sorted(ws_deps.items()):
        candidates = by_repo.get(gh_repo(ws["url"]), [])
        mod = next((c for c in candidates if modules[c]["url"] == ws["url"]), None)
        mod = mod or next((c for c in candidates if norm(c) == norm(name)), None)
        mod = mod or (candidates[0] if candidates else by_norm.get(norm(name)))
        for other in candidates:
            if other != mod:
                siblings[other] = name
        if mod and mod not in pairs:
            pairs[mod] = ws
        elif not mod:
            unmapped.append(ws)

    cache, budget = {}, [args.max_github]
    buckets = {k: [] for k in (
        "match", "registry-behind", "registry-ahead", "hash-mismatch", "unordered")}
    for mod, ws in sorted(pairs.items()):
        status, delta = classify(ws, modules[mod], token, cache, budget)
        used = "yes" if "root" in bazel_deps.get(mod, []) else "no"
        if status == "match":
            buckets[status].append((mod, ws["version"], modules[mod]["version"]))
        elif status == "hash-mismatch":
            buckets[status].append((mod, ws["url"], delta))
        else:
            buckets[status].append((mod, delta[1], delta[2], delta[0], used))

    registry_only, workspace_only = [], []
    for name, mod in sorted(modules.items()):
        if name in pairs:
            continue
        repo = gh_repo(mod["url"]) or ("", "")
        source = ("envoy-owned" if repo[0] in ("envoyproxy", "envoy")
                  else "envoy-patched upstream" if mod["patched"] or ".envoy" in mod["version"]
                  else "upstream mirror")
        if name in siblings:
            source += f" (same upstream as WORKSPACE `{siblings[name]}`)"
        registry_only.append((name, mod["version"], source, ", ".join(bazel_deps.get(name, [])) or "-"))
    no_repo = []
    for ws in sorted(unmapped, key=lambda w: w["name"]):
        repo = gh_repo(ws["url"])
        candidates = [ws["name"], ws["name"].replace("_", "-"), norm(ws["name"])]
        candidates += [repo[1], repo[1].replace("_", "-")] if repo else []
        candidates += [aliases[n] for n in (norm(ws["name"]), norm(repo[1]) if repo else "")
                       if n in aliases]
        bcr = next((c for c in candidates if in_bcr(c)), None)
        if not repo and not bcr:
            no_repo.append((ws["name"], ws["version"], f"{ws['side']} spec", ws["url"]))
            continue
        note = "BCR module, not mirrored here" if bcr else "no registry module and not in BCR"
        workspace_only.append((ws["name"], ws["version"], bcr or "no",
                               f"{note}; {ws['side']} spec"))

    counts = {k: len(v) for k, v in buckets.items()}
    counts["registry-only"] = len(registry_only)
    counts["workspace-only"] = len(workspace_only)
    counts["unmapped"] = len(no_repo)
    skew_header = ["module", "WORKSPACE", "registry", "delta", "in envoy MODULE.bazel?"]
    print(f"""# WORKSPACE ↔ registry version skew audit

envoy @ {args.envoy_sha} ({args.date})
registry @ {args.registry_sha}

## Summary
{table([(k, v) for k, v in counts.items()], ["status", "count"])}
## registry-behind  ← fix these
{table(buckets["registry-behind"], skew_header)}
## registry-ahead  ← WORKSPACE should catch up, or registry was bumped deliberately
{table(buckets["registry-ahead"], skew_header)}
## hash-mismatch  ← investigate immediately
{table(buckets["hash-mismatch"], ["module", "url", "integrity"])}
## unordered
{table(buckets["unordered"], skew_header)}
## registry-only
{table(registry_only, ["module", "registry version", "source", "used by"])}
## workspace-only
{table(workspace_only, ["WORKSPACE name", "version", "in BCR?", "note"])}
## unmapped
{table(no_repo, ["WORKSPACE name", "version", "spec", "url"])}
## match
<details>

{table(buckets["match"], ["module", "WORKSPACE version", "registry version"])}
</details>

## Method
Generated by `docs/audit/workspace_skew.py --envoy-sha {args.envoy_sha}`.
WORKSPACE entries come from `bazel/repository_locations.bzl` + `api/bazel/repository_locations.bzl`
(parsed with `ast`, `{{version}}` resolved in urls); registry entries are the last
`versions` entry of each `modules/*/metadata.json` plus its `source.json`.
Mapping is by upstream `github.com/<org>/<repo>` first, then normalised name; `match` means
identical url *and* WORKSPACE sha256 == registry SRI integrity. Git-SHA skew is measured with
the GitHub compare API (cap {args.max_github} calls, {args.max_github - budget[0]} used);
`bazel_dep` usage is read from envoy's root/api/docs/mobile/examples `MODULE.bazel`.
""")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--envoy-sha", required=True)
    parser.add_argument("--registry-root", default=".")
    parser.add_argument("--registry-sha", default="HEAD")
    parser.add_argument("--date", default=datetime.date.today().isoformat())
    parser.add_argument("--max-github", type=int, default=30,
                        help="cap on GitHub compare API calls")
    report(parser.parse_args())


if __name__ == "__main__":
    main()
