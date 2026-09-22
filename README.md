# bazel-registry

Envoy's Bazel module registry.

It holds bzlmod modules used by [Envoy](https://github.com/envoyproxy/envoy) and related Envoy projects when they are not available in the [Bazel Central Registry](https://registry.bazel.build/) or require Envoy-specific patches.

All versions in this registry carry an `.envoy` suffix to distinguish them from BCR versions.

## Usage

Add the registry to your `.bazelrc`, ahead of the BCR:

```
common --registry=https://raw.githubusercontent.com/envoyproxy/bazel-registry/main
common --registry=https://bcr.bazel.build
```

Then depend on modules as normal, for example:

```starlark
bazel_dep(name = "nghttp2", version = "1.66.0.envoy")
```

## Layout

Follows the standard Bazel registry layout: `bazel_registry.json` at the root and one directory per module under `modules/`, each containing `metadata.json` and one directory per version with `MODULE.bazel` and `source.json` plus optional `patches/` and `overlay/`.
