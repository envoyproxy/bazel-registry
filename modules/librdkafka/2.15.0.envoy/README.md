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

The presubmit keeps the upstream default and no-feature builds, and adds an extension-configured build that redirects librdkafka to `@boringssl` and `@zlib-ng`.
