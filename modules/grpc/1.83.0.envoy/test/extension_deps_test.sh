#!/usr/bin/env sh
set -eu

depfile="$1"

grep -Fxq 'crypto=@@boringssl+//:crypto' "$depfile"
grep -Fxq 'ssl=@@boringssl+//:ssl' "$depfile"
grep -Fxq 'zlib=@@zlib-ng+//:zlib-ng' "$depfile"
