# librdkafka 2.15.0.envoy

This module is copied from BCR `librdkafka@2.15.0` with two deliberate changes only:

- a small module extension (`overlay/extensions.bzl`) that lets consumers redirect the TLS and zlib deps in `MODULE.bazel`;
- a matching `overlay/BUILD.bazel` change so `:rdkafka` depends on `@librdkafka_deps//:{ssl,crypto,zlib}` instead of hardcoded `@openssl` / `@zlib` targets.

All `bool_flag`s, generated config, tests, patches, and upstream dependency declarations remain aligned with BCR. `openssl` and `zlib` stay in `MODULE.bazel` so the default configuration still resolves without any extension use.

## Configure usage

```starlark
librdkafka = use_extension("@librdkafka//:extensions.bzl", "librdkafka")
librdkafka.configure(
    ssl = "@envoy//bazel:ssl",
    crypto = "@envoy//bazel:crypto",
    zlib = "@envoy//bazel:zlib",
)
```

Resolution rules:

- a root module `librdkafka.configure(...)` tag wins for each attribute it sets;
- otherwise non-root modules are merged per attribute, where an unset attr means “don't care”;
- if two non-root modules set the same attribute to different labels, module resolution fails with a conflict naming both modules.

This is the intended pattern for Envoy's `MODULE.bazel`, where Envoy may not be the root module but still needs its TLS/zlib configuration to flow through consumers such as envoy-mobile, envoy-docs, Istio, or Nighthawk.

This module is also the reference pattern for replacing `.bazelrc` `label_flag` injection in other Envoy registry modules such as grpc (`third_party:ssl_lib` / `crypto_lib` / `zlib_lib`), protobuf (`//:zlib`), and later quiche, proxy-wasm-cpp-host, libsxg, qatzip, libbpf, and elfutils.

The presubmit keeps the upstream default and no-feature coverage, and adds an extension-configured path that redirects librdkafka to `@boringssl` and `@zlib-ng`.

That extension task builds `@librdkafka//:librdkafka`, `@librdkafka//:librdkafka_cpp`, and a lightweight `//:extension_deps_test` shell test that uses a tiny Starlark helper to record the resolved C/C++ library paths for `@librdkafka//:rdkafka` and the configured `@librdkafka_deps` aliases, then asserts that those paths come from the expected `librdkafka`, `boringssl`, and `zlib-ng` repositories. Full standalone librdkafka test binaries are intentionally not enabled on this path yet: linking them against the current boringssl-backed configuration exposes upstream unresolved TLS symbols (`SSL_CTX_use_cert_and_key`, `RAND_priv_bytes`). Envoy is expected to validate the integrated boringssl/zlib-ng configuration first before proposing this pattern upstream to BCR.
