# Module audit (pre-v0.0.1)

Generated 2026-09-22 against registry commit `4856b11055b8d56f564d6d70552ae047f2b99a86`.

## Summary

- 80 modules total
- 1 unused (no consumer): `rclone`
- 0 could be replaced by BCR drop-in: none found
- 2 in BCR but fork reason unclear: `libcircllhist`, `zipkin-api`
- 35 release-pinned and behind upstream: `aws-c-auth-testdata` (0.10.4 → v1.0.0), `boringssl-fips` (0.20260413.0 → 0.20260813.0), `boringssl-source` (0.20260413.0 → 0.20260813.0), `cel-cpp` (0.14.0 → v0.16.1), `dd-trace-cpp` (2.1.1 → v2.2.0), `elfutils` (0.195 → 0.196), `go-fips` (1.24.12 → 1.27.1), `grpc` (1.83.0 → v1.84.0), `icu` (78.2 → release-78.3), `ipp-crypto` (2.2.0 → v2.3.0), `kafka` (3.9.2 → 4.3.1), `libmaxminddb` (1.13.3 → 1.14.1), `librdkafka` (2.6.0 → v2.15.1), `msgpack-cxx` (7.0.0 → cpp-9.0.0), `nghttp2` (1.66.0 → v1.70.0), `openssl` (3.5.7 → openssl-4.0.2), `perfetto` (57.2 → v58.2), `prometheus-metrics-model` (0.6.2 → v0.6.3), `protobuf` (35.1.bcr → v36.2), `qatlib` (26.02.0 → 26.08.0), `qatzip` (1.3.2 → v2.0.0), `rclone` (1.70.3 → v1.75.1), `rules_apple` (3.20.1 → 5.1.0), `rules_rust` (0.69.0 → 0.74.0), `rules_swift` (2.5.0 → 4.1.1), `simdutf` (8.1.0 → v9.2.0), `skywalking-data-collect-protocol` (10.4.0 → v11.0.0), `sq` (1.4.0 → v1.4.1), `toolchains_llvm` (1.9.0 → v1.9.1), `uadk` (2.9 → v2.11), `v8` (14.6.202.10 → 15.6.39-pgo), `wamr` (2.4.4 → WAMR-2.4.5), `wasmtime` (45.0.2 → v49.0.0), `yq.bzl` (0.1.1 → v0.4.0), `zlib-ng` (2.3.2 → 2.3.3)
- 4 commit-pinned where an upstream tag is now available: `emsdk` (c0bb220 (2026-01-10) → 6.0.10 (2026-09-21)), `hermetic-android-toolchains` (c6a9f20 (2026-08-07) → 0.4.0 (2026-09-09)), `proxy-wasm-rust-sdk` (5283e57 (2025-12-05) → v0.2.5 (2026-05-20)), `vpp-vcl` (85abefb (2026-01-11) → v26.06 (2026-06-21))
- 2 pre-release pins with a stable now available: `libevent` (2.2.2-alpha → release-2.1.13-stable), `wuffs` (0.4.0-alpha.9 → v0.3.5)

## Recommendations

Before `v0.0.1`:

- Remove `rclone` unless a consumer is added first; it is the only orphan in the current graph.
- Resolve the two exact-version BCR duplicates with unclear value (`libcircllhist`, `zipkin-api`): either switch to BCR or document the Envoy-specific requirement before freezing them.
- Replace commit pins that already have post-pin tags (`emsdk`, `hermetic-android-toolchains`, `proxy-wasm-rust-sdk`, `vpp-vcl`); `vpp-vcl` still also has a `-dev` version string.
- Decide whether the pre-release pins (`libevent`, `wuffs`) are acceptable to freeze as-is.

Can wait:

- Larger version-refresh work for still-used modules that are behind upstream (`librdkafka`, `wasmtime`, `rules_swift`, `rules_apple`, `protobuf`, `kafka`, `qatzip`, `v8`, etc.) should be coordinated with Envoy/main rather than done piecemeal here.
- Upstream/BCR publishing work for not-in-BCR modules that already ship `MODULE.bazel` at HEAD (`dd-trace-cpp`, `googleurl`, `hessian2-codec`, `perfetto`, `quiche`, `v8`, `hermetic-android-toolchains`, plus the Envoy-owned repos) can happen after the initial registry freeze.

## Per-module detail

| module | version | pin type | pinned (tag/sha + date) | latest upstream | status | consumers | BCR? | why fork / notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `aws-c-auth-testdata` | `0.10.4.envoy` | release | `0.10.4` | `v1.0.0` | envoy, major-behind | envoy, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `bazel-compdb` | `0.0.0-20220906-4086479.envoy` | commit | `4086479 (2022-09-06)` | `0.5.2 (2021-09-10)` | envoy, commit-pinned | envoy, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `boost.headers` | `1.89.0.envoy` | release | `1.89.0` | `unknown` | envoy, unknown | envoy, hyperscan, envoy main, vectorscan | bcr-exists-but-fork-justified<br>boost.headers: 1.89.0.bcr.2, 1.90.0.bcr.1 | No matching BCR version. 1 patch(es): add_build_file.patch |
| `boringssl-fips` | `0.20260413.0.envoy` | release | `0.20260413.0` | `0.20260813.0` | envoy, minor-behind | envoy, envoy main | bcr-exists-but-fork-justified<br>boringssl: 0.0.0-20211025-d4f1ab9, 0.0.0-20230215-5c22014, 0.0.0-20240126-22d349c, 0.0.0-20240530-2db0eb3, 0.20240913.0, 0.20240930.0, 0.20241024.0, 0.20241209.0, 0.20250114.0, 0.20250212.0, 0.20250311.0, 0.20250415.0, 0.20250514.0, 0.20250701.0, 0.20250807.0, 0.20250818.0, 0.20251002.0, 0.20251110.0, 0.20251124.0, 0.20260204.0, 0.20260211.0, 0.20260327.0, 0.20260413.0, 0.20260508.0, 0.20260526.0, 0.20260616.0, 0.20260713.0, 0.20260730.0, 0.20260803.0, 0.20260813.0 | Uses the same upstream boringssl release as BCR but publishes a separate FIPS-flavoured wrapper with a go-fips dependency. |
| `boringssl-source` | `0.20260413.0.envoy` | release | `0.20260413.0` | `0.20260813.0` | envoy, minor-behind | envoy, envoy main | bcr-exists-but-fork-justified<br>boringssl: 0.0.0-20211025-d4f1ab9, 0.0.0-20230215-5c22014, 0.0.0-20240126-22d349c, 0.0.0-20240530-2db0eb3, 0.20240913.0, 0.20240930.0, 0.20241024.0, 0.20241209.0, 0.20250114.0, 0.20250212.0, 0.20250311.0, 0.20250415.0, 0.20250514.0, 0.20250701.0, 0.20250807.0, 0.20250818.0, 0.20251002.0, 0.20251110.0, 0.20251124.0, 0.20260204.0, 0.20260211.0, 0.20260327.0, 0.20260413.0, 0.20260508.0, 0.20260526.0, 0.20260616.0, 0.20260713.0, 0.20260730.0, 0.20260803.0, 0.20260813.0 | Uses the BCR boringssl source tarball but publishes a source-only wrapper module for Envoy's split boringssl setup. |
| `cel-cpp` | `0.14.0.envoy` | release | `0.14.0` | `v0.16.1` | envoy, minor-behind | envoy, envoy main | bcr-exists-but-fork-justified<br>cel-cpp: 0.11.0, 0.12.0, 0.13.0, 0.14.0, 0.15.0, 0.16.1 | 2 patch(es): cel-cpp-protobuf-v35.patch, cel-cpp.patch |
| `colm` | `0.14.7-211228-2d8ba76.envoy` | commit | `2d8ba76 (2021-12-28)` | `ragel-barracuda-v5 (2015-08-05)` | envoy, commit-pinned | envoy, ragel, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `cpp2sky` | `0.6.0.envoy` | release | `0.6.0` | `v0.6.0` | envoy, current | envoy, envoy main | bcr-exists-but-fork-justified<br>cpp2sky: 0.6.1-20251203-dfc5bd9 | BCR has only 0.6.1-20251203-dfc5bd9; registry carries 0.6.0 with cpp2sky.patch. |
| `dd-trace-cpp` | `2.1.1.envoy` | release | `2.1.1` | `v2.2.0` | envoy, minor-behind | envoy, envoy main | not-in-bcr | Upstream ships MODULE.bazel |
| `dragonbox` | `0.0.0-241028-6c7c925.envoy` | commit | `6c7c925 (2024-10-28)` | `1.1.3 (2022-06-18)` | transitive-only, commit-pinned | proxy-wasm-cpp-host, v8 | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `elfutils` | `0.195.envoy` | release | `0.195` | `0.196` | transitive-only, minor-behind | libbpf | bcr-exists-but-fork-justified<br>elfutils: 0.195 | Exact BCR 0.195 exists; local fork keeps the same upstream packaging but retargets zlib-ng. |
| `emsdk` | `4.0.23.envoy` | commit | `c0bb220 (2026-01-10)` | `6.0.10 (2026-09-21)` | envoy, tag-available | envoy, proxy-wasm-cpp-sdk, envoy main | bcr-exists-but-fork-justified<br>emsdk: 4.0.13, 4.0.15, 4.0.16, 4.0.17, 5.0.2, 5.0.3, 5.0.4, 5.0.5, 5.0.6, 5.0.7, 6.0.0, 6.0.1, 6.0.2, 6.0.3, 6.0.4, 6.0.5, 6.0.6, 6.0.7, 6.0.8, 6.0.9, 6.0.10 | Commit pin predates upstream tag 6.0.10. |
| `envoy` | `1.40.0-dev.20260904.13144fb.envoy` | envoy-owned | `13144fb (2026-09-04)` | `main 40e1405 (2026-09-22)` | examples, mobile | envoy-example-filter-cc, envoy-example-wasm-cc, envoy-examples, mobile (envoy main) | not-in-bcr | Upstream ships MODULE.bazel |
| `envoy-example-filter-cc` | `0.2.6.envoy` | envoy-owned | `da44185 (2026-09-04)` | `main fd3f56f (2026-09-04)` | examples | envoy-examples | not-in-bcr | Upstream ships MODULE.bazel |
| `envoy-example-wasm-cc` | `0.2.6.envoy` | envoy-owned | `da44185 (2026-09-04)` | `main fd3f56f (2026-09-04)` | examples | envoy-examples | not-in-bcr | Upstream ships MODULE.bazel |
| `envoy-examples` | `0.2.6.envoy` | envoy-owned | `da44185 (2026-09-04)` | `main fd3f56f (2026-09-04)` | docs | docs (envoy main) | not-in-bcr | Upstream ships MODULE.bazel |
| `envoy_api` | `1.40.0-dev.20260904.13144fb.envoy` | envoy-owned | `13144fb (2026-09-04)` | `main 40e1405 (2026-09-22)` | envoy, examples, docs, mobile | envoy, envoy-example-filter-cc, docs (envoy main), envoy main, mobile (envoy main) | bcr-exists-but-fork-justified<br>envoy_api: 0.0.0-20241214-918efc9, 0.0.0-20250128-4de3c74, 0.0.0-20251105-4a2b9a3, 0.0.0-20251216-6ef568c, 0.0.0-20260130-84e8436, 0.0.0-20260901-005c18a, 0.0.0-20260901-005c18a.bcr.1 | Snapshot cut from envoy main; BCR has older envoy_api snapshots, not this commit. |
| `envoy_toolshed` | `0.4.15.envoy` | envoy-owned | `79701c1 (2026-09-09)` | `main aa952f2 (2026-09-20)` | envoy, envoy_api, docs, mobile | envoy, envoy_api, api/MODULE on envoy main, docs (envoy main), envoy main, mobile (envoy main) | bcr-exists-but-fork-justified<br>envoy_toolshed: 0.3.11, 0.3.24, 0.3.25 | BCR has only older 0.3.x releases; the registry carries 0.4.15 used by envoy/envoy_api/docs/mobile. |
| `envoy_toolshed_jq` | `0.4.15.envoy` | envoy-owned | `79701c1 (2026-09-09)` | `main aa952f2 (2026-09-20)` | toolshed | envoy_toolshed | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `fp16` | `0.0.0-260704-3d2de18.envoy` | commit | `3d2de18 (2026-07-04)` | `unknown` | transitive-only, commit-pinned | proxy-wasm-cpp-host, v8 | bcr-exists-but-fork-justified<br>fp16: 0.0.0-20210320-0a92994 | No matching BCR version. overlay: BUILD.bazel |
| `go-fips` | `1.24.12.envoy` | release | `1.24.12` | `1.27.1` | transitive-only, minor-behind | boringssl-fips | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `googleurl` | `0.0.0-221103-dd4080f.envoy` | commit | `dd4080f (2022-11-03)` | `unknown` | envoy, examples, docs, mobile, commit-pinned | envoy, envoy-example-filter-cc, quiche, docs (envoy main), envoy main, mobile (envoy main) | not-in-bcr | Upstream ships MODULE.bazel |
| `grpc` | `1.83.0.envoy` | release | `1.83.0` | `v1.84.0` | envoy, envoy_api, docs, mobile, minor-behind | cpp2sky, envoy, envoy_api, skywalking-data-collect-protocol, api/MODULE on envoy main, docs (envoy main), envoy main, mobile (envoy main) | bcr-exists-but-fork-justified<br>grpc: 1.41.0, 1.47.0, 1.48.1, 1.48.1.bcr.1, 1.48.1.bcr.2, 1.48.1.bcr.3, 1.56.3, 1.56.3.bcr.1, 1.62.1, 1.62.1.bcr.1, 1.62.1.bcr.2, 1.63.1, 1.63.1.bcr.1, 1.65.0, 1.66.0, 1.66.0.bcr.1, 1.66.0.bcr.2, 1.66.0.bcr.3, 1.68.0, 1.69.0, 1.70.1, 1.71.0, 1.71.1, 1.71.2, 1.72.0-pre1, 1.72.0, 1.73.0-pre1, 1.73.1, 1.74.0-pre2, 1.74.0, 1.74.1, 1.75.0, 1.75.1, 1.76.0, 1.76.0.bcr.1, 1.78.0-pre1, 1.78.0, 1.78.0.bcr.1, 1.80.0-pre1, 1.80.0, 1.81.0-pre1, 1.81.0, 1.81.1, 1.82.0-pre1, 1.82.0, 1.82.1, 1.83.0-pre1, 1.83.0, 1.84.0 | Exact BCR 1.83.0 exists; local fork adds grpc.patch. |
| `grpc-httpjson-transcoding` | `0.0.0-20250507-a6e226f.envoy` | commit | `a6e226f (2025-05-07)` | `unknown` | envoy, commit-pinned | envoy, proto-field-extraction, proto-processing, envoy main | bcr-exists-but-fork-justified<br>grpc-httpjson-transcoding: 0.0.0-20230607-ff41eb3 | No matching BCR version. 2 patch(es): grpc-httpjson-transcoding.patch, module_dot_bazel.patch |
| `hermetic-android-toolchains` | `0.0.0-20260807-c6a9f20.envoy` | commit | `c6a9f20 (2026-08-07)` | `0.4.0 (2026-09-09)` | mobile, tag-available | mobile (envoy main) | not-in-bcr | Commit pin predates upstream tag 0.4.0. |
| `hessian2-codec` | `0.0.0-250114-6f5a647.envoy` | commit | `6f5a647 (2025-01-14)` | `unknown` | envoy, commit-pinned | envoy, envoy main | not-in-bcr | Upstream ships MODULE.bazel |
| `hyperscan` | `5.4.2.envoy` | release | `5.4.2` | `v5.4.2` | envoy, current | envoy, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `icu` | `78.2.envoy` | release | `78.2` | `release-78.3` | envoy, minor-behind | envoy, envoy main, v8 | bcr-exists-but-fork-justified<br>icu: 76.1, 76.1.bcr.1, 76.1.bcr.2, 76.1.bcr.3, 76.1.bcr.4, 77.1, 78.2, 78.2.bcr.1, 78.2.bcr.2 | Exact BCR 78.2 exists; local fork uses the release tarball plus four extra patches/overlay files. |
| `ipp-crypto` | `2.2.0.envoy` | release | `2.2.0` | `v2.3.0` | envoy, minor-behind | envoy, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `kafka` | `3.9.2.envoy` | release | `3.9.2` | `4.3.1` | envoy, major-behind | envoy, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `libbpf` | `1.7.0.envoy` | release | `1.7.0` | `v1.7.0` | envoy, current | envoy, envoy main | bcr-exists-but-fork-justified<br>libbpf: 1.7.0 | Exact BCR 1.7.0 exists; local fork swaps zlib for zlib-ng and elfutils for elfutils.envoy. |
| `libcircllhist` | `0.3.2.envoy` | release | `0.3.2` | `py-0.3.2` | envoy, current | envoy, envoy main | bcr-exists-reason-unclear<br>libcircllhist: 0.3.2, 0.3.2.bcr.1 | Exact BCR 0.3.2 exists; this fork mostly rewrites BCR's generic add_build_file/module patching as overlays and adds a rules_cc dep. No Envoy-specific need is obvious from the fork. |
| `libevent` | `2.2.2-alpha.envoy` | release | `2.2.2-alpha` | `release-2.1.13-stable` | envoy, stable-available | envoy, envoy main | bcr-exists-but-fork-justified<br>libevent: 2.1.12-stable.bcr.0 | Pinned to a pre-release; the latest stable upstream line is still release-2.1.13-stable. |
| `libmaxminddb` | `1.13.3.envoy` | release | `1.13.3` | `1.14.1` | envoy, minor-behind | envoy main | bcr-exists-but-fork-justified<br>libmaxminddb: 1.10.0, 1.12.2 | BCR has 1.10.0 and 1.12.2; registry carries newer 1.13.3 packaging. |
| `librdkafka` | `2.6.0.envoy` | release | `2.6.0` | `v2.15.1` | envoy, docs, mobile, minor-behind | envoy, docs (envoy main), envoy main, mobile (envoy main) | bcr-exists-but-fork-justified<br>librdkafka: 2.3.0, 2.3.0.bcr.1, 2.8.0, 2.8.0.bcr.1, 2.8.0.bcr.2, 2.14.2, 2.15.0 | BCR exists but not at 2.6.0; local fork also carries five patches plus BUILD/MODULE/test overlays. |
| `libsxg` | `0.0.0-210708-beaa393.envoy` | commit | `beaa393 (2021-07-08)` | `v2.1 (2021-02-22)` | envoy, docs, mobile, commit-pinned | envoy, docs (envoy main), envoy main, mobile (envoy main) | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `liburing` | `2.15.envoy` | release | `2.15` | `liburing-2.15` | envoy, current | envoy, envoy main | bcr-exists-but-fork-justified<br>liburing: 2.5, 2.10, 2.14, 2.14.bcr.1, 2.14.bcr.2, 2.15 | Exact BCR 2.15 exists; local fork adds liburing.patch for external-build archive tool handling. |
| `luajit` | `0.0.0-260126-871db2c.envoy` | commit | `871db2c (2026-01-26)` | `unknown` | envoy, commit-pinned | envoy, envoy main | bcr-exists-but-fork-justified<br>luajit: 2.0.5, 2.1.0-beta3 | No matching BCR version. overlay: BUILD.bazel, MODULE.bazel |
| `lz4` | `1.10.0.bcr.2.envoy` | release | `1.10.0.bcr.2` | `v1.10.0` | envoy, current | envoy, qatzip, envoy main | bcr-exists-but-fork-justified<br>lz4: 1.9.4, 1.9.4.bcr.1, 1.9.4.bcr.2, 1.10.0, 1.10.0.bcr.1 | No matching BCR version. overlay: BUILD.bazel, MODULE.bazel, foreign_cc/BUILD.bazel… |
| `msgpack-cxx` | `7.0.0.envoy` | release | `7.0.0` | `cpp-9.0.0` | envoy, major-behind | envoy, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `nghttp2` | `1.66.0.envoy` | release | `1.66.0` | `v1.70.0` | envoy, minor-behind | envoy, quiche, envoy main | bcr-exists-but-fork-justified<br>nghttp2: 1.65.0 | No matching BCR version. 7 patch(es): nghttp2-CVE-2026-27135_part1.patch, nghttp2-CVE-2026-27135_part2.patch, nghttp2-CVE-2026-27135_part3.patch… overlay: BUILD.bazel, MODULE.bazel, config/config.h |
| `ocp-diag-core` | `0.0.0-230505-e965ac0.envoy` | commit | `e965ac0 (2023-05-05)` | `unknown` | envoy, commit-pinned | envoy, proto-field-extraction, proto-processing, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `openssl` | `3.5.7.envoy` | release | `3.5.7` | `openssl-4.0.2` | envoy, mobile, major-behind | envoy, envoy main, mobile (envoy main) | bcr-exists-but-fork-justified<br>openssl: 3.3.1.bcr.0, 3.3.1.bcr.1, 3.3.1.bcr.2, 3.3.1.bcr.3, 3.3.1.bcr.6, 3.3.1.bcr.7, 3.3.1.bcr.8, 3.3.1.bcr.9, 3.5.4.bcr.0, 3.5.4.bcr.1, 3.5.5.bcr.0, 3.5.5.bcr.1, 3.5.5.bcr.2, 3.5.5.bcr.3, 3.5.5.bcr.4, 3.5.8.bcr.0, 4.0.1.bcr.0 | No matching BCR version. overlay: BUILD.bazel |
| `perfetto` | `57.2.envoy` | release | `57.2` | `v58.2` | envoy, major-behind | envoy, envoy main | not-in-bcr | Upstream ships MODULE.bazel |
| `prometheus-metrics-model` | `0.6.2.envoy` | release | `0.6.2` | `v0.6.3` | envoy, envoy_api, minor-behind | envoy, envoy_api, api/MODULE on envoy main, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `proto-converter` | `0.0.0-20260912-3850764.envoy` | commit | `3850764 (2026-09-12)` | `unknown` | envoy, commit-pinned | envoy, proto-processing, envoy main | bcr-exists-but-fork-justified<br>proto-converter: 0.0.0-20230607-d77ff30 | No matching BCR version. 2 patch(es): module_dot_bazel.patch, proto-converter.patch |
| `proto-field-extraction` | `0.0.0-240710-d5d39f0.envoy` | commit | `d5d39f0 (2024-07-10)` | `unknown` | envoy, commit-pinned | envoy, proto-processing, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `proto-processing` | `0.0.0-250110-279353c.envoy` | commit | `279353c (2025-01-10)` | `unknown` | envoy, commit-pinned | envoy, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `protobuf` | `35.1.bcr.envoy` | release | `35.1.bcr` | `v36.2` | envoy, examples, envoy_api, toolshed, docs, mobile, major-behind | envoy, envoy-example-filter-cc, envoy_api, envoy_toolshed, prometheus-metrics-model, protoc-gen-jsonschema, quiche, api/MODULE on envoy main, docs (envoy main), envoy main, mobile (envoy main), zipkin-api | bcr-exists-but-fork-justified<br>protobuf: 3.19.0, 3.19.2, 3.19.6, 21.7, 23.1, 24.4, 25.5, 25.6, 26.0, 26.0.bcr.1, 26.0.bcr.2, 27.0-rc2, 27.0, 27.0.bcr.1, 27.1, 27.1.bcr.1, 27.2, 27.3, 27.4, 27.5, 28.0-rc1, 28.0-rc2, 28.0, 28.1, 28.2, 28.3, 29.0-rc1, 29.0-rc2, 29.0-rc2.bcr.1, 29.0-rc3, 29.0, 29.1, 29.2, 29.3, 29.4, 29.5, 30.0-rc1, 30.0-rc2, 30.0, 30.1, 30.2, 31.0-rc1, 31.0-rc2, 31.0, 31.1, 32.0-rc1, 32.0-rc2, 32.0, 32.1, 33.0-rc1, 33.0-rc2, 33.0, 33.1, 33.2, 33.3, 33.3.bcr.1, 33.4, 33.5, 33.6, 34.0-rc1, 34.0, 34.0.bcr.1, 34.1, 35.0-rc1, 35.0-rc2, 35.0, 35.1, 36.0-rc1, 36.0-rc2, 36.0, 36.0.bcr.1, 36.1, 36.1.bcr.1, 36.2 | No matching BCR version. 1 patch(es): envoy.patch |
| `protoc-gen-jsonschema` | `0.0.0-20230530-7680e49.envoy` | commit | `7680e49 (2023-05-30)` | `unknown` | envoy_api, commit-pinned | envoy_api, api/MODULE on envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `protoc-gen-validate` | `1.3.3.envoy` | release | `1.3.3` | `v1.3.3` | envoy, examples, envoy_api, docs, mobile, current | envoy, envoy-example-filter-cc, envoy_api, protoc-gen-jsonschema, api/MODULE on envoy main, docs (envoy main), envoy main, mobile (envoy main) | bcr-exists-but-fork-justified<br>protoc-gen-validate: 1.0.4, 1.0.4.bcr.1, 1.0.4.bcr.2, 1.2.1, 1.2.1.bcr.1, 1.2.1.bcr.2, 1.3.0, 1.3.3 | Exact BCR 1.3.3 exists; local fork adds pgv.patch and self_labels.patch on top of BCR's bazel_9_fixes.patch. |
| `proxy-wasm-cpp-host` | `0.0.0-260704-f2db56a.envoy` | commit | `f2db56a (2026-07-04)` | `unknown` | envoy, examples, docs, mobile, commit-pinned | envoy, envoy-example-filter-cc, docs (envoy main), envoy main, mobile (envoy main) | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `proxy-wasm-cpp-sdk` | `0.0.0-250925-e5256b0.envoy` | commit | `e5256b0 (2025-09-25)` | `v0.1.0 (2020-02-29)` | envoy, commit-pinned | envoy, proxy-wasm-cpp-host, envoy main | bcr-exists-but-fork-justified<br>proxy-wasm-cpp-sdk: 0.0.0-20260123-894dd29 | No matching BCR version. 2 patch(es): proxy-wasm-cpp-sdk.patch, proxy_wasm_cpp_sdk-protobuf-v35.patch |
| `proxy-wasm-rust-sdk` | `0.2.4-251205-5283e57.envoy` | commit | `5283e57 (2025-12-05)` | `v0.2.5 (2026-05-20)` | envoy, tag-available | envoy, envoy main | bcr-exists-but-fork-justified<br>proxy-wasm-rust-sdk: 0.2.4, 0.2.5 | Commit pin predates upstream tag v0.2.5. |
| `qat-zstd` | `1.0.0.envoy` | release | `1.0.0` | `v1.0.0` | envoy, current | envoy, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `qatlib` | `26.02.0.envoy` | release | `26.02.0` | `26.08.0` | envoy, minor-behind | envoy, qat-zstd, qatzip, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `qatzip` | `1.3.2.envoy` | release | `1.3.2` | `v2.0.0` | envoy, major-behind | envoy, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `quiche` | `0.0.0-260831-5c9cc6b.envoy` | commit | `5c9cc6b (2026-08-31)` | `unknown` | envoy, examples, docs, mobile, commit-pinned | envoy, envoy-example-filter-cc, docs (envoy main), envoy main, mobile (envoy main) | not-in-bcr | Upstream ships MODULE.bazel |
| `ragel` | `7.0.4-211228-d4577c9.envoy` | commit | `d4577c9 (2021-12-28)` | `ragel-barracuda-v5 (2015-08-05)` | envoy, commit-pinned | envoy, hyperscan, envoy main, vectorscan | bcr-exists-but-fork-justified<br>ragel: 26.04.0-20260414092900-8841e561489e | No matching BCR version. overlay: BUILD.bazel, MODULE.bazel |
| `rclone` | `1.70.3.envoy` | release | `1.70.3` | `v1.75.1` | unused, minor-behind | — | not-in-bcr | No direct or transitive consumer in the registry snapshots or envoy main docs/mobile roots. |
| `rules_apple` | `3.20.1.envoy` | release | `3.20.1` | `5.1.0` | envoy, mobile, major-behind | envoy, envoy main, mobile (envoy main) | bcr-exists-but-fork-justified<br>rules_apple: 2.0.0-rc1, 2.0.0, 2.1.0, 2.2.0, 2.3.0, 2.4.0, 2.4.1, 2.5.0, 3.0.0-rc1, 3.0.0-rc2, 3.0.0, 3.1.0, 3.1.1, 3.2.0, 3.2.1, 3.3.0, 3.4.0, 3.5.0, 3.5.1, 3.6.0, 3.7.0, 3.8.0, 3.9.0, 3.9.1, 3.9.2, 3.10.0, 3.11.0, 3.11.1, 3.11.2, 3.12.0, 3.13.0, 3.14.0, 3.15.0, 3.16.0, 3.16.1, 3.17.0, 3.17.1, 3.18.0, 3.19.0, 3.19.1, 3.20.0, 3.20.1, 3.21.0, 3.21.1, 3.22.0, 4.0.0, 4.0.1, 4.1.0, 4.1.1, 4.1.2, 4.2.0, 4.3.1, 4.3.2, 4.3.3, 4.4.0, 4.5.0, 4.5.1, 4.5.2, 4.5.3, 5.0.0-rc1, 5.0.0-rc2, 5.0.0-rc3, 5.0.0-rc4, 5.0.0, 5.0.1, 5.1.0 | Exact BCR 3.20.1 exists; local fork adds rules_apple.patch and rules_apple_py.patch. |
| `rules_rust` | `0.69.0.envoy` | release | `0.69.0` | `0.74.0` | envoy, examples, toolshed, docs, mobile, minor-behind | envoy, envoy-example-filter-cc, envoy_toolshed, sq, docs (envoy main), envoy main, mobile (envoy main) | bcr-exists-but-fork-justified<br>rules_rust: 0.35.0, 0.36.2, 0.38.0, 0.39.0, 0.40.0, 0.41.1, 0.42.1, 0.43.0, 0.44.0, 0.45.0, 0.45.1, 0.46.0, 0.47.1, 0.48.0, 0.49.0, 0.49.1, 0.49.2, 0.49.3, 0.50.0, 0.50.1, 0.51.0, 0.52.0, 0.52.1, 0.52.2, 0.53.0, 0.54.1, 0.55.6, 0.56.0, 0.57.0, 0.57.1, 0.58.0, 0.59.1, 0.59.2, 0.60.0, 0.61.0, 0.62.0, 0.63.0, 0.64.0, 0.65.0, 0.66.0, 0.67.0, 0.68.0, 0.68.1, 0.69.0, 0.70.0, 0.71.0, 0.71.1, 0.71.2, 0.71.3, 0.72.0, 0.73.0, 0.74.0 | Exact BCR 0.69.0 exists; local fork adds rules_rust.patch. |
| `rules_swift` | `2.5.0.envoy` | release | `2.5.0` | `4.1.1` | envoy, mobile, major-behind | envoy main, mobile (envoy main) | bcr-exists-but-fork-justified<br>rules_swift: 1.2.0, 1.5.0, 1.5.1, 1.6.0, 1.7.0, 1.7.1, 1.8.0, 1.9.0, 1.9.1, 1.10.0, 1.10.1, 1.11.0, 1.12.0, 1.13.0, 1.14.0, 1.15.0, 1.15.1, 1.16.0, 1.17.0, 1.18.0, 2.0.0-rc1, 2.0.0, 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4, 2.3.0, 2.3.1, 2.4.0, 2.5.0, 2.6.0, 2.7.0, 2.8.0, 2.8.1, 2.8.2, 2.9.0, 3.0.0, 3.0.2, 3.1.0, 3.1.1, 3.1.2, 3.2.0, 3.3.0, 3.4.0, 3.4.1, 3.4.2, 3.5.0, 3.6.0, 3.6.1, 4.0.0-rc1, 4.0.0-rc2, 4.0.0-rc3, 4.0.0-rc4, 4.0.0-rc5, 4.0.0-rc6, 4.0.1, 4.1.0, 4.1.1 | Exact BCR 2.5.0 exists; local fork adds rules_swift_remove_toolchain_prints.patch. |
| `simdutf` | `8.1.0.envoy` | release | `8.1.0` | `v9.2.0` | transitive-only, major-behind | proxy-wasm-cpp-host, v8 | bcr-exists-but-fork-justified<br>simdutf: 7.7.0 | No matching BCR version. overlay: BUILD.bazel |
| `skywalking-data-collect-protocol` | `10.4.0.envoy` | release | `10.4.0` | `v11.0.0` | transitive-only, major-behind | cpp2sky | bcr-exists-but-fork-justified<br>skywalking-data-collect-protocol: 9.7.0, 10.3.0 | No matching BCR version. |
| `sq` | `1.4.0.envoy` | release | `1.4.0` | `v1.4.1` | toolshed, envoy, minor-behind | envoy_toolshed, envoy main | not-in-bcr | Upstream MODULE.bazel unknown |
| `sql-parser` | `0.0.0-260715-52e5ad1.envoy` | commit | `52e5ad1 (2026-07-15)` | `v1.5 (2017-03-08)` | envoy, commit-pinned | envoy, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `tcmalloc` | `0.0.0-250926-12f2552.envoy` | commit | `12f2552 (2025-09-26)` | `unknown` | envoy, commit-pinned | envoy, envoy main | bcr-exists-but-fork-justified<br>tcmalloc: 0.0.0-20240411-5ed309d, 0.0.0-20250331-43fcf6e, 0.0.0-20250927-12f2552, 0.0.0-20260818-15db23d | No matching BCR version. 1 patch(es): tcmalloc.patch |
| `thrift` | `0.24.0.envoy` | release | `0.24.0` | `v0.24.0` | envoy, current | envoy, envoy main | bcr-exists-but-fork-justified<br>thrift: 0.22.0 | No matching BCR version. 1 patch(es): thrift.patch overlay: BUILD.bazel |
| `toolchains_llvm` | `1.9.0.envoy` | release | `1.9.0` | `v1.9.1` | envoy, examples, toolshed, docs, mobile, minor-behind | envoy, envoy-example-filter-cc, envoy-example-wasm-cc, envoy-examples, envoy_toolshed, icu, docs (envoy main), envoy main, mobile (envoy main) | bcr-exists-but-fork-justified<br>toolchains_llvm: 0.10.3, 1.0.0, 1.1.2, 1.2.0, 1.3.0, 1.4.0, 1.5.0, 1.6.0, 1.7.0, 1.8.0, 1.9.0, 1.9.1 | Exact BCR 1.9.0 exists; local fork adds allow_nonroot.patch and x_compile.patch. |
| `uadk` | `2.9.envoy` | release | `2.9` | `v2.11` | envoy, minor-behind | envoy, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `v8` | `14.6.202.10.envoy` | release | `14.6.202.10` | `15.6.39-pgo` | envoy, toolshed, major-behind | envoy, envoy_toolshed, proxy-wasm-cpp-host, envoy main | not-in-bcr | Upstream ships MODULE.bazel |
| `vectorscan` | `5.4.11.envoy` | release | `5.4.11` | `vectorscan-v5.4.0` | envoy, current | envoy, envoy main | not-in-bcr | Latest GitHub release is still vectorscan-v5.4.0; the registry pin 5.4.11 is newer than that release tag. |
| `vpp-vcl` | `26.02-dev-85abefb.envoy` | commit | `85abefb (2026-01-11)` | `v26.06 (2026-06-21)` | envoy, tag-available | envoy, envoy main | not-in-bcr | Commit pin predates upstream tag v26.06; the registry version string also still carries a -dev suffix. |
| `wamr` | `2.4.4.envoy` | release | `2.4.4` | `WAMR-2.4.5` | envoy, minor-behind | envoy, proxy-wasm-cpp-host, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `wasmtime` | `45.0.2.envoy` | release | `45.0.2` | `v49.0.0` | envoy, major-behind | envoy, proxy-wasm-cpp-host, envoy main | not-in-bcr | No upstream MODULE.bazel at HEAD |
| `wuffs` | `0.4.0-alpha.9.envoy` | release | `0.4.0-alpha.9` | `v0.3.5` | envoy, stable-available | envoy, envoy main | not-in-bcr | Pinned to a pre-release; upstream also has stable v0.3.5. |
| `yq.bzl` | `0.1.1.envoy` | release | `0.1.1` | `v0.4.0` | envoy, envoy_api, minor-behind | envoy, envoy_api, api/MODULE on envoy main, envoy main | bcr-exists-but-fork-justified<br>yq.bzl: 0.1.1, 0.2.0, 0.3.0, 0.3.1, 0.3.2, 0.3.4, 0.3.5, 0.3.6, 0.4.0 | Exact BCR 0.1.1 exists; local fork adds yq.patch and a MODULE overlay. |
| `zipkin-api` | `1.0.0.envoy` | release | `1.0.0` | `1.0.0` | envoy, envoy_api, current | envoy, envoy_api, api/MODULE on envoy main, envoy main | bcr-exists-reason-unclear<br>zipkin-api: 1.0.0, 1.0.0.bcr.1 | Exact BCR 1.0.0 exists; this fork swaps BCR patches for a BUILD overlay and adds a protobuf dep. No Envoy-specific need is obvious from the fork. |
| `zlib-ng` | `2.3.2.envoy` | release | `2.3.2` | `2.3.3` | envoy, docs, mobile, minor-behind | elfutils, envoy, libbpf, qatzip, docs (envoy main), envoy main, mobile (envoy main) | bcr-exists-but-fork-justified<br>zlib-ng: 2.0.7, 2.3.3, 2.3.3.bcr.1, 2.3.3.bcr.2 | No matching BCR version. 2 patch(es): add_build_file.patch, add_module_dot_bazel.patch |

### rclone

No direct or transitive consumer in the registry snapshots or envoy main docs/mobile roots.

### libcircllhist

Exact BCR 0.3.2 exists; this fork mostly rewrites BCR's generic add_build_file/module patching as overlays and adds a rules_cc dep. No Envoy-specific need is obvious from the fork.

### zipkin-api

Exact BCR 1.0.0 exists; this fork swaps BCR patches for a BUILD overlay and adds a protobuf dep. No Envoy-specific need is obvious from the fork.

### libevent

Pinned to a pre-release; the latest stable upstream line is still release-2.1.13-stable.

### wuffs

Pinned to a pre-release; upstream also has stable v0.3.5.

### emsdk

Commit pin predates upstream tag 6.0.10.

### hermetic-android-toolchains

Commit pin predates upstream tag 0.4.0.

### proxy-wasm-rust-sdk

Commit pin predates upstream tag v0.2.5.

### vpp-vcl

Commit pin predates upstream tag v26.06; the registry version string also still carries a -dev suffix.
