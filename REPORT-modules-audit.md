# Module audit report (branch `61cd206`)

## Executive summary

- Hosted module directories on this branch: **76 modules / 77 version directories** (`quiche` has two hosted versions). Evidence: https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/quiche/metadata.json
- Staleness sweep result: **24 `STALE-MAJOR`**, **27 `STALE-MINOR`**, **25 `CURRENT`**, **0 `UNKNOWN`**.
- `grpc` and `protobuf` are stale (`grpc` `1.83.0.envoy` → upstream `v1.84.0`; `protobuf` `35.1.bcr.envoy` → upstream `v36.2`) but are **excluded from action items** per issue scope.
- Highest-value patch-drop candidates are `nghttp2` (security patch set upstream by `v1.68.1`), `quiche` consumer bumps (old consumer pins still carry the pre-`7f07dc4` snapshot), `elfutils` (`0.196`), `liburing` (`2.16`), and probably `yq.bzl` (`0.4.0`).
- Overlay-only modules that most look historical vs justified packaging are **`libbpf`** and probably **`openssl` on bump**; **`lz4`** and **`ragel`** still have material overlay differences versus BCR.
- Internal metadata drift is real: several hosted `MODULE.bazel` files still declare versions that are neither the currently hosted versions nor even present in this registry; some would resolve to BCR/non-hosted versions, others would fail unless another consumer requests a newer replacement.
- Consumer pin drift is small for Envoy/envoy-website (**2 commits behind HEAD; only `quiche` changes**) and much larger for examples/toolshed.

### Ordered action list

1. **Bumps that also drop patches**
   - `nghttp2` to at least `v1.68.1` (drops the CVE-2026-27135 backports plus Huffman/max-header-size security carry). Evidence: https://github.com/nghttp2/nghttp2/releases/tag/v1.68.1
   - `elfutils` to `0.196` (drops `assert_perror.patch`). Evidence: https://sourceware.org/git/?p=elfutils.git;a=tag;h=refs/tags/0.196
   - `liburing` to `2.16` (drops `liburing.patch`). Evidence: https://github.com/axboe/liburing/releases/tag/liburing-2.16
   - `yq.bzl` to `0.4.0` and re-check that `yq.patch` can be deleted. Evidence: https://github.com/bazel-contrib/yq.bzl/releases/tag/v0.4.0
2. **Security-relevant bumps**
   - `nghttp2` first.
   - `openssl` is also stale at a major boundary (`3.5.7.envoy` vs upstream `4.0.2`). Evidence: https://github.com/openssl/openssl/releases/tag/openssl-4.0.2
3. **Other `STALE-MAJOR` bumps**
   - Prioritize very old commit-pins / major-version gaps: `colm`, `ragel`, `googleurl`, `bazel-compdb`, `libsxg`, `luajit`, `tcmalloc`, `proxy-wasm-cpp-sdk`, `vpp-vcl`, `emsdk`, `aws-c-auth-testdata`, `kafka`, `msgpack-cxx`, `perfetto`, `qatzip`, `simdutf`, `skywalking-data-collect-protocol`, `v8`, `wasmtime`.
4. **Overlay-only modules that look redundant with BCR**
   - `libbpf` looks directly redundant with BCR `1.7.0`.
   - `openssl` looks plausibly redundant on bump because BCR already carries a richer maintained overlay for `3.5.8.bcr.0`.
5. **Metadata drift fixes**
   - Normalize stale dependency declarations in `envoy`, `envoy_api`, `grpc`, `libevent`, `librdkafka`, `perfetto`, `proxy-wasm-*`, `skywalking-data-collect-protocol`, `tcmalloc`, `wasmtime`, and the hosted examples modules.
6. **Consumer pin bumps**
   - `envoy` / `envoy-website`: only picks up the newer `quiche` snapshot.
   - `toolshed` bazel pin: picks up `quiche` + `hermetic-android-toolchains`.
   - `toolshed` jq pin: picks up 9 module-version changes.
   - `examples` pin: picks up 17 module-version changes.

## Methodology

- Upstream data was fetched for every module from the `source.json` origin URL at current branch `HEAD`, using GitHub release redirects first, then tag pages / `git ls-remote --tags`, and default-branch head/compare data for commit-pinned modules. Representative examples: https://github.com/grpc/grpc/releases/tag/v1.84.0, https://github.com/google/quiche/compare/7f07dc4d14c5702607a0dee9c7e4ab07f63f9883...41ee992597583771801dcb8569e1eca71842ef74
- BCR data was read from `https://raw.githubusercontent.com/bazelbuild/bazel-central-registry/main/modules/<module>/metadata.json` (or absence of that file was treated as no BCR module).
- Consumer coverage / pinning was verified from these exact consumer commits:
  - Envoy `a712680a0725ad8fe401d9bceb1a356efd58d2fc`: `MODULE.bazel`, `MODULE.bazel.lock`, `api/MODULE.bazel`, `mobile/MODULE.bazel`, `docs/MODULE.bazel`, `bazel/tests/external/MODULE.bazel`, `.bazelrc`.
  - envoy-website `c03efd7234fe36ef65226e1000038adffa41d7e2`: `MODULE.bazel`, `.bazelrc`.
  - toolshed `bc06f06d02c81bd69b4bdf13cc05408030926e10`: `bazel/MODULE.bazel(.lock)`, `jq/MODULE.bazel`, `bazel/.bazelrc`, `jq/.bazelrc`.
  - examples `fd3f56fce6807b0a434e2ef5c394795ba3f00404`: root / `filter-cc` / `wasm-cc` `MODULE.bazel(.lock)` plus `.bazelrc`.
- Note: this branch predates main’s `libmaxminddb` removal (`#150`), so the tables below still include `libmaxminddb` because it exists on this branch. Evidence: https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/libmaxminddb/metadata.json

## 1. Staleness — every module

| Module | Hosted version → upstream ref | Upstream latest | BCR latest | Classification | Notes |
|---|---|---|---|---|---|
| `colm` | `0.14.7-211228-2d8ba76.envoy` → [`2d8ba76ddaf6634f285d0a81ee42d5ee77d084cf`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/colm/0.14.7-211228-2d8ba76.envoy/source.json#L1-L9) | HEAD [`0237fa9`](https://github.com/adrian-thurston/colm-suite/commit/0237fa9fb2caea573468e657c61a3d430c04fd2f) (244 commits / 1725d newer; [compare](https://github.com/adrian-thurston/colm-suite/compare/2d8ba76ddaf6634f285d0a81ee42d5ee77d084cf...0237fa9fb2caea573468e657c61a3d430c04fd2f)) | — | STALE-MAJOR |  |
| `ragel` | `7.0.4-211228-d4577c9.envoy` → [`d4577c924451b331c73c8ed0af04f6efd35ac0b4`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/ragel/7.0.4-211228-d4577c9.envoy/source.json#L1-L9) | HEAD [`b91c7d6`](https://github.com/adrian-thurston/ragel/commit/b91c7d6f70a3b47e1710e54a6380ccec77403ab8) (commit count unavailable / 1528d newer; [compare](https://github.com/adrian-thurston/ragel/compare/d4577c924451b331c73c8ed0af04f6efd35ac0b4...b91c7d6f70a3b47e1710e54a6380ccec77403ab8)) | [`26.04.0-20260414092900-8841e561489e`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/ragel) | STALE-MAJOR |  |
| `googleurl` | `0.0.0-221103-dd4080f.envoy` → [`dd4080fec0b443296c0ed0036e1e776df8813aa7`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/googleurl/0.0.0-221103-dd4080f.envoy/source.json#L1-L9) | HEAD [`94ff147`](https://github.com/google/gurl/commit/94ff147fe0b96b4cca5d6d316b9af6210c0b8051) (15 commits / 1102d newer; [compare](https://github.com/google/gurl/compare/dd4080fec0b443296c0ed0036e1e776df8813aa7...94ff147fe0b96b4cca5d6d316b9af6210c0b8051)) | — | STALE-MAJOR |  |
| `bazel-compdb` | `0.0.0-20220906-4086479.envoy` → [`40864791135333e1446a04553b63cbe744d358d0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/bazel-compdb/0.0.0-20220906-4086479.envoy/source.json#L1-L9) | HEAD [`d198303`](https://github.com/grailbio/bazel-compilation-database/commit/d198303a4319092ab31895c4b98d64174ebe8872) (5 commits / 558d newer; [compare](https://github.com/grailbio/bazel-compilation-database/compare/40864791135333e1446a04553b63cbe744d358d0...d198303a4319092ab31895c4b98d64174ebe8872)) | — | STALE-MAJOR |  |
| `libsxg` | `0.0.0-210708-beaa393.envoy` → [`beaa3939b76f8644f6833267e9f2462760838f18`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/libsxg/0.0.0-210708-beaa393.envoy/source.json#L1-L9) | HEAD [`b77cfb0`](https://github.com/google/libsxg/commit/b77cfb04c63cf3c02a4e118cbf40157d85bfca95) (6 commits / 447d newer; [compare](https://github.com/google/libsxg/compare/beaa3939b76f8644f6833267e9f2462760838f18...b77cfb04c63cf3c02a4e118cbf40157d85bfca95)) | — | STALE-MAJOR |  |
| `luajit` | `0.0.0-260126-871db2c.envoy` → [`871db2c`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/luajit/0.0.0-260126-871db2c.envoy/source.json#L1-L9) | HEAD [`c6ffc14`](https://github.com/LuaJIT/LuaJIT/commit/c6ffc141a8762b41703f9287d63d93622a13dd8f) (110 commits / 410d newer; [compare](https://github.com/LuaJIT/LuaJIT/compare/871db2c...c6ffc141a8762b41703f9287d63d93622a13dd8f)) | [`2.1.0-beta3`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/luajit) | STALE-MAJOR |  |
| `tcmalloc` | `0.0.0-250926-12f2552.envoy` → [`12f255231938d30493186b0a037feedd70f5a1c1`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/tcmalloc/0.0.0-250926-12f2552.envoy/source.json#L1-L9) | HEAD [`872c59e`](https://github.com/google/tcmalloc/commit/872c59e581449c2202c9e18d83c1bc66e38aad80) (commit count unavailable / 361d newer; [compare](https://github.com/google/tcmalloc/compare/12f255231938d30493186b0a037feedd70f5a1c1...872c59e581449c2202c9e18d83c1bc66e38aad80)) | [`0.0.0-20260818-15db23d`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/tcmalloc) | STALE-MAJOR |  |
| `proxy-wasm-cpp-sdk` | `0.0.0-250925-e5256b0.envoy` → [`e5256b0c5463ea9961965ad5de3e379e00486640`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/proxy-wasm-cpp-sdk/0.0.0-250925-e5256b0.envoy/source.json#L1-L9) | HEAD [`19c45f4`](https://github.com/proxy-wasm/proxy-wasm-cpp-sdk/commit/19c45f4df062e383a16bc3ac59c62f1948467866) (commit count unavailable / 337d newer; [compare](https://github.com/proxy-wasm/proxy-wasm-cpp-sdk/compare/e5256b0c5463ea9961965ad5de3e379e00486640...19c45f4df062e383a16bc3ac59c62f1948467866)) | [`0.0.0-20260123-894dd29`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/proxy-wasm-cpp-sdk) | STALE-MAJOR |  |
| `dragonbox` | `0.0.0-241028-6c7c925.envoy` → [`6c7c925b571d54486b9ffae8d9d18a822801cbda`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/dragonbox/0.0.0-241028-6c7c925.envoy/source.json#L1-L9) | HEAD [`beeeef9`](https://github.com/jk-jeon/dragonbox/commit/beeeef91cf6fef89a4d4ba5e95d47ca64ccb3a44) (31 commits / 318d newer; [compare](https://github.com/jk-jeon/dragonbox/compare/6c7c925b571d54486b9ffae8d9d18a822801cbda...beeeef91cf6fef89a4d4ba5e95d47ca64ccb3a44)) | — | STALE-MAJOR |  |
| `fp16` | `0.0.0-260704-3d2de18.envoy` → [`3d2de1816307bac63c16a297e8c4dc501b4076df`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/fp16/0.0.0-260704-3d2de18.envoy/source.json#L1-L9) | HEAD [`782eea1`](https://github.com/Maratyszcza/FP16/commit/782eea126dc5c755827be751a099eb01826175cf) (1 commits / 307d newer; [compare](https://github.com/Maratyszcza/FP16/compare/3d2de1816307bac63c16a297e8c4dc501b4076df...782eea126dc5c755827be751a099eb01826175cf)) | [`0.0.0-20210320-0a92994`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/fp16) | STALE-MAJOR |  |
| `vpp-vcl` | `26.02-260111-85abefb.envoy` → [`85abefb55ee931fa4e45c0b6a9fc8c43118651b3`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/vpp-vcl/26.02-260111-85abefb.envoy/source.json#L1-L9) | HEAD [`4669bd8`](https://github.com/FDio/vpp/commit/4669bd8b37fdf4ffc5cd182515aa1e359405d902) (commit count unavailable / 257d newer; [compare](https://github.com/FDio/vpp/compare/85abefb55ee931fa4e45c0b6a9fc8c43118651b3...4669bd8b37fdf4ffc5cd182515aa1e359405d902)) | — | STALE-MAJOR |  |
| `emsdk` | `4.0.23.envoy` → [`c0bb220cb6e6f4e0fabb6f6db9efd53390ef5e56`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/emsdk/4.0.23.envoy/source.json#L1-L9) | HEAD [`e566f7b`](https://github.com/emscripten-core/emsdk/commit/e566f7bdcc7735f44037911c24b87a58a3c93145) (116 commits / 256d newer; [compare](https://github.com/emscripten-core/emsdk/compare/c0bb220cb6e6f4e0fabb6f6db9efd53390ef5e56...e566f7bdcc7735f44037911c24b87a58a3c93145)) | [`6.0.10`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/emsdk) | STALE-MAJOR |  |
| `proxy-wasm-rust-sdk` | `0.2.4-251205-5283e57.envoy` → [`5283e57e503c8d4773b4bc8a51e1ff486bff981c`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/proxy-wasm-rust-sdk/0.2.4-251205-5283e57.envoy/source.json#L1-L9) | HEAD [`19e691b`](https://github.com/proxy-wasm/proxy-wasm-rust-sdk/commit/19e691b3a40458d67433c8ff8ce1225f371b65ee) (commit count unavailable / 210d newer; [compare](https://github.com/proxy-wasm/proxy-wasm-rust-sdk/compare/5283e57e503c8d4773b4bc8a51e1ff486bff981c...19e691b3a40458d67433c8ff8ce1225f371b65ee)) | [`0.2.5`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/proxy-wasm-rust-sdk) | STALE-MAJOR |  |
| `aws-c-auth-testdata` | `0.10.4.envoy` → [`v0.10.4`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/aws-c-auth-testdata/0.10.4.envoy/source.json#L1-L9) | [`v1.0.0`](https://github.com/awslabs/aws-c-auth/releases/tag/v1.0.0) | — | STALE-MAJOR |  |
| `kafka` | `3.9.2.envoy` → [`3.9.2`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/kafka/3.9.2.envoy/source.json#L1-L9) | [`4.3.1`](https://github.com/apache/kafka/tags) | — | STALE-MAJOR |  |
| `msgpack-cxx` | `7.0.0.envoy` → [`cpp-7.0.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/msgpack-cxx/7.0.0.envoy/source.json#L1-L9) | [`cpp-9.0.0`](https://github.com/msgpack/msgpack-c/releases/tag/cpp-9.0.0) | — | STALE-MAJOR |  |
| `openssl` | `3.5.7.envoy` → [`openssl-3.5.7`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/openssl/3.5.7.envoy/source.json#L1-L9) | [`openssl-4.0.2`](https://github.com/openssl/openssl/releases/tag/openssl-4.0.2) | [`4.0.1.bcr.0`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/openssl) | STALE-MAJOR |  |
| `perfetto` | `57.2.envoy` → [`v57.2`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/perfetto/57.2.envoy/source.json#L1-L9) | [`v58.2`](https://github.com/google/perfetto/releases/tag/v58.2) | — | STALE-MAJOR |  |
| `protobuf` | `35.1.bcr.envoy` → [`v35.1`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/protobuf/35.1.bcr.envoy/source.json#L1-L9) | [`v36.2`](https://github.com/protocolbuffers/protobuf/releases/tag/v36.2) | [`36.2`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/protobuf) | STALE-MAJOR |  |
| `qatzip` | `1.3.2.envoy` → [`v1.3.2`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/qatzip/1.3.2.envoy/source.json#L1-L9) | [`v2.0.0`](https://github.com/intel/QATzip/releases/tag/v2.0.0) | — | STALE-MAJOR |  |
| `simdutf` | `8.1.0.envoy` → [`v8.1.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/simdutf/8.1.0.envoy/source.json#L1-L9) | [`v9.2.0`](https://github.com/simdutf/simdutf/releases/tag/v9.2.0) | [`7.7.0`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/simdutf) | STALE-MAJOR |  |
| `skywalking-data-collect-protocol` | `10.4.0.envoy` → [`v10.4.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/skywalking-data-collect-protocol/10.4.0.envoy/source.json#L1-L9) | [`v11.0.0`](https://github.com/apache/skywalking-data-collect-protocol/releases/tag/v11.0.0) | [`10.3.0`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/skywalking-data-collect-protocol) | STALE-MAJOR |  |
| `v8` | `14.6.202.10.envoy` → [`14.6.202.10`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/v8/14.6.202.10.envoy/source.json#L1-L9) | [`15.6.48`](https://github.com/v8/v8/tags) | — | STALE-MAJOR |  |
| `wasmtime` | `45.0.2.envoy` → [`v45.0.2`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/wasmtime/45.0.2.envoy/source.json#L1-L9) | [`v49.0.0`](https://github.com/bytecodealliance/wasmtime/releases/tag/v49.0.0) | — | STALE-MAJOR |  |
| `ocp-diag-core` | `0.0.0-230505-e965ac0.envoy` → [`e965ac0ac6db6686169678e2a6c77ede904fa82c`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/ocp-diag-core/0.0.0-230505-e965ac0.envoy/source.json#L1-L9) | HEAD [`8fae3f5`](https://github.com/opencomputeproject/ocp-diag-core/commit/8fae3f573a0aeb07d4fd78855f0ba2e464a8a2ad) (commit count unavailable / 35d newer; [compare](https://github.com/opencomputeproject/ocp-diag-core/compare/e965ac0ac6db6686169678e2a6c77ede904fa82c...8fae3f573a0aeb07d4fd78855f0ba2e464a8a2ad)) | — | STALE-MINOR |  |
| `proxy-wasm-cpp-host` | `0.0.0-260704-f2db56a.envoy` → [`f2db56af443571e92a31c0b877106d9ea96e19ef`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/proxy-wasm-cpp-host/0.0.0-260704-f2db56a.envoy/source.json#L1-L9) | HEAD [`5f03d89`](https://github.com/proxy-wasm/proxy-wasm-cpp-host/commit/5f03d8991f9ff802b728f60f817e7c8450183631) (commit count unavailable / 23d newer; [compare](https://github.com/proxy-wasm/proxy-wasm-cpp-host/compare/f2db56af443571e92a31c0b877106d9ea96e19ef...5f03d8991f9ff802b728f60f817e7c8450183631)) | — | STALE-MINOR |  |
| `envoy` | `1.40.0-dev.20260904.13144fb.envoy` → [`13144fbbb3800f1a41c45d17dc9de44978b567b1`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/envoy/1.40.0-dev.20260904.13144fb.envoy/source.json#L1-L9) | HEAD [`a712680`](https://github.com/envoyproxy/envoy/commit/a712680a0725ad8fe401d9bceb1a356efd58d2fc) (321 commits / 19d newer; [compare](https://github.com/envoyproxy/envoy/compare/13144fbbb3800f1a41c45d17dc9de44978b567b1...a712680a0725ad8fe401d9bceb1a356efd58d2fc)) | — | STALE-MINOR |  |
| `envoy_api` | `1.40.0-dev.20260904.13144fb.envoy` → [`13144fbbb3800f1a41c45d17dc9de44978b567b1`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/envoy_api/1.40.0-dev.20260904.13144fb.envoy/source.json#L1-L9) | HEAD [`a712680`](https://github.com/envoyproxy/envoy/commit/a712680a0725ad8fe401d9bceb1a356efd58d2fc) (321 commits / 19d newer; [compare](https://github.com/envoyproxy/envoy/compare/13144fbbb3800f1a41c45d17dc9de44978b567b1...a712680a0725ad8fe401d9bceb1a356efd58d2fc)) | [`0.0.0-20260901-005c18a.bcr.1`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/envoy_api) | STALE-MINOR |  |
| `protoc-gen-jsonschema` | `0.0.0-20230530-7680e49.envoy` → [`7680e4998426e62b6896995ff73d4d91cc5fb13c`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/protoc-gen-jsonschema/0.0.0-20230530-7680e49.envoy/source.json#L1-L9) | HEAD [`e35f2ad`](https://github.com/norbjd/protoc-gen-jsonschema/commit/e35f2ad05c0ccbf9208a884dcb92c72529ea2e02) (commit count unavailable / 7d newer; [compare](https://github.com/norbjd/protoc-gen-jsonschema/compare/7680e4998426e62b6896995ff73d4d91cc5fb13c...e35f2ad05c0ccbf9208a884dcb92c72529ea2e02)) | — | STALE-MINOR |  |
| `boost.headers` | `1.89.0.envoy` → [`1.89.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/boost.headers/1.89.0.envoy/source.json#L1-L9) | [`1.92.0`](https://archives.boost.io/release/1.92.0/) | [`1.90.0.bcr.1`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/boost.headers) | STALE-MINOR |  |
| `cel-cpp` | `0.14.0.envoy` → [`v0.14.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/cel-cpp/0.14.0.envoy/source.json#L1-L9) | [`v0.16.1`](https://github.com/cel-expr/cel-cpp/releases/tag/v0.16.1) | [`0.16.1`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/cel-cpp) | STALE-MINOR |  |
| `dd-trace-cpp` | `2.1.1.envoy` → [`v2.1.1`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/dd-trace-cpp/2.1.1.envoy/source.json#L1-L9) | [`v2.2.0`](https://github.com/DataDog/dd-trace-cpp/releases/tag/v2.2.0) | — | STALE-MINOR |  |
| `elfutils` | `0.195.envoy` → [`0.195`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/elfutils/0.195.envoy/source.json#L1-L9) | [`0.196`](https://sourceware.org/elfutils/ftp/) | [`0.195`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/elfutils) | STALE-MINOR |  |
| `go-fips` | `1.24.12.envoy` → [`1.24.12`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/go-fips/1.24.12.envoy/source.json#L1-L9) | [`1.27.1`](https://go.dev/dl/) | — | STALE-MINOR |  |
| `grpc` | `1.83.0.envoy` → [`v1.83.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/grpc/1.83.0.envoy/source.json#L1-L9) | [`v1.84.0`](https://github.com/grpc/grpc/releases/tag/v1.84.0) | [`1.84.0`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/grpc) | STALE-MINOR |  |
| `icu` | `78.2.envoy` → [`release-78.2`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/icu/78.2.envoy/source.json#L1-L9) | [`release-78.3`](https://github.com/unicode-org/icu/releases/tag/release-78.3) | [`78.2.bcr.2`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/icu) | STALE-MINOR |  |
| `ipp-crypto` | `2.2.0.envoy` → [`v2.2.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/ipp-crypto/2.2.0.envoy/source.json#L1-L9) | [`v2.3.0`](https://github.com/intel/cryptography-primitives/releases/tag/v2.3.0) | — | STALE-MINOR |  |
| `libmaxminddb` | `1.13.3.envoy` → [`1.13.3`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/libmaxminddb/1.13.3.envoy/source.json#L1-L9) | [`1.14.1`](https://github.com/maxmind/libmaxminddb/releases/tag/1.14.1) | [`1.12.2`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/libmaxminddb) | STALE-MINOR |  |
| `librdkafka` | `2.6.0.envoy` → [`v2.6.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/librdkafka/2.6.0.envoy/source.json#L1-L9) | [`v2.15.1`](https://github.com/confluentinc/librdkafka/releases/tag/v2.15.1) | [`2.15.0`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/librdkafka) | STALE-MINOR |  |
| `nghttp2` | `1.66.0.envoy` → [`v1.66.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/nghttp2/1.66.0.envoy/source.json#L1-L9) | [`v1.70.0`](https://github.com/nghttp2/nghttp2/releases/tag/v1.70.0) | [`1.65.0`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/nghttp2) | STALE-MINOR |  |
| `prometheus-metrics-model` | `0.6.2.envoy` → [`v0.6.2`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/prometheus-metrics-model/0.6.2.envoy/source.json#L1-L9) | [`v0.6.3`](https://github.com/prometheus/client_model/releases/tag/v0.6.3) | — | STALE-MINOR |  |
| `qatlib` | `26.02.0.envoy` → [`26.02.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/qatlib/26.02.0.envoy/source.json#L1-L9) | [`26.08.0`](https://github.com/intel/qatlib/releases/tag/26.08.0) | — | STALE-MINOR |  |
| `quiche` | `0.0.0-260922-7f07dc4.envoy` → [`7f07dc4d14c5702607a0dee9c7e4ab07f63f9883`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/quiche/0.0.0-260922-7f07dc4.envoy/source.json#L1-L9) | HEAD [`41ee992`](https://github.com/google/quiche/commit/41ee992597583771801dcb8569e1eca71842ef74) (commit count unavailable / 0d newer; [compare](https://github.com/google/quiche/compare/7f07dc4d14c5702607a0dee9c7e4ab07f63f9883...41ee992597583771801dcb8569e1eca71842ef74)) | — | STALE-MINOR |  |
| `rules_rust` | `0.69.0.envoy` → [`0.69.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/rules_rust/0.69.0.envoy/source.json#L1-L9) | [`0.74.0`](https://github.com/bazelbuild/rules_rust/releases/tag/0.74.0) | [`0.74.0`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/rules_rust) | STALE-MINOR |  |
| `uadk` | `2.9.envoy` → [`v2.9`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/uadk/2.9.envoy/source.json#L1-L9) | [`v2.11`](https://github.com/Linaro/uadk/tags) | — | STALE-MINOR |  |
| `wamr` | `2.4.4.envoy` → [`WAMR-2.4.4`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/wamr/2.4.4.envoy/source.json#L1-L9) | [`WAMR-2.4.5`](https://github.com/wasm-micro-runtime/wasm-micro-runtime/releases/tag/WAMR-2.4.5) | — | STALE-MINOR |  |
| `wuffs` | `0.4.0-alpha.9.envoy` → [`v0.4.0-alpha.9`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/wuffs/0.4.0-alpha.9.envoy/source.json#L1-L9) | [`v0.4.0-alpha.10`](https://github.com/google/wuffs-mirror-release-c/tags) | — | STALE-MINOR |  |
| `yq.bzl` | `0.1.1.envoy` → [`v0.1.1`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/yq.bzl/0.1.1.envoy/source.json#L1-L9) | [`v0.4.0`](https://github.com/bazel-contrib/yq.bzl/releases/tag/v0.4.0) | [`0.4.0`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/yq.bzl) | STALE-MINOR |  |
| `zlib-ng` | `2.3.2.envoy` → [`2.3.2`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/zlib-ng/2.3.2.envoy/source.json#L1-L9) | [`2.3.3`](https://github.com/zlib-ng/zlib-ng/releases/tag/2.3.3) | [`2.3.3.bcr.2`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/zlib-ng) | STALE-MINOR |  |
| `sq` | `1.4.0.envoy` → [`1.4.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/sq/1.4.0.envoy/source.json#L1-L9) | [`v1.4.1`](https://gitlab.com/sequoia-pgp/sequoia-sq/-/tags/v1.4.1) | — | STALE-MINOR | GitLab releases API 404ed; tags page shows `v1.4.1` as latest release tag. |
| `vectorscan` | `5.4.11.envoy` → [`vectorscan/5.4.11`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/vectorscan/5.4.11.envoy/source.json#L1-L9) | [`vectorscan/5.4.13`](https://github.com/VectorCamp/vectorscan/releases/tag/vectorscan/5.4.13) | — | STALE-MINOR | Latest tag determined from upstream release/tag namespace. |
| `boringssl-fips` | `0.20260813.0.envoy` → [`0.20260813.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/boringssl-fips/0.20260813.0.envoy/source.json#L1-L9) | [`0.20260813.0`](https://github.com/google/boringssl/releases/tag/0.20260813.0) | — | CURRENT |  |
| `boringssl-source` | `0.20260813.0.envoy` → [`0.20260813.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/boringssl-source/0.20260813.0.envoy/source.json#L1-L9) | [`0.20260813.0`](https://github.com/google/boringssl/releases/tag/0.20260813.0) | — | CURRENT |  |
| `cpp2sky` | `0.6.0.envoy` → [`v0.6.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/cpp2sky/0.6.0.envoy/source.json#L1-L9) | [`v0.6.0`](https://github.com/SkyAPM/cpp2sky/releases/tag/v0.6.0) | [`0.6.1-20251203-dfc5bd9`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/cpp2sky) | CURRENT |  |
| `envoy-example-filter-cc` | `0.2.6.envoy` → [`v0.2.6`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/envoy-example-filter-cc/0.2.6.envoy/source.json#L1-L9) | [`v0.2.6`](https://github.com/envoyproxy/examples/releases/tag/v0.2.6) | — | CURRENT |  |
| `envoy-example-wasm-cc` | `0.2.6.envoy` → [`v0.2.6`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/envoy-example-wasm-cc/0.2.6.envoy/source.json#L1-L9) | [`v0.2.6`](https://github.com/envoyproxy/examples/releases/tag/v0.2.6) | — | CURRENT |  |
| `envoy-examples` | `0.2.6.envoy` → [`v0.2.6`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/envoy-examples/0.2.6.envoy/source.json#L1-L9) | [`v0.2.6`](https://github.com/envoyproxy/examples/releases/tag/v0.2.6) | — | CURRENT |  |
| `envoy_toolshed` | `0.4.15.envoy` → [`bazel-v0.4.15`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/envoy_toolshed/0.4.15.envoy/source.json#L1-L9) | [`bazel-v0.4.15`](https://github.com/envoyproxy/toolshed/releases/tag/bazel-v0.4.15) | [`0.3.25`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/envoy_toolshed) | CURRENT |  |
| `envoy_toolshed_jq` | `0.4.15.envoy` → [`bazel-v0.4.15`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/envoy_toolshed_jq/0.4.15.envoy/source.json#L1-L9) | [`bazel-v0.4.15`](https://github.com/envoyproxy/toolshed/releases/tag/bazel-v0.4.15) | — | CURRENT |  |
| `grpc-httpjson-transcoding` | `0.0.0-20250507-a6e226f.envoy` → [`a6e226f9a2e656a973df3ad48f0ee5efacce1a28`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/grpc-httpjson-transcoding/0.0.0-20250507-a6e226f.envoy/source.json#L1-L9) | [`a6e226f`](https://github.com/grpc-ecosystem/grpc-httpjson-transcoding/commit/a6e226f9a2e656a973df3ad48f0ee5efacce1a28) (HEAD) | [`0.0.0-20230607-ff41eb3`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/grpc-httpjson-transcoding) | CURRENT |  |
| `hermetic-android-toolchains` | `0.4.0.envoy` → [`0.4.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/hermetic-android-toolchains/0.4.0.envoy/source.json#L1-L9) | [`0.4.0`](https://github.com/keith/hermetic_android_toolchains/releases/tag/0.4.0) | — | CURRENT |  |
| `hessian2-codec` | `0.0.0-250114-6f5a647.envoy` → [`6f5a64770f0374a761eece13c8863b80dc5adcd8`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/hessian2-codec/0.0.0-250114-6f5a647.envoy/source.json#L1-L9) | [`6f5a647`](https://github.com/alibaba/hessian2-codec/commit/6f5a64770f0374a761eece13c8863b80dc5adcd8) (HEAD) | — | CURRENT |  |
| `hyperscan` | `5.4.2.envoy` → [`v5.4.2`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/hyperscan/5.4.2.envoy/source.json#L1-L9) | [`v5.4.2`](https://github.com/intel/hyperscan/releases/tag/v5.4.2) | — | CURRENT |  |
| `libbpf` | `1.7.0.envoy` → [`v1.7.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/libbpf/1.7.0.envoy/source.json#L1-L9) | [`v1.7.0`](https://github.com/libbpf/libbpf/releases/tag/v1.7.0) | [`1.7.0`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/libbpf) | CURRENT |  |
| `libcircllhist` | `0.3.2.envoy` → [`py-0.3.2`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/libcircllhist/0.3.2.envoy/source.json#L1-L9) | [`py-0.3.2`](https://github.com/openhistogram/libcircllhist/tags) | [`0.3.2.bcr.1`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/libcircllhist) | CURRENT |  |
| `libevent` | `2.2.2-alpha.envoy` → [`release-2.2.2-alpha`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/libevent/2.2.2-alpha.envoy/source.json#L1-L9) | [`release-2.2.2-alpha`](https://github.com/libevent/libevent/tags) | [`2.1.12-stable.bcr.0`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/libevent) | CURRENT |  |
| `liburing` | `2.15.envoy` → [`liburing-2.15`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/liburing/2.15.envoy/source.json#L1-L9) | [`liburing-2.15`](https://github.com/axboe/liburing/releases/tag/liburing-2.15) | [`2.15`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/liburing) | CURRENT |  |
| `lz4` | `1.10.0.bcr.2.envoy` → [`v1.10.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/lz4/1.10.0.bcr.2.envoy/source.json#L1-L9) | [`v1.10.0`](https://github.com/lz4/lz4/releases/tag/v1.10.0) | [`1.10.0.bcr.1`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/lz4) | CURRENT |  |
| `proto-converter` | `0.0.0-20260912-3850764.envoy` → [`385076472517e4e006cfb7a2c5401b918c233d7d`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/proto-converter/0.0.0-20260912-3850764.envoy/source.json#L1-L9) | [`3850764`](https://github.com/grpc-ecosystem/proto-converter/commit/385076472517e4e006cfb7a2c5401b918c233d7d) (HEAD) | [`0.0.0-20230607-d77ff30`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/proto-converter) | CURRENT |  |
| `proto-field-extraction` | `0.0.0-240710-d5d39f0.envoy` → [`d5d39f0373e9b6691c32c85929838b1006bcb3fb`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/proto-field-extraction/0.0.0-240710-d5d39f0.envoy/source.json#L1-L9) | [`d5d39f0`](https://github.com/grpc-ecosystem/proto-field-extraction/commit/d5d39f0373e9b6691c32c85929838b1006bcb3fb) (HEAD) | — | CURRENT |  |
| `proto-processing` | `0.0.0-250110-279353c.envoy` → [`279353cfab372ac7f268ae529df29c4d546ca18d`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/proto-processing/0.0.0-250110-279353c.envoy/source.json#L1-L9) | [`279353c`](https://github.com/grpc-ecosystem/proto_processing_lib/commit/279353cfab372ac7f268ae529df29c4d546ca18d) (HEAD) | — | CURRENT |  |
| `protoc-gen-validate` | `1.3.3.envoy` → [`v1.3.3`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/protoc-gen-validate/1.3.3.envoy/source.json#L1-L9) | [`v1.3.3`](https://github.com/bufbuild/protoc-gen-validate/releases/tag/v1.3.3) | [`1.3.3`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/protoc-gen-validate) | CURRENT |  |
| `qat-zstd` | `1.0.0.envoy` → [`v1.0.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/qat-zstd/1.0.0.envoy/source.json#L1-L9) | [`v1.0.0`](https://github.com/intel/QAT-ZSTD-Plugin/releases/tag/v1.0.0) | — | CURRENT |  |
| `sql-parser` | `0.0.0-260715-52e5ad1.envoy` → [`52e5ad1f4fbb21301fcee7f9d18eef7e6ae6ab3e`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/sql-parser/0.0.0-260715-52e5ad1.envoy/source.json#L1-L9) | [`52e5ad1`](https://github.com/envoyproxy/sql-parser/commit/52e5ad1f4fbb21301fcee7f9d18eef7e6ae6ab3e) (HEAD) | — | CURRENT |  |
| `thrift` | `0.24.0.envoy` → [`v0.24.0`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/thrift/0.24.0.envoy/source.json#L1-L9) | [`v0.24.0`](https://github.com/apache/thrift/releases/tag/v0.24.0) | [`0.22.0`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/thrift) | CURRENT |  |
| `toolchains_llvm` | `1.9.1.envoy` → [`v1.9.1`](https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/toolchains_llvm/1.9.1.envoy/source.json#L1-L9) | [`v1.9.1`](https://github.com/bazel-contrib/toolchains_llvm/releases/tag/v1.9.1) | [`1.9.1`](https://github.com/bazelbuild/bazel-central-registry/tree/main/modules/toolchains_llvm) | CURRENT |  |

## 2. Patch debt — every patched module

### 2A. Highest-value patch-drop findings

## Section 2 — Highest-signal patch findings

### A. Generic-fix / security-backport patches

| Module | Patch | Category | What it does | Upstream later release? |
|---|---|---|---|---|
| `quiche/0.0.0-260831-5c9cc6b.envoy` | `oghttp2_trailer_fix.patch` | generic-fix | Rejects HTTP/2 trailers unless `END_STREAM` is set. `envoyproxy/bazel-registry:modules/quiche/0.0.0-260831-5c9cc6b.envoy/patches/oghttp2_trailer_fix.patch:1-18` | **Yes.** Local later snapshot `0.0.0-260922-7f07dc4.envoy` drops this patch entirely, and upstream `main` contains the same check (`"Trailers must contain END_STREAM"`). `envoyproxy/bazel-registry:modules/quiche/0.0.0-260831-5c9cc6b.envoy/source.json:1-13`, `envoyproxy/bazel-registry:modules/quiche/0.0.0-260922-7f07dc4.envoy/source.json:1-12`, https://github.com/google/quiche/blob/main/quiche/http2/adapter/oghttp2_session.cc |
| `qatzip/1.3.2.envoy` | `cast.patch` | generic-fix | Removes unnecessary casts from public compression-format macros in `qatzip.h`. `envoyproxy/bazel-registry:modules/qatzip/1.3.2.envoy/patches/cast.patch:1-25` | **Not verified** in a later upstream release in this pass. Current upstream file/tags do not give a clear released equivalent. https://github.com/intel/QATzip/blob/master/include/qatzip.h , https://github.com/intel/QATzip/tags |
| `elfutils/0.195.envoy` | `assert_perror.patch` | generic-fix | Adds a fallback `assert_perror` definition when libc/toolchain headers omit it. `envoyproxy/bazel-registry:modules/elfutils/0.195.envoy/patches/assert_perror.patch:1-12` | **Yes — elfutils 0.196.** Upstream commit `45e604d4e42d` and tag `0.196`. https://sourceware.org/git/?p=elfutils.git;a=commit;h=45e604d4e42d , https://sourceware.org/git/?p=elfutils.git;a=tag;h=refs/tags/0.196 |
| `liburing/2.15.envoy` | `liburing.patch` | generic-fix | Makes `AR` / `RANLIB` honor `EXT_BUILD_ROOT` before archive creation. `envoyproxy/bazel-registry:modules/liburing/2.15.envoy/patches/liburing.patch:1-36` | **Yes — liburing 2.16.** Upstream commit `e6ed2f979c2e1511f280dd2d5be7f43a6c6dadd8` is in `liburing-2.16`. https://github.com/axboe/liburing/commit/e6ed2f979c2e1511f280dd2d5be7f43a6c6dadd8 , https://github.com/axboe/liburing/releases/tag/liburing-2.16 |
| `nghttp2/1.66.0.envoy` | `nghttp2-CVE-2026-27135_part1..4.patch` | security-backport | Backports the CVE-2026-27135 fix set: zero-length `ALTSVC` handling, extra ignore-state/fatal-state guards, and regression tests. `envoyproxy/bazel-registry:modules/nghttp2/1.66.0.envoy/patches/nghttp2-CVE-2026-27135_part1.patch:1-49`, `...part2.patch:1-26`, `...part3.patch:1-160`, `...part4.patch:1-111` | **Yes — verified by `v1.68.1`.** Security fix commit `5c7df8fa815ac1004d9ecb9d1f7595c4d37f46e1`; release `v1.68.1`. https://github.com/nghttp2/nghttp2/commit/5c7df8fa815ac1004d9ecb9d1f7595c4d37f46e1 , https://github.com/nghttp2/nghttp2/releases/tag/v1.68.1 |
| `nghttp2/1.66.0.envoy` | `nghttp2_huffman.patch` | security-backport | Adds a disable-Huffman option and no-Huffman emit path. `envoyproxy/bazel-registry:modules/nghttp2/1.66.0.envoy/patches/nghttp2_huffman.patch:1-160` | **Yes — present in later upstream; verified by `v1.68.1`** (and likely earlier in the 1.67.x line). https://github.com/nghttp2/nghttp2/releases/tag/v1.68.1 |
| `nghttp2/1.66.0.envoy` | `nghttp2_max_hd_nv.patch` | security-backport | Adds configurable max header name/value size limits. `envoyproxy/bazel-registry:modules/nghttp2/1.66.0.envoy/patches/nghttp2_max_hd_nv.patch:1-119` | **Yes — present in later upstream; verified by `v1.68.1`** (likely earlier in 1.67.x). https://github.com/nghttp2/nghttp2/releases/tag/v1.68.1 |

### B. Protobuf-v35 compatibility patches to watch on bump

These are not generic/security patches, but they are the most important “does upstream now contain it?” checks from a bump-risk perspective.

| Module | Patch | What it does | Upstream status in this pass |
|---|---|---|---|
| `cel-cpp/0.14.0.envoy` | `cel-cpp-protobuf-v35.patch` | Replaces deprecated `FieldDescriptor::label()` logic with `is_repeated()`-based checks. `envoyproxy/bazel-registry:modules/cel-cpp/0.14.0.envoy/patches/cel-cpp-protobuf-v35.patch:1-40` | **Not confirmed** from a released upstream tag in this pass. Keep as a bump checkpoint. |
| `proxy-wasm-cpp-sdk/0.0.0-250925-e5256b0.envoy` | `proxy_wasm_cpp_sdk-protobuf-v35.patch` | Explicitly discards `ParseFromArray()`’s `[[nodiscard]]` result. `envoyproxy/bazel-registry:modules/proxy-wasm-cpp-sdk/0.0.0-250925-e5256b0.envoy/patches/proxy_wasm_cpp_sdk-protobuf-v35.patch:1-11` | **Not confirmed** upstream in this pass. |
| `proto-field-extraction/0.0.0-240710-d5d39f0.envoy` | `protobuf-v35.patch` | Adds `-Wno-unused-result` and explicit result-discard casts for protobuf-v35 API changes. `envoyproxy/bazel-registry:modules/proto-field-extraction/0.0.0-240710-d5d39f0.envoy/patches/protobuf-v35.patch:1-140` | **Not confirmed** upstream in this pass. |

### 2B. Complete patch inventory

## 2. Patch-carrying hosted module versions

- `cpp2sky/0.6.0.envoy`
  - `cpp2sky.patch` — switches `cc_proto_library` loads from `rules_cc` to protobuf’s Bazel defs in two BUILD files; **envoy-specific**. `envoyproxy/bazel-registry:modules/cpp2sky/0.6.0.envoy/patches/cpp2sky.patch:1-20`

- `zlib-ng/2.3.2.envoy`
  - `add_module_dot_bazel.patch` — adds a root `MODULE.bazel`; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/zlib-ng/2.3.2.envoy/patches/add_module_dot_bazel.patch:1-11`
  - `add_build_file.patch` — adds a full Bazel BUILD, adapted from LLVM’s third-party `zlib-ng` rules; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/zlib-ng/2.3.2.envoy/patches/add_build_file.patch:1-120`
  - Upstream shim status: upstream root still lacks native `MODULE.bazel`/`BUILD(.bazel)` in the repo root listing, so this is **not droppable yet**.

- `quiche/0.0.0-260831-5c9cc6b.envoy`
  - `oghttp2_trailer_fix.patch` — rejects request/response trailers that do not carry `END_STREAM`; **generic-fix**. `envoyproxy/bazel-registry:modules/quiche/0.0.0-260831-5c9cc6b.envoy/patches/oghttp2_trailer_fix.patch:1-18`
    - Later-upstream status: **yes**. The later local snapshot `0.0.0-260922-7f07dc4.envoy` drops this patch entirely from `source.json` while upstream head contains the same `Trailers must contain END_STREAM` check. `envoyproxy/bazel-registry:modules/quiche/0.0.0-260831-5c9cc6b.envoy/source.json:1-13`, `envoyproxy/bazel-registry:modules/quiche/0.0.0-260922-7f07dc4.envoy/source.json:1-12`, https://github.com/google/quiche/blob/main/quiche/http2/adapter/oghttp2_session.cc
  - `delete-bazel-files.patch` — renames upstream `BUILD.bazel` files out of the way so Envoy’s overlay can replace them; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/quiche/0.0.0-260831-5c9cc6b.envoy/patches/delete-bazel-files.patch:1-8`
  - Upstream shim status: upstream now ships both `MODULE.bazel` and `BUILD.bazel`, so native Bazel support exists; this patch is only needed because Envoy intentionally overrides upstream rules. https://github.com/google/quiche/blob/main/MODULE.bazel , https://github.com/google/quiche/blob/main/BUILD.bazel

- `quiche/0.0.0-260922-7f07dc4.envoy`
  - `delete-bazel-files.patch` — same overlay-forcing rename as above; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/quiche/0.0.0-260922-7f07dc4.envoy/patches/delete-bazel-files.patch:1-8`

- `tcmalloc/0.0.0-250926-12f2552.envoy`
  - `tcmalloc.patch` — makes `tcmalloc/BUILD` public-visibility; **envoy-specific**. `envoyproxy/bazel-registry:modules/tcmalloc/0.0.0-250926-12f2552.envoy/patches/tcmalloc.patch:1-9`

- `rules_rust/0.69.0.envoy`
  - `rules_rust.patch` — relaxes crate-universe assumptions for multi-module reuse and disables a coverage flag / tweaks `CrateInfo` emission; **envoy-specific**. `envoyproxy/bazel-registry:modules/rules_rust/0.69.0.envoy/patches/rules_rust.patch:1-99`

- `proxy-wasm-cpp-sdk/0.0.0-250925-e5256b0.envoy`
  - `proxy_wasm_cpp_sdk-protobuf-v35.patch` — suppresses protobuf-v35 `[[nodiscard]]` fallout on `ParseFromArray`; **envoy-specific**. `envoyproxy/bazel-registry:modules/proxy-wasm-cpp-sdk/0.0.0-250925-e5256b0.envoy/patches/proxy_wasm_cpp_sdk-protobuf-v35.patch:1-11`
  - `proxy-wasm-cpp-sdk.patch` — rewires labels to local targets and disables fission for wasm/LTO; **envoy-specific**. `envoyproxy/bazel-registry:modules/proxy-wasm-cpp-sdk/0.0.0-250925-e5256b0.envoy/patches/proxy-wasm-cpp-sdk.patch:1-68`

- `boost.headers/1.89.0.envoy`
  - `add_build_file.patch` — adds a header-only Bazel target for Boost headers; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/boost.headers/1.89.0.envoy/patches/add_build_file.patch:1-19`
  - Upstream shim status: upstream `boostorg/headers` root still lacks native `MODULE.bazel`/`BUILD(.bazel)`, so **not droppable yet**.

- `qatzip/1.3.2.envoy`
  - `cast.patch` — removes unnecessary casts in public macro constants in `qatzip.h`; **generic-fix**. `envoyproxy/bazel-registry:modules/qatzip/1.3.2.envoy/patches/cast.patch:1-25`
    - Later-upstream status: **no clear later release found**; current upstream `include/qatzip.h` and tags do not show a verified released cleanup. https://github.com/intel/QATzip/blob/master/include/qatzip.h , https://github.com/intel/QATzip/tags

- `cel-cpp/0.14.0.envoy`
  - `cel-cpp.patch` — null-guards `ByteString` input, adds `[[maybe_unused]]`, and fixes signed/unsigned DCHECK usage; **envoy-specific**. `envoyproxy/bazel-registry:modules/cel-cpp/0.14.0.envoy/patches/cel-cpp.patch:1-62`
  - `cel-cpp-protobuf-v35.patch` — replaces deprecated `FieldDescriptor::label()` logic with `is_repeated()`-based checks; **envoy-specific**. `envoyproxy/bazel-registry:modules/cel-cpp/0.14.0.envoy/patches/cel-cpp-protobuf-v35.patch:1-40`

- `elfutils/0.195.envoy`
  - `assert_perror.patch` — defines `assert_perror` when libc/toolchain headers do not provide it; **generic-fix**. `envoyproxy/bazel-registry:modules/elfutils/0.195.envoy/patches/assert_perror.patch:1-12`
    - Later-upstream status: **yes, elfutils 0.196** via commit `45e604d4e42d`. https://sourceware.org/git/?p=elfutils.git;a=commit;h=45e604d4e42d , https://sourceware.org/git/?p=elfutils.git;a=tag;h=refs/tags/0.196

- `protobuf/35.1.bcr.envoy`
  - `envoy.patch` — adds a root `label_flag` for zlib, exports additional proto files, broadens visibility, and refreshes tool-integrity metadata for protobuf 35.1; **envoy-specific**. `envoyproxy/bazel-registry:modules/protobuf/35.1.bcr.envoy/patches/envoy.patch:1-130`

- `googleurl/0.0.0-221103-dd4080f.envoy`
  - `googleurl.patch` — removes non-clang-cl Windows hard error and layers on multiple warning/iterator compatibility fixes; **envoy-specific**. `envoyproxy/bazel-registry:modules/googleurl/0.0.0-221103-dd4080f.envoy/patches/googleurl.patch:1-153`

- `librdkafka/2.6.0.envoy`
  - `src_rd.h.patch` — fixes `config.h` include path; **envoy-specific**. `envoyproxy/bazel-registry:modules/librdkafka/2.6.0.envoy/patches/src_rd.h.patch:1-9`
  - `src-cpp_rdkafkacpp_int.h.patch` — same include-path fix for C++ internals; **envoy-specific**. `envoyproxy/bazel-registry:modules/librdkafka/2.6.0.envoy/patches/src-cpp_rdkafkacpp_int.h.patch:1-9`
  - `src_tinycthread.h.patch` — same include-path fix for tinycthread; **envoy-specific**. `envoyproxy/bazel-registry:modules/librdkafka/2.6.0.envoy/patches/src_tinycthread.h.patch:1-9`
  - `tests_testcpp.h.patch` — same include-path fix for tests; **envoy-specific**. `envoyproxy/bazel-registry:modules/librdkafka/2.6.0.envoy/patches/tests_testcpp.h.patch:1-10`
  - `envoy-remove-cjson.patch` — removes bundled `cJSON` from build inputs and init; **envoy-specific**. `envoyproxy/bazel-registry:modules/librdkafka/2.6.0.envoy/patches/envoy-remove-cjson.patch:1-84`

- `proto-converter/0.0.0-20260912-3850764.envoy`
  - `proto-converter.patch` — trims protobuf-lite BUILD wiring away from `common.cc/common.h/port_def` and relaxes exports; **envoy-specific**. `envoyproxy/bazel-registry:modules/proto-converter/0.0.0-20260912-3850764.envoy/patches/proto-converter.patch:1-153`
  - `module_dot_bazel.patch` — adds `MODULE.bazel`; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/proto-converter/0.0.0-20260912-3850764.envoy/patches/module_dot_bazel.patch:1-45`
  - Upstream shim status: upstream `grpc-ecosystem/proto-converter` has Bazel BUILD files but no root `MODULE.bazel`, so **not droppable yet**.

- `thrift/0.24.0.envoy`
  - `thrift.patch` — removes `wheel` from Python build-system requirements; **envoy-specific**. `envoyproxy/bazel-registry:modules/thrift/0.24.0.envoy/patches/thrift.patch:1-9`

- `hyperscan/5.4.2.envoy`
  - `hyperscan.patch` — initializes `val` before a masked 512-bit load path in `teddy_runtime_common.h`; **envoy-specific**. `envoyproxy/bazel-registry:modules/hyperscan/5.4.2.envoy/patches/hyperscan.patch:1-12`

- `liburing/2.15.envoy`
  - `liburing.patch` — makes `AR`/`RANLIB` honor `EXT_BUILD_ROOT` before archive creation; **generic-fix**. `envoyproxy/bazel-registry:modules/liburing/2.15.envoy/patches/liburing.patch:1-36`
    - Later-upstream status: **yes, liburing 2.16** via commit `e6ed2f979c2e1511f280dd2d5be7f43a6c6dadd8`. https://github.com/axboe/liburing/commit/e6ed2f979c2e1511f280dd2d5be7f43a6c6dadd8 , https://github.com/axboe/liburing/releases/tag/liburing-2.16

- `grpc/1.83.0.envoy`
  - `grpc.patch` — disables layering checks, removes Apple universal-binary logic, strips always-inline attributes in promises, and swaps BoringSSL/OpenSSL APIs; **envoy-specific**. `envoyproxy/bazel-registry:modules/grpc/1.83.0.envoy/patches/grpc.patch:1-220`

- `protoc-gen-validate/1.3.3.envoy`
  - `pgv.patch` — parameterizes protobuf/re2 deps for PGV C++ rules; **envoy-specific**. `envoyproxy/bazel-registry:modules/protoc-gen-validate/1.3.3.envoy/patches/pgv.patch:1-24`
  - `bazel_9_fixes.patch` — updates Java/toolchain loads for newer Bazel/rules_java; **envoy-specific**. `envoyproxy/bazel-registry:modules/protoc-gen-validate/1.3.3.envoy/patches/bazel_9_fixes.patch:1-11`
  - `self_labels.patch` — replaces self-references like `@com_envoyproxy_protoc_gen_validate//...` with repo-relative labels; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/protoc-gen-validate/1.3.3.envoy/patches/self_labels.patch:1-84`
  - Upstream shim status: upstream `bufbuild/protoc-gen-validate` has `BUILD.bazel` but no root `MODULE.bazel`, so **not droppable yet**.

- `proto-processing/0.0.0-250110-279353c.envoy`
  - `ocp.patch` — renames `@ocp//...` deps to `@ocp-diag-core//...`; **envoy-specific**. `envoyproxy/bazel-registry:modules/proto-processing/0.0.0-250110-279353c.envoy/patches/ocp.patch:1-67`

- `nghttp2/1.66.0.envoy`
  - `nghttp2.patch` — adjusts CMake’s fallback `ssize_t` choice for Win64; **envoy-specific**. `envoyproxy/bazel-registry:modules/nghttp2/1.66.0.envoy/patches/nghttp2.patch:1-13`
  - `nghttp2_huffman.patch` — adds a `disable_huffman` option and no-huffman emit path; **security-backport**. `envoyproxy/bazel-registry:modules/nghttp2/1.66.0.envoy/patches/nghttp2_huffman.patch:1-160`
  - `nghttp2_max_hd_nv.patch` — adds configurable max header name/value size enforcement; **security-backport**. `envoyproxy/bazel-registry:modules/nghttp2/1.66.0.envoy/patches/nghttp2_max_hd_nv.patch:1-119`
  - `nghttp2-CVE-2026-27135_part1.patch` — zero-length `ALTSVC` payload safety fix; **security-backport**. `envoyproxy/bazel-registry:modules/nghttp2/1.66.0.envoy/patches/nghttp2-CVE-2026-27135_part1.patch:1-49`
  - `nghttp2-CVE-2026-27135_part2.patch` — early fatal/ignore-state handling in `session_mem_recv2`; **security-backport**. `envoyproxy/bazel-registry:modules/nghttp2/1.66.0.envoy/patches/nghttp2-CVE-2026-27135_part2.patch:1-26`
  - `nghttp2-CVE-2026-27135_part3.patch` — adds exhaustive session-termination regression tests; **security-backport**. `envoyproxy/bazel-registry:modules/nghttp2/1.66.0.envoy/patches/nghttp2-CVE-2026-27135_part3.patch:1-160`
  - `nghttp2-CVE-2026-27135_part4.patch` — more ignore-state guards after callbacks/parse transitions; **security-backport**. `envoyproxy/bazel-registry:modules/nghttp2/1.66.0.envoy/patches/nghttp2-CVE-2026-27135_part4.patch:1-111`
    - Later-upstream status: **yes**; the upstream bundle is present by **v1.68.1** (security fix commit `5c7df8fa815ac1004d9ecb9d1f7595c4d37f46e1`; web evidence also points to `v1.67.0` for the Huffman/max-header-size support). https://github.com/nghttp2/nghttp2/commit/5c7df8fa815ac1004d9ecb9d1f7595c4d37f46e1 , https://github.com/nghttp2/nghttp2/releases/tag/v1.68.1 , https://github.com/nghttp2/nghttp2/releases/tag/v1.67.0

- `grpc-httpjson-transcoding/0.0.0-20250507-a6e226f.envoy`
  - `grpc-httpjson-transcoding.patch` — adds Bazel module extensions for `googleapis` and fixes `pb::int64` use to `int64_t`; **envoy-specific**. `envoyproxy/bazel-registry:modules/grpc-httpjson-transcoding/0.0.0-20250507-a6e226f.envoy/patches/grpc-httpjson-transcoding.patch:1-64`
  - `module_dot_bazel.patch` — adds `MODULE.bazel`; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/grpc-httpjson-transcoding/0.0.0-20250507-a6e226f.envoy/patches/module_dot_bazel.patch:1-66`
  - Upstream shim status: upstream has `BUILD` but no `MODULE.bazel`, so **not droppable yet**.

- `v8/14.6.202.10.envoy`
  - `requirements.patch` — updates pinned Python package hashes / version set (notably `MarkupSafe`); **envoy-specific**. `envoyproxy/bazel-registry:modules/v8/14.6.202.10.envoy/patches/requirements.patch:1-120`
  - `v8.patch` — large Envoy-specific Bazel integration patch: externalizes deps (`dragonbox/fp16/simdutf`), relaxes warnings, adds `no_debug_info`, disables pointer compression defaults, and adjusts headers/includes; **envoy-specific**. `envoyproxy/bazel-registry:modules/v8/14.6.202.10.envoy/patches/v8.patch:1-200`

- `sq/1.4.0.envoy`
  - `sq-default-crypto-rust.patch` — switches default crypto feature set from nettle to rust crypto and enables experimental/variable-time flags; **envoy-specific**. `envoyproxy/bazel-registry:modules/sq/1.4.0.envoy/patches/sq-default-crypto-rust.patch:1-15`
  - `sq-rustls-network.patch` — makes network crates optional, prefers rustls, and bundles sqlite; **envoy-specific**. `envoyproxy/bazel-registry:modules/sq/1.4.0.envoy/patches/sq-rustls-network.patch:1-54`
  - `overlay/crate-patches/libsqlite3-sys-manifest-dir.patch` — makes build.rs use `CARGO_MANIFEST_DIR` for crate-local files; **envoy-specific**. `envoyproxy/bazel-registry:modules/sq/1.4.0.envoy/overlay/crate-patches/libsqlite3-sys-manifest-dir.patch:1-48`
  - `overlay/crate-patches/sequoia-ipc-hermetic-capnp.patch` — honors `CAPNP` env var in build.rs; **envoy-specific**. `envoyproxy/bazel-registry:modules/sq/1.4.0.envoy/overlay/crate-patches/sequoia-ipc-hermetic-capnp.patch:1-15`
  - `overlay/crate-patches/sequoia-keystore-hermetic-capnp.patch` — same `CAPNP` hermeticity fix for `sequoia-keystore`; **envoy-specific**. `envoyproxy/bazel-registry:modules/sq/1.4.0.envoy/overlay/crate-patches/sequoia-keystore-hermetic-capnp.patch:1-15`
  - `overlay/crate-patches/sequoia-keystore-backend-hermetic-paths.patch` — removes cwd-relative paths and makes include_bytes paths manifest-relative; **envoy-specific**. `envoyproxy/bazel-registry:modules/sq/1.4.0.envoy/overlay/crate-patches/sequoia-keystore-backend-hermetic-paths.patch:1-24`

- `yq.bzl/0.1.1.envoy`
  - `yq.patch` — fixes output-directory calculation for external-workspace/bzlmod execution; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/yq.bzl/0.1.1.envoy/patches/yq.patch:1-28`
  - Upstream shim status: **likely droppable now**. Upstream `bazel-contrib/yq.bzl` ships both `MODULE.bazel` and `BUILD.bazel`, and current `yq/private/yq.bzl` already computes `bin_dir = outs[0].dirname`, covering the local fix. `envoyproxy/bazel-registry:modules/yq.bzl/0.1.1.envoy/source.json:1-11`, https://github.com/bazel-contrib/yq.bzl/blob/main/MODULE.bazel , https://github.com/bazel-contrib/yq.bzl/blob/main/BUILD.bazel , https://github.com/bazel-contrib/yq.bzl/blob/main/yq/private/yq.bzl

- `proxy-wasm-cpp-host/0.0.0-260704-f2db56a.envoy`
  - `proxy-wasm-cpp-host.patch` — replaces external dep labels with local flag/alias-based ones and adds a first-class string build setting for wasm engine selection; **envoy-specific**. `envoyproxy/bazel-registry:modules/proxy-wasm-cpp-host/0.0.0-260704-f2db56a.envoy/patches/proxy-wasm-cpp-host.patch:1-160`

- `toolchains_llvm/1.9.1.envoy`
  - `allow_nonroot.patch` — removes root-only restriction from the llvm extension and deduplicates toolchain registration across modules; **envoy-specific**. `envoyproxy/bazel-registry:modules/toolchains_llvm/1.9.1.envoy/patches/allow_nonroot.patch:1-60`
  - `x_compile.patch` — adds cross-libc++ wiring, `-stdlib=libc++`, and new `cxx_cross_lib` extension tags; **envoy-specific**. `envoyproxy/bazel-registry:modules/toolchains_llvm/1.9.1.envoy/patches/x_compile.patch:1-180`

- `icu/78.2.envoy`
  - `icu.patch` — normalizes `ARFLAGS` handling and cleans minor makefile whitespace; **envoy-specific**. `envoyproxy/bazel-registry:modules/icu/78.2.envoy/patches/icu.patch:1-37`
  - `fix-shebangs.patch` — canonicalizes `#!/bin/sh` shebangs in generated/configure scripts; **envoy-specific**. `envoyproxy/bazel-registry:modules/icu/78.2.envoy/patches/fix-shebangs.patch:1-49`
  - `icu4c_source_common_BUILD.bazel.patch` — broadens Bazel source globs/deps and makes `-ldl` Linux-only; **envoy-specific**. `envoyproxy/bazel-registry:modules/icu/78.2.envoy/patches/icu4c_source_common_BUILD.bazel.patch:1-70`
  - `icu4c_source_common_putil.cpp.patch` — teaches ICU data lookup to use Bazel runfiles under `ICU_DATA_DIR_BAZEL`; **envoy-specific**. `envoyproxy/bazel-registry:modules/icu/78.2.envoy/patches/icu4c_source_common_putil.cpp.patch:1-28`

- `uadk/2.9.envoy`
  - `uadk.patch` — fixes formatting macro spacing, makes fair-lock counters atomic, and narrows a spinlock temp type; **envoy-specific**. `envoyproxy/bazel-registry:modules/uadk/2.9.envoy/patches/uadk.patch:1-41`

- `proto-field-extraction/0.0.0-240710-d5d39f0.envoy`
  - `module_dot_bazel.patch` — adds `MODULE.bazel`; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/proto-field-extraction/0.0.0-240710-d5d39f0.envoy/patches/module_dot_bazel.patch:1-50`
  - `protobuf-v35.patch` — suppresses protobuf-v35 unused-result warnings and explicitly discards return values; **envoy-specific**. `envoyproxy/bazel-registry:modules/proto-field-extraction/0.0.0-240710-d5d39f0.envoy/patches/protobuf-v35.patch:1-140`
  - `ocp.patch` — renames `@ocp//...` deps to `@ocp-diag-core//...`; **envoy-specific**. `envoyproxy/bazel-registry:modules/proto-field-extraction/0.0.0-240710-d5d39f0.envoy/patches/ocp.patch:1-76`
  - Upstream shim status: upstream has `BUILD.bazel` but no root `MODULE.bazel`, so **not droppable yet**.

- `libmaxminddb/1.13.3.envoy`
  - `module_dot_bazel.patch` — adds `MODULE.bazel`; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/libmaxminddb/1.13.3.envoy/patches/module_dot_bazel.patch:1-9`
  - `add_build_file.patch` — adds a Bazel `cc_library` plus generated `maxminddb_config.h`; **bzlmod-shim**. `envoyproxy/bazel-registry:modules/libmaxminddb/1.13.3.envoy/patches/add_build_file.patch:1-43`
  - Upstream shim status: upstream root still lacks native Bazel files, so **not droppable yet**.

- `emsdk/4.0.23.envoy`
  - `emsdk_bzlmod.patch` — reworks the upstream `bazel/` subtree for bzlmod/hermetic toolchains (`dwp_files`, Python toolchain handoff, wrapper-script env fixes, npm section removal); **bzlmod-shim**. `envoyproxy/bazel-registry:modules/emsdk/4.0.23.envoy/patches/emsdk_bzlmod.patch:1-200`
  - Upstream shim status: upstream `emsdk/bazel/` now ships both `BUILD` and `MODULE.bazel`, and `dwp_files` has upstream support, so this looks **partially droppable on bump**, but not obviously fully dropped yet. `envoyproxy/bazel-registry:modules/emsdk/4.0.23.envoy/source.json:1-9`, https://github.com/emscripten-core/emsdk/tree/main/bazel , https://github.com/emscripten-core/emsdk/blob/main/bazel/MODULE.bazel

## 3. Overlay-only modules

## 3. Overlay-only hosted module versions

| Module/version | Overlay adds | Upstream native Bazel now? | BCR compare / classification |
|---|---|---|---|
| `luajit/0.0.0-260126-871db2c.envoy` | `BUILD.bazel` + `MODULE.bazel`. `envoyproxy/bazel-registry:modules/luajit/0.0.0-260126-871db2c.envoy/source.json:5-8` | No root Bazel files in `LuaJIT/LuaJIT`. | BCR has older `luajit` versions (`2.0.5`, `2.1.0-beta3`) only; no same/newer equivalent → **no-bcr-equivalent**. |
| `vectorscan/5.4.11.envoy` | `BUILD.bazel` + `MODULE.bazel`. `envoyproxy/bazel-registry:modules/vectorscan/5.4.11.envoy/source.json:7-10` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `kafka/3.9.2.envoy` | subtree-only `BUILD.bazel` for `clients/.../message`. `envoyproxy/bazel-registry:modules/kafka/3.9.2.envoy/source.json:5-7` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `wasmtime/45.0.2.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/wasmtime/45.0.2.envoy/source.json:5-7` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `go-fips/1.24.12.envoy` | `BUILD.bazel` only, wrapping the Go distro tarball. `envoyproxy/bazel-registry:modules/go-fips/1.24.12.envoy/source.json:5-7` | N/A / no upstream repo-level Bazel metadata in the Go distro tarball. | No BCR module dir found → **no-bcr-equivalent**. |
| `libsxg/0.0.0-210708-beaa393.envoy` | `BUILD.bazel` + `include/libsxg.h` shim header. `envoyproxy/bazel-registry:modules/libsxg/0.0.0-210708-beaa393.envoy/source.json:5-8` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `boringssl-fips/0.20260813.0.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/boringssl-fips/0.20260813.0.envoy/source.json:5-7` | **Yes**; upstream `google/boringssl` now has `MODULE.bazel` + `BUILD.bazel`. | BCR has `boringssl`, not `boringssl-fips`; module-name mismatch → **no-bcr-equivalent**. |
| `boringssl-source/0.20260813.0.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/boringssl-source/0.20260813.0.envoy/source.json:5-7` | **Yes**; same upstream `google/boringssl` Bazel support. | BCR has `boringssl`, not `boringssl-source` → **no-bcr-equivalent**. |
| `prometheus-metrics-model/0.6.2.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/prometheus-metrics-model/0.6.2.envoy/source.json:5-7` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `openssl/3.5.7.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/openssl/3.5.7.envoy/source.json:5-7` | No native upstream Bazel files in `openssl/openssl`. | BCR has newer `openssl/3.5.8.bcr.0` with a much richer overlay/configdata stack: https://github.com/bazelbuild/bazel-central-registry/blob/main/modules/openssl/3.5.8.bcr.0/source.json → **possibly-redundant** on bump. |
| `libevent/2.2.2-alpha.envoy` | root/sample/test/compat `BUILD`s + many generated config headers + `test-config.c`. `envoyproxy/bazel-registry:modules/libevent/2.2.2-alpha.envoy/source.json:5-22` | No. | BCR only has older `2.1.12-stable`; no same/newer match → **no-bcr-equivalent**. |
| `qat-zstd/1.0.0.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/qat-zstd/1.0.0.envoy/source.json:5-7` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `dragonbox/0.0.0-241028-6c7c925.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/dragonbox/0.0.0-241028-6c7c925.envoy/source.json:5-7` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `wuffs/0.4.0-alpha.9.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/wuffs/0.4.0-alpha.9.envoy/source.json:5-7` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `simdutf/8.1.0.envoy` | `BUILD.bazel` only for `singleheader.zip`. `envoyproxy/bazel-registry:modules/simdutf/8.1.0.envoy/source.json:4-6` | No. | BCR has older `7.7.0` only → **no-bcr-equivalent**. |
| `wamr/2.4.4.envoy` | root `BUILD.bazel` + `bazel/BUILD.bazel`. `envoyproxy/bazel-registry:modules/wamr/2.4.4.envoy/source.json:5-8` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `ipp-crypto/2.2.0.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/ipp-crypto/2.2.0.envoy/source.json:5-7` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `lz4/1.10.0.bcr.2.envoy` | `BUILD.bazel` + `MODULE.bazel` + `programs/BUILD.bazel` + `foreign_cc/BUILD.bazel` + `foreign_cc/lz4_archive.bzl`. `envoyproxy/bazel-registry:modules/lz4/1.10.0.bcr.2.envoy/source.json:5-10` | No native upstream Bazel files in `lz4/lz4`. | BCR `1.10.0` already has `BUILD.bazel`/`MODULE.bazel`/`programs/BUILD.bazel`, but **not** the extra `foreign_cc` glue local overlay adds: https://github.com/bazelbuild/bazel-central-registry/blob/main/modules/lz4/1.10.0/source.json → **justified**. |
| `libcircllhist/0.3.2.envoy` | `BUILD.bazel` + `MODULE.bazel`. `envoyproxy/bazel-registry:modules/libcircllhist/0.3.2.envoy/source.json:5-8` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `perfetto/57.2.envoy` | `BUILD.bazel` + `MODULE.bazel`. `envoyproxy/bazel-registry:modules/perfetto/57.2.envoy/source.json:5-7` | **Yes**; upstream `google/perfetto` now ships both `BUILD` and `MODULE.bazel`. | No BCR module dir found → **no-bcr-equivalent**. |
| `ragel/7.0.4-211228-d4577c9.envoy` | `BUILD.bazel` + `MODULE.bazel`. `envoyproxy/bazel-registry:modules/ragel/7.0.4-211228-d4577c9.envoy/source.json:5-8` | No. | BCR has newer `ragel` packaging, but from a different source lineage/shape (`modules/ragel/26.04.../source.json`); local overlay still differs materially → **justified**. |
| `sql-parser/0.0.0-260715-52e5ad1.envoy` | `BUILD.bazel` + `MODULE.bazel`. `envoyproxy/bazel-registry:modules/sql-parser/0.0.0-260715-52e5ad1.envoy/source.json:5-8` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `ocp-diag-core/0.0.0-230505-e965ac0.envoy` | `BUILD.bazel` + `MODULE.bazel` for the `apis/c++` subtree. `envoyproxy/bazel-registry:modules/ocp-diag-core/0.0.0-230505-e965ac0.envoy/source.json:5-8` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `libbpf/1.7.0.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/libbpf/1.7.0.envoy/source.json:4-6` | No. | BCR has exact `1.7.0` with the same one-file overlay shape: https://github.com/bazelbuild/bazel-central-registry/blob/main/modules/libbpf/1.7.0/source.json → **possibly-redundant**. |
| `aws-c-auth-testdata/0.10.4.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/aws-c-auth-testdata/0.10.4.envoy/source.json:5-7` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `fp16/0.0.0-260704-3d2de18.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/fp16/0.0.0-260704-3d2de18.envoy/source.json:5-7` | No. | BCR has only older `0.0.0-20210320-0a92994` → **no-bcr-equivalent**. |
| `vpp-vcl/26.02-260111-85abefb.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/vpp-vcl/26.02-260111-85abefb.envoy/source.json:5-7` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `qatlib/26.02.0.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/qatlib/26.02.0.envoy/source.json:5-7` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `colm/0.14.7-211228-2d8ba76.envoy` | `BUILD.bazel` + `MODULE.bazel`. `envoyproxy/bazel-registry:modules/colm/0.14.7-211228-2d8ba76.envoy/source.json:5-8` | No. | No BCR module dir found → **no-bcr-equivalent**. |
| `msgpack-cxx/7.0.0.envoy` | `BUILD.bazel` only. `envoyproxy/bazel-registry:modules/msgpack-cxx/7.0.0.envoy/source.json:5-7` | No. | No BCR module dir found → **no-bcr-equivalent**. |

### Overlay-only modules where upstream now has native Bazel support
These are the clear “could be droppable on bump” cases:
- `boringssl-fips` / `boringssl-source` → upstream `google/boringssl` now has both `MODULE.bazel` and `BUILD.bazel`.
- `perfetto` → upstream `google/perfetto` now has both `MODULE.bazel` and `BUILD`.
- `yq.bzl` (patch-carrying, not overlay-only) → upstream now has `MODULE.bazel`, `BUILD.bazel`, and the local path-fix logic.

### Gaps / cautions
- For “no-bcr-equivalent” rows, that classification is based on direct BCR directory lookup; many simply have no `modules/<name>` directory at all, while some only have older or differently-shaped packages.
- `emsdk_bzlmod.patch` looks only **partially** upstreamed: native Bazel support exists upstream, and `dwp_files` is present, but I did not verify every shell-wrapper/python-exec hunk landed.

## 4. Internal metadata drift

The table below lists every hosted `MODULE.bazel` edge whose requested version differs from the latest version we currently host for that same module name.

| Hosted module | Declared dep edge | Currently hosted latest | Exact version still hosted here? | Exact version exists in BCR? | MVS / resolution note |
|---|---|---|---|---|---|
| `cpp2sky@0.6.0.envoy` | `protobuf@33.0` | `35.1.bcr.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `envoy@1.40.0-dev.20260904.13144fb.envoy` | `envoy_toolshed@0.4.14.envoy` | `0.4.15.envoy` | no | no | Exact version absent here; works only if another request upgrades it (or fails elsewhere) |
| `envoy@1.40.0-dev.20260904.13144fb.envoy` | `libmaxminddb@1.12.2` | `1.13.3.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `envoy@1.40.0-dev.20260904.13144fb.envoy` | `protoc-gen-validate@1.3.0.envoy` | `1.3.3.envoy` | no | no | Exact version absent here; works only if another request upgrades it (or fails elsewhere) |
| `envoy@1.40.0-dev.20260904.13144fb.envoy` | `proto-converter@0.0.0-20240625-1db7653.envoy` | `0.0.0-20260912-3850764.envoy` | no | no | Exact version absent here; works only if another request upgrades it (or fails elsewhere) |
| `envoy@1.40.0-dev.20260904.13144fb.envoy` | `quiche@0.0.0-260831-5c9cc6b.envoy` | `0.0.0-260922-7f07dc4.envoy` | yes | no | Can resolve to older hosted version still present here |
| `envoy@1.40.0-dev.20260904.13144fb.envoy` | `thrift@0.22.0.envoy` | `0.24.0.envoy` | no | no | Exact version absent here; works only if another request upgrades it (or fails elsewhere) |
| `envoy@1.40.0-dev.20260904.13144fb.envoy` | `vpp-vcl@26.02-dev-85abefb.envoy` | `26.02-260111-85abefb.envoy` | no | no | Exact version absent here; works only if another request upgrades it (or fails elsewhere) |
| `envoy-example-filter-cc@0.2.6.envoy` | `envoy@1.40.0-dev.20260903.6609c01.envoy` | `1.40.0-dev.20260904.13144fb.envoy` | no | no | Exact version absent here; works only if another request upgrades it (or fails elsewhere) |
| `envoy-example-filter-cc@0.2.6.envoy` | `envoy_api@1.40.0-dev.20260903.16b0d47.envoy` | `1.40.0-dev.20260904.13144fb.envoy` | no | no | Exact version absent here; works only if another request upgrades it (or fails elsewhere) |
| `envoy-example-filter-cc@0.2.6.envoy` | `quiche@0.0.0-260831-5c9cc6b.envoy` | `0.0.0-260922-7f07dc4.envoy` | yes | no | Can resolve to older hosted version still present here |
| `envoy-example-wasm-cc@0.2.6.envoy` | `envoy@1.40.0-dev.20260903.6609c01.envoy` | `1.40.0-dev.20260904.13144fb.envoy` | no | no | Exact version absent here; works only if another request upgrades it (or fails elsewhere) |
| `envoy-examples@0.2.6.envoy` | `envoy@1.40.0-dev.20260903.6609c01.envoy` | `1.40.0-dev.20260904.13144fb.envoy` | no | no | Exact version absent here; works only if another request upgrades it (or fails elsewhere) |
| `envoy_api@1.40.0-dev.20260904.13144fb.envoy` | `envoy_toolshed@0.4.14.envoy` | `0.4.15.envoy` | no | no | Exact version absent here; works only if another request upgrades it (or fails elsewhere) |
| `envoy_api@1.40.0-dev.20260904.13144fb.envoy` | `protoc-gen-validate@1.3.0.envoy` | `1.3.3.envoy` | no | no | Exact version absent here; works only if another request upgrades it (or fails elsewhere) |
| `grpc@1.83.0.envoy` | `envoy_api@0.0.0-20251216-6ef568c` | `1.40.0-dev.20260904.13144fb.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `grpc@1.83.0.envoy` | `openssl@3.3.1.bcr.1` | `3.5.7.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `grpc@1.83.0.envoy` | `protobuf@35.1` | `35.1.bcr.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `grpc@1.83.0.envoy` | `protoc-gen-validate@1.2.1.bcr.1` | `1.3.3.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `hermetic-android-toolchains@0.4.0.envoy` | `protobuf@35.1` | `35.1.bcr.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `libevent@2.2.2-alpha.envoy` | `openssl@3.3.1.bcr.1` | `3.5.7.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `librdkafka@2.6.0.envoy` | `lz4@1.9.4` | `1.10.0.bcr.2.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `librdkafka@2.6.0.envoy` | `openssl@3.3.1.bcr.1` | `3.5.7.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `perfetto@57.2.envoy` | `protobuf@28.3` | `35.1.bcr.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `protobuf@35.1.bcr.envoy` | `rules_rust@0.69.0` | `0.69.0.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `proxy-wasm-cpp-host@0.0.0-260704-f2db56a.envoy` | `protobuf@33.2` | `35.1.bcr.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `proxy-wasm-cpp-host@0.0.0-260704-f2db56a.envoy` | `rules_rust@0.68.1` | `0.69.0.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `proxy-wasm-cpp-sdk@0.0.0-250925-e5256b0.envoy` | `protobuf@33.2` | `35.1.bcr.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `proxy-wasm-rust-sdk@0.2.4-251205-5283e57.envoy` | `rules_rust@0.67.0` | `0.69.0.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `skywalking-data-collect-protocol@10.4.0.envoy` | `protobuf@33.0` | `35.1.bcr.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `tcmalloc@0.0.0-250926-12f2552.envoy` | `protobuf@27.5` | `35.1.bcr.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |
| `wasmtime@45.0.2.envoy` | `rules_rust@0.68.1` | `0.69.0.envoy` | no | yes | Can resolve to non-hosted/BCR version if no higher request overrides it |

Key takeaways:
- The most consequential drift is where the stale version **is not hosted here but does exist in BCR** (`grpc` → `openssl@3.3.1.bcr.1`, many modules → older plain `protobuf` versions, `librdkafka` → `lz4@1.9.4`, etc.). Those edges can genuinely resolve to a non-hosted version if nothing else asks for a newer replacement.
- `envoy`, `envoy_api`, and the hosted examples modules also have several stale edges whose exact requested versions are **absent from this registry** (`envoy_toolshed@0.4.14.envoy`, `protoc-gen-validate@1.3.0.envoy`, `envoy@...20260903...`, etc.); those only work today because some other request upgrades them.
- `quiche` is the one prominent case where the stale version is **still hosted here**, so consumers can really stay on the older hosted snapshot until their own pin changes.

## 5. Consumer pin drift

Registry pins verified from consumer `.bazelrc` files:
- Envoy and envoy-website pin `a472b2b59854d52ef584c4651a9e7486fe454090`. Evidence: https://github.com/envoyproxy/envoy/blob/a712680a0725ad8fe401d9bceb1a356efd58d2fc/.bazelrc#L31 and https://github.com/envoyproxy/envoy-website/blob/c03efd7234fe36ef65226e1000038adffa41d7e2/.bazelrc#L11
- toolshed bazel pins `4fc17bd72fe9ef29531bafaefcc2e8ec06ad3568`; toolshed jq pins `e1bd4ce32359abc1c80e934d99eca937ae798308`. Evidence: https://github.com/envoyproxy/toolshed/blob/bc06f06d02c81bd69b4bdf13cc05408030926e10/bazel/.bazelrc#L15 and https://github.com/envoyproxy/toolshed/blob/bc06f06d02c81bd69b4bdf13cc05408030926e10/jq/.bazelrc#L19
- examples pins `e71edce2634e3a733553eff8da3ea9ae3831913a`. Evidence: https://github.com/envoyproxy/examples/blob/fd3f56fce6807b0a434e2ef5c394795ba3f00404/.bazelrc#L4

### envoy / envoy-website (`a472b2b` → `HEAD`, 2 commits)
| Module | Pinned version | HEAD version |
|---|---|---|
| `quiche` | `0.0.0-260831-5c9cc6b.envoy` | `0.0.0-260922-7f07dc4.envoy` |

### toolshed bazel (`4fc17bd` → `HEAD`, 5 commits)
| Module | Pinned version | HEAD version |
|---|---|---|
| `hermetic-android-toolchains` | `0.0.0-20260807-c6a9f20.envoy` | `0.4.0.envoy` |
| `quiche` | `0.0.0-260831-5c9cc6b.envoy` | `0.0.0-260922-7f07dc4.envoy` |

### toolshed jq (`e1bd4ce` → `HEAD`, 22 commits)
| Module | Pinned version | HEAD version |
|---|---|---|
| `boringssl-fips` | `0.20260413.0.envoy` | `0.20260813.0.envoy` |
| `boringssl-source` | `0.20260413.0.envoy` | `0.20260813.0.envoy` |
| `envoy_toolshed` | `0.4.13.envoy` | `0.4.15.envoy` |
| `envoy_toolshed_jq` | `—` | `0.4.15.envoy` |
| `hermetic-android-toolchains` | `0.0.0-20260807-c6a9f20.envoy` | `0.4.0.envoy` |
| `proto-converter` | `0.0.0-20240625-1db7653.envoy` | `0.0.0-20260912-3850764.envoy` |
| `quiche` | `0.0.0-260831-5c9cc6b.envoy` | `0.0.0-260922-7f07dc4.envoy` |
| `toolchains_llvm` | `1.9.0.envoy` | `1.9.1.envoy` |
| `vpp-vcl` | `26.02-dev-85abefb.envoy` | `26.02-260111-85abefb.envoy` |

### examples (`e71edce` → `HEAD`, 43 commits)
| Module | Pinned version | HEAD version |
|---|---|---|
| `boringssl-fips` | `0.20260413.0.envoy` | `0.20260813.0.envoy` |
| `boringssl-source` | `0.20260413.0.envoy` | `0.20260813.0.envoy` |
| `envoy` | `1.40.0-dev.20260902.9efea9b.envoy` | `1.40.0-dev.20260904.13144fb.envoy` |
| `envoy-example-filter-cc` | `—` | `0.2.6.envoy` |
| `envoy-example-wasm-cc` | `0.2.5.envoy` | `0.2.6.envoy` |
| `envoy-examples` | `0.2.5.envoy` | `0.2.6.envoy` |
| `envoy_api` | `1.40.0-dev.20260903.16b0d47.envoy` | `1.40.0-dev.20260904.13144fb.envoy` |
| `envoy_toolshed` | `0.4.13.envoy` | `0.4.15.envoy` |
| `envoy_toolshed_jq` | `—` | `0.4.15.envoy` |
| `hermetic-android-toolchains` | `0.0.0-20260807-c6a9f20.envoy` | `0.4.0.envoy` |
| `proto-converter` | `0.0.0-20240625-1db7653.envoy` | `0.0.0-20260912-3850764.envoy` |
| `protoc-gen-validate` | `1.3.0.envoy` | `1.3.3.envoy` |
| `quiche` | `0.0.0-260824-0140828.envoy` | `0.0.0-260922-7f07dc4.envoy` |
| `sq` | `—` | `1.4.0.envoy` |
| `thrift` | `0.22.0.envoy` | `0.24.0.envoy` |
| `toolchains_llvm` | `1.9.0.envoy` | `1.9.1.envoy` |
| `vpp-vcl` | `26.02-dev-85abefb.envoy` | `26.02-260111-85abefb.envoy` |

## 6. Consumer coverage (brief, re-verified)

- **Transitive usage matters:** `envoy-example-filter-cc` and `envoy-example-wasm-cc` are **not droppable**; hosted `envoy-examples@0.2.6.envoy` depends on both, and `envoy-examples` is consumed by Envoy docs and envoy-website. Evidence: https://github.com/envoyproxy/bazel-registry/blob/61cd20664ece6df60b14cd93623ab6e678038b2c/modules/envoy-examples/0.2.6.envoy/MODULE.bazel#L7-L9 , https://github.com/envoyproxy/envoy/blob/a712680a0725ad8fe401d9bceb1a356efd58d2fc/docs/MODULE.bazel#L7-L9 , https://github.com/envoyproxy/envoy-website/blob/c03efd7234fe36ef65226e1000038adffa41d7e2/MODULE.bazel#L5-L9
- **Single-consumer / narrow-use modules:** `hermetic-android-toolchains` is only Envoy mobile (`dev_dependency` only), and `protoc-gen-jsonschema` is only Envoy API (`dev_dependency` only). Evidence: https://github.com/envoyproxy/envoy/blob/a712680a0725ad8fe401d9bceb1a356efd58d2fc/mobile/MODULE.bazel#L20-L22 and https://github.com/envoyproxy/envoy/blob/a712680a0725ad8fe401d9bceb1a356efd58d2fc/api/MODULE.bazel#L42-L43
- Full per-module direct/transitive map:

| Module | Direct consumer(s) | Transitive consumer(s) | Notes |
|---|---|---|---|
| `aws-c-auth-testdata` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `bazel-compdb` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `boost.headers` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `boringssl-fips` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `boringssl-source` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `cel-cpp` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `colm` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `cpp2sky` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `dd-trace-cpp` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `dragonbox` | — | envoy (api, docs, mobile, root, tests), website, toolshed (bazel), examples (filter-cc, root, wasm-cc) | — |
| `elfutils` | — | envoy (docs, mobile, root), website, examples (filter-cc, root, wasm-cc) | — |
| `emsdk` | envoy | envoy (docs, mobile, tests), website, examples (filter-cc, root, wasm-cc) | — |
| `envoy` | envoy (mobile), examples (filter-cc, root, wasm-cc) | envoy (docs), website | — |
| `envoy-example-filter-cc` | examples | envoy (docs), website | — |
| `envoy-example-wasm-cc` | examples | envoy (docs), website | — |
| `envoy-examples` | envoy (docs), website | — | — |
| `envoy_api` | envoy (docs, mobile, root, tests), examples (filter-cc) | envoy (api), website, examples (root, wasm-cc) | — |
| `envoy_toolshed` | envoy (api, docs, mobile, root, tests), website | examples (filter-cc, root, wasm-cc) | — |
| `envoy_toolshed_jq` | toolshed (bazel) | envoy (api, docs, mobile, root, tests), website, examples (filter-cc, root, wasm-cc) | — |
| `fp16` | — | envoy (api, docs, mobile, root, tests), website, toolshed (bazel), examples (filter-cc, root, wasm-cc) | — |
| `go-fips` | — | envoy (docs, mobile, root), website, examples (filter-cc, root, wasm-cc) | — |
| `googleurl` | envoy (docs, mobile, root, tests), website, examples (filter-cc) | examples (root, wasm-cc) | — |
| `grpc` | envoy (api, docs, mobile, root), website | envoy (tests), examples (filter-cc, root, wasm-cc) | — |
| `grpc-httpjson-transcoding` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `hermetic-android-toolchains` | envoy (mobile) | — | dev-only; single-consumer |
| `hessian2-codec` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `hyperscan` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `icu` | envoy | envoy (api, docs, mobile, tests), website, toolshed (bazel), examples (filter-cc, root, wasm-cc) | — |
| `ipp-crypto` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `kafka` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `libbpf` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `libcircllhist` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `libevent` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `libmaxminddb` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `librdkafka` | envoy (docs, mobile, root), website | examples (filter-cc, root, wasm-cc) | — |
| `libsxg` | envoy (docs, mobile, root, tests), website | examples (filter-cc, root, wasm-cc) | — |
| `liburing` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `luajit` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `lz4` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `msgpack-cxx` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `nghttp2` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `ocp-diag-core` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `openssl` | envoy (mobile, root) | envoy (api, docs, tests), website, examples (filter-cc, root, wasm-cc) | — |
| `perfetto` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `prometheus-metrics-model` | envoy (api, root) | envoy (docs, mobile, tests), website, examples (filter-cc, root, wasm-cc) | — |
| `proto-converter` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `proto-field-extraction` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `proto-processing` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `protobuf` | envoy (api, docs, mobile, root, tests), website, toolshed (bazel), examples (filter-cc) | examples (root, wasm-cc) | — |
| `protoc-gen-jsonschema` | envoy (api) | — | dev-only; single-consumer |
| `protoc-gen-validate` | envoy (api, docs, mobile, root), website, examples (filter-cc) | envoy (tests), examples (root, wasm-cc) | — |
| `proxy-wasm-cpp-host` | envoy (docs, mobile, root, tests), website, examples (filter-cc) | examples (root, wasm-cc) | — |
| `proxy-wasm-cpp-sdk` | envoy | envoy (docs, mobile, tests), website, examples (filter-cc, root, wasm-cc) | — |
| `proxy-wasm-rust-sdk` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `qat-zstd` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `qatlib` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `qatzip` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `quiche` | envoy (docs, mobile, root, tests), website, examples (filter-cc) | examples (root, wasm-cc) | — |
| `ragel` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `rules_rust` | envoy (docs, mobile, root), website, toolshed (bazel), examples (filter-cc) | envoy (api, tests), examples (root, wasm-cc) | — |
| `simdutf` | — | envoy (api, docs, mobile, root, tests), website, toolshed (bazel), examples (filter-cc, root, wasm-cc) | — |
| `skywalking-data-collect-protocol` | — | envoy (docs, mobile, root), website, examples (filter-cc, root, wasm-cc) | — |
| `sq` | envoy, toolshed (bazel) | envoy (api, docs, mobile, tests), website, examples (filter-cc, root, wasm-cc) | — |
| `sql-parser` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `tcmalloc` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `thrift` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `toolchains_llvm` | envoy (docs, mobile, root, tests), website, toolshed (bazel), examples (filter-cc, root, wasm-cc) | envoy (api, tests), toolshed (bazel), examples (filter-cc, root, wasm-cc) | — |
| `uadk` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `v8` | envoy, toolshed (bazel) | envoy (api, docs, mobile, tests), website, examples (filter-cc, root, wasm-cc) | — |
| `vectorscan` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `vpp-vcl` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `wamr` | envoy | envoy (docs, mobile, tests), website, examples (filter-cc, root, wasm-cc) | — |
| `wasmtime` | envoy | envoy (docs, mobile, tests), website, examples (filter-cc, root, wasm-cc) | — |
| `wuffs` | envoy | envoy (docs, mobile), website, examples (filter-cc, root, wasm-cc) | — |
| `yq.bzl` | envoy (api, root) | envoy (docs, mobile, tests), website, examples (filter-cc, root, wasm-cc) | — |
| `zlib-ng` | envoy (docs, mobile, root), website | examples (filter-cc, root, wasm-cc) | — |

## 7. Notes / caveats

- Two special cases needed non-API fallback logic rather than GitHub Releases API: `sq` (GitLab tags page; latest visible tag `v1.4.1`) and `vectorscan` (slash-namespaced tags / release pages). Those are now classified, not left `UNKNOWN`.
- Some commit-pinned repos returned unauthenticated GitHub API `403` for repository metadata, so their “latest commit” rows use a combination of `git ls-remote --symref`, commit `.patch` pages for dates, and compare URLs for evidence instead of API JSON.
- No module directories under `modules/` were modified for this report.
