#!/usr/bin/env bash

set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "Usage: $0 <published-ref> [head-ref]" >&2
    exit 2
fi

BASE="$1"
HEAD_REF="${2:-HEAD}"
errors=0

if [[ "$(git rev-parse "${BASE}:modules")" == "$(git rev-parse "${HEAD_REF}:modules")" ]]; then
    echo "modules/ unchanged since ${BASE}"
    exit 0
fi

while IFS= read -r path; do
    base_tree="$(git rev-parse "${BASE}:${path}")"
    head_tree="$(git rev-parse -q --verify "${HEAD_REF}:${path}" 2>/dev/null || true)"
    if [[ -z "${head_tree}" ]]; then
        echo "::error::${path} was published in ${BASE} and has been removed"
        errors=1
    elif [[ "${base_tree}" != "${head_tree}" ]]; then
        echo "::error::${path} was published in ${BASE} and has been modified:"
        git diff --stat "${BASE}" "${HEAD_REF}" -- "${path}" | sed 's/^/    /'
        errors=1
    fi
done < <(git ls-tree -r -d --name-only "${BASE}" modules | awk -F/ 'NF==3')

while IFS= read -r metadata; do
    if ! git cat-file -e "${HEAD_REF}:${metadata}" 2>/dev/null; then
        echo "::error::${metadata} was published in ${BASE} and has been removed"
        errors=1
        continue
    fi

    base_json="$(git show "${BASE}:${metadata}")"
    head_json="$(git show "${HEAD_REF}:${metadata}")"
    missing="$(jq -nr \
        --argjson base "${base_json}" \
        --argjson head "${head_json}" '
        (($base.versions // []) - ($head.versions // [])) as $versions
        | ((($base.yanked_versions // {}) | keys)
            - (($head.yanked_versions // {}) | keys)) as $yanked
        | ($versions | map("versions entry \(.)"))
            + ($yanked | map("yanked_versions[\(.)]"))
        | .[]')"
    if [[ -n "${missing}" ]]; then
        echo "::error::${metadata}: published entries removed:"
        sed 's/^/    /' <<< "${missing}"
        errors=1
    fi
done < <(git ls-tree -r --name-only "${BASE}" modules | grep '/metadata.json$' || true)

exit "${errors}"
