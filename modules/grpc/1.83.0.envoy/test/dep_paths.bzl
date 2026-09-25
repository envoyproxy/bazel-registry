load("@rules_cc//cc/common:cc_info.bzl", "CcInfo")

"""Asserts resolved C/C++ library deps for the extension-configured grpc test module."""


def _library_paths(target):
    paths = []
    cc_info = target[CcInfo]
    for linker_input in cc_info.linking_context.linker_inputs.to_list():
        for library in linker_input.libraries:
            for file in [
                library.static_library,
                library.pic_static_library,
                library.dynamic_library,
                library.interface_library,
            ]:
                if file:
                    paths.append(file.path)
    return depset(paths)


def _dep_paths_impl(ctx):
    actual_targets = [
        ("crypto", ctx.attr.crypto, ctx.attr.expected_crypto),
        ("ssl", ctx.attr.ssl, ctx.attr.expected_ssl),
        ("zlib", ctx.attr.zlib, ctx.attr.expected_zlib),
    ]
    results = []
    for name, actual, expected in actual_targets:
        actual_paths = {path: True for path in _library_paths(actual).to_list()}
        expected_paths = {path: True for path in _library_paths(expected).to_list()}
        if actual_paths != expected_paths:
            fail("Configured %s alias does not resolve to the expected target" % name)
        results.append("%s=%s" % (name, expected.label))

    out = ctx.actions.declare_file(ctx.label.name + ".txt")
    ctx.actions.write(out, "\n".join(results) + "\n")
    return DefaultInfo(files = depset([out]))


dep_paths = rule(
    implementation = _dep_paths_impl,
    attrs = {
        "crypto": attr.label(providers = [CcInfo]),
        "expected_crypto": attr.label(providers = [CcInfo]),
        "expected_ssl": attr.label(providers = [CcInfo]),
        "expected_zlib": attr.label(providers = [CcInfo]),
        "ssl": attr.label(providers = [CcInfo]),
        "zlib": attr.label(providers = [CcInfo]),
    },
)
