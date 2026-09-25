#!/usr/bin/env sh
set -eu

if [ -n "${RUNFILES_MANIFEST_FILE:-}" ] && [ -f "$RUNFILES_MANIFEST_FILE" ]; then
    depfile=$(grep -F '_main/extension_dep_paths.txt ' "$RUNFILES_MANIFEST_FILE" | cut -d ' ' -f 2-)
else
    depfile="${RUNFILES_DIR:-$0.runfiles}/_main/extension_dep_paths.txt"
fi

grep -Fq 'external/librdkafka+' "$depfile"
grep -Fq 'external/boringssl+' "$depfile"
grep -Fq 'external/zlib-ng+' "$depfile"
