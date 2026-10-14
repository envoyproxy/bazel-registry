#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHECK_SCRIPT="${SCRIPT_DIR}/registry_immutability.sh"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TEMP_DIR}"' EXIT

new_repo() {
    local name="$1"
    REPO="${TEMP_DIR}/${name}"
    mkdir -p "${REPO}/modules/foo/1.0"
    git -C "${REPO}" init -q
    git -C "${REPO}" config user.name "Registry test"
    git -C "${REPO}" config user.email "registry-test@example.com"
    cat > "${REPO}/modules/foo/1.0/source.json" <<'EOF'
{"url":"https://example.com/foo-1.0.tar.gz"}
EOF
    cat > "${REPO}/modules/foo/metadata.json" <<'EOF'
{
    "versions": ["1.0"],
    "yanked_versions": {},
    "homepage": "https://example.com",
    "maintainers": []
}
EOF
    git -C "${REPO}" add modules
    git -C "${REPO}" commit -qm "published baseline"
    git -C "${REPO}" tag v0.0.1
}

commit_changes() {
    git -C "${REPO}" add -A
    git -C "${REPO}" commit -qm "test change"
}

update_metadata() {
    local filter="$1"
    local metadata="${REPO}/modules/foo/metadata.json"
    jq "${filter}" "${metadata}" > "${metadata}.tmp"
    mv "${metadata}.tmp" "${metadata}"
}

run_case() {
    local name="$1"
    local expected_status="$2"
    local expected_text="${3:-}"
    local baseline="${4:-v0.0.1}"
    local output
    local status

    if output="$(cd "${REPO}" && bash "${CHECK_SCRIPT}" "${baseline}" 2>&1)"; then
        status=0
    else
        status=$?
    fi
    if [[ "${status}" -ne "${expected_status}" ]]; then
        echo "FAILED: ${name}: expected exit ${expected_status}, got ${status}" >&2
        echo "${output}" >&2
        return 1
    fi
    if [[ -n "${expected_text}" ]] && ! grep -Fq -- "${expected_text}" <<< "${output}"; then
        echo "FAILED: ${name}: expected output containing ${expected_text}" >&2
        echo "${output}" >&2
        return 1
    fi
    echo "ok: ${name}"
}

new_repo unchanged
run_case "unchanged fast path" 0 "modules/ unchanged since v0.0.1"

new_repo new-module
mkdir -p "${REPO}/modules/bar/2.0"
printf '%s\n' '{"url":"https://example.com/bar-2.0.tar.gz"}' > "${REPO}/modules/bar/2.0/source.json"
printf '%s\n' '{"versions":["2.0"],"yanked_versions":{}}' > "${REPO}/modules/bar/metadata.json"
commit_changes
run_case "new module added" 0

new_repo new-version
mkdir -p "${REPO}/modules/foo/2.0"
printf '%s\n' '{"url":"https://example.com/foo-2.0.tar.gz"}' > "${REPO}/modules/foo/2.0/source.json"
update_metadata '.versions += ["2.0"]'
commit_changes
run_case "new version added" 0

new_repo add-yank
update_metadata '.yanked_versions["1.0"] = "no longer supported"'
commit_changes
run_case "yank added" 0

new_repo metadata-fields
update_metadata '.homepage = "https://new.example.com" | .maintainers = [{"name":"New Maintainer"}]'
commit_changes
run_case "other metadata changed" 0

new_repo modify-version
printf '%s\n' '{"url":"https://example.com/changed.tar.gz"}' > "${REPO}/modules/foo/1.0/source.json"
commit_changes
run_case "published version modified" 1 "::error::modules/foo/1.0 was published in v0.0.1 and has been modified:"

new_repo add-version-file
printf '%s\n' "patch" > "${REPO}/modules/foo/1.0/fix.patch"
commit_changes
run_case "file added to published version" 1 "::error::modules/foo/1.0 was published in v0.0.1 and has been modified:"

new_repo delete-version
rm -rf "${REPO}/modules/foo/1.0"
commit_changes
run_case "published version deleted" 1 "::error::modules/foo/1.0 was published in v0.0.1 and has been removed"

new_repo remove-version-entry
update_metadata '.versions = []'
commit_changes
run_case "published version removed from metadata" 1 "::error::modules/foo/metadata.json: published entries removed:"

new_repo remove-yank
update_metadata '.yanked_versions["1.0"] = "already yanked"'
git -C "${REPO}" add modules/foo/metadata.json
git -C "${REPO}" commit -qm "published yank"
git -C "${REPO}" tag -f v0.0.1
update_metadata '.yanked_versions = {}'
commit_changes
run_case "yank removed from metadata" 1 "::error::modules/foo/metadata.json: published entries removed:"

new_repo delete-module
rm -rf "${REPO}/modules/foo"
commit_changes
run_case "published module deleted" 1 "::error::modules/foo/metadata.json was published in v0.0.1 and has been removed"

new_repo latest-release-wins
rm -rf "${REPO}/modules/foo"
commit_changes
git -C "${REPO}" tag v0.0.2
mkdir -p "${REPO}/modules/foo/1.0"
printf '%s\n' '{"url":"https://example.com/replacement.tar.gz"}' > "${REPO}/modules/foo/1.0/source.json"
printf '%s\n' '{"versions":["1.0"],"yanked_versions":{}}' > "${REPO}/modules/foo/metadata.json"
commit_changes
run_case "dropped by latest release can be re-added" 0 "" v0.0.2

new_repo multiple-violations
update_metadata '.yanked_versions["1.0"] = "temporarily yanked"'
commit_changes
git -C "${REPO}" tag -f v0.0.1
printf '%s\n' '{"url":"https://example.com/changed.tar.gz"}' > "${REPO}/modules/foo/1.0/source.json"
update_metadata '.versions = [] | .yanked_versions = {}'
commit_changes
output="$(cd "${REPO}" && bash "${CHECK_SCRIPT}" v0.0.1 2>&1)" && status=0 || status=$?
if [[ "${status}" -ne 1 ]] \
    || ! grep -Fq "::error::modules/foo/1.0 was published in v0.0.1 and has been modified:" <<< "${output}" \
    || ! grep -Fq "::error::modules/foo/metadata.json: published entries removed:" <<< "${output}"; then
    echo "FAILED: multiple violations are all reported" >&2
    echo "${output}" >&2
    exit 1
fi
echo "ok: multiple violations are all reported"
