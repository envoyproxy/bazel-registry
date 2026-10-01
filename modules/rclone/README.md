# rclone

This module wraps the [rclone](https://rclone.org) prebuilt binaries as a
Bazel module, so consumers can depend on `@rclone//:rclone` instead of an
ad-hoc `http_archive` + `use_repo_rule` in their own `MODULE.bazel`.

The `source.json` points at the small, stable rclone *source* tarball (used
only for its `strip_prefix`); the overlaid `MODULE.bazel` declares one
`http_archive` per supported platform (`linux-amd64`, `linux-arm64`,
`osx-amd64`, `osx-arm64`), and the overlaid `BUILD.bazel` exposes
`@rclone//:rclone` as a `select()` alias that resolves to the archive
matching the target platform. Bazel only fetches the archive for the
platform actually selected (lazy repo fetching).

## Bumping the version

1. Update `strip_prefix` and the `integrity` of the source tarball in
   `source.json` (`https://github.com/rclone/rclone/archive/refs/tags/v<version>.tar.gz`).
2. Update the four platform zip `sha256` values in `MODULE.bazel` (both the
   copy at `<version>/MODULE.bazel` and `<version>/overlay/MODULE.bazel`,
   which must stay in sync aside from their file-specific header comments)
   from `https://downloads.rclone.org/v<version>/SHA256SUMS`.
3. Recompute the `integrity` of `overlay/BUILD.bazel` and
   `overlay/MODULE.bazel` in `source.json`
   (`openssl dgst -sha256 -binary <file> | base64`).
4. Add the new version to `metadata.json`'s `versions` list.
