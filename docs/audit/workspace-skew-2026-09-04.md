# WORKSPACE ↔ registry version skew audit

envoy @ 13144fbbb3800f1a41c45d17dc9de44978b567b1 (2026-09-04)
registry @ bed06c78cb1ea901164f4d248c3e5167f720e068

## Summary
| status | count |
|---|---|
| hash-mismatch | 0 |
| match | 49 |
| registry-ahead | 1 |
| registry-behind | 3 |
| registry-only | 11 |
| unmapped | 2 |
| unordered | 19 |
| workspace-only | 48 |

## registry-behind  ← fix these
| module | WORKSPACE | registry | delta | in root MODULE.bazel? |
|---|---|---|---|---|
| protoc-gen-validate | v1.3.3 | v1.3.0 | version bump | yes |
| quiche | 5c9cc6b (2026-08-31) | 0140828 (2026-08-24) | 21 commits | yes |
| thrift | v0.24.0 | v0.22.0 | version bump | yes |

## registry-ahead  ← WORKSPACE should catch up, or registry was bumped deliberately
| module | WORKSPACE | registry | delta | in root MODULE.bazel? |
|---|---|---|---|---|
| emsdk | 4.0.6 | c0bb220 | module version 4.0.23.envoy vs workspace 4.0.6 | yes |

## hash-mismatch  ← investigate immediately
_none_

## unordered
| module | WORKSPACE | registry | delta | in root MODULE.bazel? |
|---|---|---|---|---|
| boringssl-fips | 0.20260413.0 | 0.20260413.0 | same version, different url | yes |
| cel-cpp | v0.14.0 | 439003a | same version (0.14.0), registry pins a commit | yes |
| dragonbox | 6c7c925 | 6c7c925 | same commit, different url | no |
| flatbuffers | v25.12.19 | v25.12.19 | same version, different url | yes |
| icu | release-78.2 | release-78.2 | same version, different url | yes |
| libprotobuf-mutator | v1.5 | v1.5 | same version, different url | yes |
| librdkafka | v2.6.0 | v2.6.0 | same version, different url | yes |
| liburing | liburing-2.15 | liburing-2.15 | same version, different url | yes |
| luajit | 871db2c | 871db2c | same commit (registry url uses a short sha) | yes |
| lz4 | v1.10.0 | v1.10.0 | same version, different url | yes |
| perfetto | v57.2 | v57.2 | same version, different url | yes |
| proxy-wasm-rust-sdk | v0.2.4 | 5283e57 | same version (0.2.4), registry pins a commit | yes |
| qatzip | v1.3.2 | v1.3.2 | same version, different url | yes |
| su-exec | v0.3 | v0.3 | same version, different url | yes |
| vectorscan | vectorscan/5.4.11 | vectorscan/5.4.11 | same version, different url | yes |
| wamr | WAMR-2.4.4 | WAMR-2.4.4 | same version, different url | yes |
| wasmtime | v45.0.2 | v45.0.2 | same version, different url | yes |
| zipkin-api | 1.0.0 | 1.0.0 | same version, different url | yes |
| zlib-ng | 2.3.2 | 2.3.2 | same version, different url | yes |

## registry-only
| module | registry version | source | used by |
|---|---|---|---|
| aws-lc-fips | 1.66.2.envoy | envoy-patched upstream | - |
| boost.headers | 1.89.0.envoy | envoy-patched upstream | root |
| boringssl-source | 0.20260413.0.envoy | envoy-patched upstream (same upstream as WORKSPACE `boringssl`) | root |
| envoy | 1.40.0-dev.20260904.13144fb.envoy | envoy-owned | docs, mobile |
| envoy-example-filter-cc | 0.2.6.envoy | envoy-owned | - |
| envoy-example-wasm-cc | 0.2.6.envoy | envoy-owned | - |
| envoy-examples | 0.2.6.envoy | envoy-owned | docs |
| envoy_api | 1.40.0-dev.20260904.13144fb.envoy | envoy-owned | root, docs, mobile |
| go-fips | 1.24.12.envoy | envoy-patched upstream | - |
| hermetic-android-toolchains | 0.0.0-20260807-c6a9f20.envoy | envoy-patched upstream | mobile |
| rules_xcodeproj | 1.2.0.envoy | envoy-patched upstream | mobile |

## workspace-only
| WORKSPACE name | version | in BCR? | note |
|---|---|---|---|
| abseil_cpp | 20260107.1 | abseil-cpp | BCR module, not mirrored here; root spec |
| aspect_bazel_lib | 2.21.2 | aspect_bazel_lib | BCR module, not mirrored here; root spec |
| bazel_features | 1.51.0 | bazel_features | BCR module, not mirrored here; root spec |
| bazel_skylib | 1.9.2 | bazel_skylib | BCR module, not mirrored here; api spec |
| benchmark | 1.9.5 | google_benchmark | BCR module, not mirrored here; root spec |
| boost | 1.89.0 | boost | BCR module, not mirrored here; root spec |
| brotli | 1.2.0 | brotli | BCR module, not mirrored here; root spec |
| buildtools | 8.5.1 | no | no registry module and not in BCR; root spec |
| c_ares | 1.34.8 | c-ares | BCR module, not mirrored here; root spec |
| cel_spec | 0.25.2 | cel-spec | BCR module, not mirrored here; root spec |
| dev_cel | 0.25.1 | cel-spec | BCR module, not mirrored here; api spec |
| fast_float | 7.0.0 | fast_float | BCR module, not mirrored here; root spec |
| fips_cmake_linux_aarch64 | 4.4.0 | no | no registry module and not in BCR; root spec |
| fips_cmake_linux_x86_64 | 4.4.0 | no | no registry module and not in BCR; root spec |
| fips_ninja | 1.13.2 | ninja | BCR module, not mirrored here; root spec |
| fmt | 12.2.0 | fmt | BCR module, not mirrored here; root spec |
| gazelle | 0.47.0 | gazelle | BCR module, not mirrored here; root spec |
| googleapis | fd52b5754b2b268bc3a22a10f29844f206abb327 | googleapis | BCR module, not mirrored here; api spec |
| googletest | 1.17.0 | googletest | BCR module, not mirrored here; root spec |
| gperftools | 2.18.1 | gperftools | BCR module, not mirrored here; root spec |
| highway | 1.2.0 | highway | BCR module, not mirrored here; root spec |
| jemalloc | 5.3.0 | jemalloc | BCR module, not mirrored here; root spec |
| libpfm | 4.11.0 | libpfm | BCR module, not mirrored here; root spec |
| nlohmann_json | 3.12.0 | nlohmann_json | BCR module, not mirrored here; root spec |
| numactl | 2.0.19 | numactl | BCR module, not mirrored here; root spec |
| opentelemetry_proto | 1.11.0 | opentelemetry-proto | BCR module, not mirrored here; api spec |
| platforms | 1.1.0 | platforms | BCR module, not mirrored here; root spec |
| re2 | 2024-07-02 | re2 | BCR module, not mirrored here; root spec |
| rules_buf | 0.5.4 | rules_buf | BCR module, not mirrored here; api spec |
| rules_cc | 0.2.22 | rules_cc | BCR module, not mirrored here; root spec |
| rules_foreign_cc | 0.15.1 | rules_foreign_cc | BCR module, not mirrored here; root spec |
| rules_fuzzing | 0.8.0 | rules_fuzzing | BCR module, not mirrored here; root spec |
| rules_go | 0.61.1 | rules_go | BCR module, not mirrored here; root spec |
| rules_java | 9.7.0 | rules_java | BCR module, not mirrored here; root spec |
| rules_jvm_external | 6.10 | rules_jvm_external | BCR module, not mirrored here; api spec |
| rules_license | 1.0.0 | rules_license | BCR module, not mirrored here; root spec |
| rules_pkg | 1.2.0 | rules_pkg | BCR module, not mirrored here; root spec |
| rules_proto | 7.1.0 | rules_proto | BCR module, not mirrored here; api spec |
| rules_proto_grpc | 4.6.0 | rules_proto_grpc | BCR module, not mirrored here; root spec |
| rules_python | 2.2.0 | rules_python | BCR module, not mirrored here; root spec |
| rules_ruby | 37cf5900d0b0e44fa379c0ea3f5fcee0035d77ca | rules_ruby | BCR module, not mirrored here; root spec |
| rules_shell | 0.8.0 | rules_shell | BCR module, not mirrored here; root spec |
| shellcheck | 0.4.0 | rules_shellcheck | BCR module, not mirrored here; root spec |
| spdlog | 1.17.0 | spdlog | BCR module, not mirrored here; root spec |
| tclap | 1.2.5 | tclap | BCR module, not mirrored here; root spec |
| xxhash | 0.8.3 | xxhash | BCR module, not mirrored here; root spec |
| yaml_cpp | 0.9.0 | yaml-cpp | BCR module, not mirrored here; root spec |
| zstd | 1.5.7 | zstd | BCR module, not mirrored here; root spec |

## unmapped
| WORKSPACE name | version | spec | url |
|---|---|---|---|
| fips_go_linux_amd64 | 1.26.3 | root spec | https://dl.google.com/go/go1.26.3.linux-amd64.tar.gz |
| fips_go_linux_arm64 | 1.26.3 | root spec | https://dl.google.com/go/go1.26.3.linux-arm64.tar.gz |

## match
<details>

| module | WORKSPACE version | registry version |
|---|---|---|
| aws-c-auth-testdata | 0.10.4 | 0.10.4.envoy |
| bazel-compdb | 40864791135333e1446a04553b63cbe744d358d0 | 0.0.0-20220906-4086479.envoy |
| colm | 2d8ba76ddaf6634f285d0a81ee42d5ee77d084cf | 0.14.7-211228-2d8ba76.envoy |
| cpp2sky | 0.6.0 | 0.6.0.envoy |
| dd-trace-cpp | 2.1.1 | 2.1.1.envoy |
| elfutils | 0.195 | 0.195.envoy |
| envoy_toolshed | 0.4.13 | 0.4.13.envoy |
| fp16 | 3d2de1816307bac63c16a297e8c4dc501b4076df | 0.0.0-260704-3d2de18.envoy |
| googleurl | dd4080fec0b443296c0ed0036e1e776df8813aa7 | 0.0.0-221103-dd4080f.envoy |
| grpc | 1.83.0 | 1.83.0.envoy |
| grpc-httpjson-transcoding | a6e226f9a2e656a973df3ad48f0ee5efacce1a28 | 0.0.0-20250507-a6e226f.envoy |
| hessian2-codec | 6f5a64770f0374a761eece13c8863b80dc5adcd8 | 0.0.0-250114-6f5a647.envoy |
| hyperscan | 5.4.2 | 5.4.2.envoy |
| ipp-crypto | 2.2.0 | 2.2.0.envoy |
| kafka | 3.9.2 | 3.9.2.envoy |
| libbpf | 1.7.0 | 1.7.0.envoy |
| libcircllhist | 0.3.2 | 0.3.2.envoy |
| libevent | release-2.2.2-alpha | 2.2.2-alpha.envoy |
| libmaxminddb | 1.13.3 | 1.13.3.envoy |
| libsxg | beaa3939b76f8644f6833267e9f2462760838f18 | 0.0.0-210708-beaa393.envoy |
| msgpack-cxx | 7.0.0 | 7.0.0.envoy |
| nghttp2 | 1.66.0 | 1.66.0.envoy |
| ocp-diag-core | e965ac0ac6db6686169678e2a6c77ede904fa82c | 0.0.0-230505-e965ac0.envoy |
| openssl | 3.5.7 | 3.5.7.envoy |
| opentelemetry-cpp | 1.28.0 | 1.28.0.envoy |
| prometheus-metrics-model | 0.6.2 | 0.6.2.envoy |
| proto-converter | 1db76535b86b80aa97489a1edcc7009e18b67ab7 | 0.0.0-20240625-1db7653.envoy |
| proto-field-extraction | d5d39f0373e9b6691c32c85929838b1006bcb3fb | 0.0.0-240710-d5d39f0.envoy |
| proto-processing | 279353cfab372ac7f268ae529df29c4d546ca18d | 0.0.0-250110-279353c.envoy |
| protobuf | 35.1 | 35.1.bcr.envoy |
| protoc-gen-jsonschema | 7680e4998426e62b6896995ff73d4d91cc5fb13c | 0.0.0-20230530-7680e49.envoy |
| proxy-wasm-cpp-host | f2db56af443571e92a31c0b877106d9ea96e19ef | 0.0.0-260704-f2db56a.envoy |
| proxy-wasm-cpp-sdk | e5256b0c5463ea9961965ad5de3e379e00486640 | 0.0.0-250925-e5256b0.envoy |
| qat-zstd | 1.0.0 | 1.0.0.envoy |
| qatlib | 26.02.0 | 26.02.0.envoy |
| ragel | d4577c924451b331c73c8ed0af04f6efd35ac0b4 | 7.0.4-211228-d4577c9.envoy |
| rules_apple | 3.20.1 | 3.20.1.envoy |
| rules_rust | 0.69.0 | 0.69.0.envoy |
| simdutf | 8.1.0 | 8.1.0.envoy |
| skywalking-data-collect-protocol | 10.4.0 | 10.4.0.envoy |
| sql-parser | 52e5ad1f4fbb21301fcee7f9d18eef7e6ae6ab3e | 0.0.0-260715-52e5ad1.envoy |
| tcmalloc | 12f255231938d30493186b0a037feedd70f5a1c1 | 0.0.0-250926-12f2552.envoy |
| toolchains_llvm | 1.9.0 | 1.9.0.envoy |
| uadk | 2.9 | 2.9.envoy |
| v8 | 14.6.202.10 | 14.6.202.10.envoy |
| vpp-vcl | 85abefb55ee931fa4e45c0b6a9fc8c43118651b3 | 26.02-dev-85abefb.envoy |
| wuffs | 0.4.0-alpha.9 | 0.4.0-alpha.9.envoy |
| xds | 8bfbf64dc13ee1a570be4fbdcfccbdd8532463f0 | 0.0.1-20251110-8bfbf64.envoy |
| yq.bzl | 0.1.1 | 0.1.1.envoy |

</details>

## Method
Generated by `docs/audit/workspace_skew.py --envoy-sha 13144fbbb3800f1a41c45d17dc9de44978b567b1`.
WORKSPACE entries come from `bazel/repository_locations.bzl` + `api/bazel/repository_locations.bzl`
(parsed with `ast`, `{version}` resolved in urls); registry entries are the last
`versions` entry of each `modules/*/metadata.json` plus its `source.json`.
Mapping is by upstream `github.com/<org>/<repo>` first, then normalised name; `match` means
identical url *and* WORKSPACE sha256 == registry SRI integrity. Git-SHA skew is measured with
the GitHub compare API (cap 30 calls, 2 used);
`bazel_dep` usage is read from envoy's root/api/docs/mobile/examples `MODULE.bazel`.

