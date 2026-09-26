#!/usr/bin/env sh
set -eu

if [ -n "${RUNFILES_MANIFEST_FILE:-}" ] && [ -f "$RUNFILES_MANIFEST_FILE" ]; then
    depfile=$(grep -F '_main/extension_dep_paths.txt ' "$RUNFILES_MANIFEST_FILE" | cut -d ' ' -f 2-)
else
    depfile="${RUNFILES_DIR:-$0.runfiles}/_main/extension_dep_paths.txt"
fi

grep -Fxq 'crypto=@@boringssl+//:crypto' "$depfile"
grep -Fxq 'ssl=@@boringssl+//:ssl' "$depfile"
grep -Fxq 'zlib=@@zlib-ng+//:zlib-ng' "$depfile"
grep -Fxq 'librdkafka=@@librdkafka+//:rdkafka' "$depfile"
