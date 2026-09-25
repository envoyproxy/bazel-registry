"""Asserts resolved C/C++ library deps for the extension-configured test module."""

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
    alias_crypto = _library_paths(ctx.attr.crypto)
    alias_ssl = _library_paths(ctx.attr.ssl)
    alias_zlib = _library_paths(ctx.attr.zlib)
    expected_crypto = _library_paths(ctx.attr.expected_crypto)
    expected_ssl = _library_paths(ctx.attr.expected_ssl)
    expected_zlib = _library_paths(ctx.attr.expected_zlib)
    librdkafka = _library_paths(ctx.attr.rdkafka)

    if alias_crypto.to_list() != expected_crypto.to_list():
        fail("Configured crypto alias does not resolve to the expected target")
    if alias_ssl.to_list() != expected_ssl.to_list():
        fail("Configured ssl alias does not resolve to the expected target")
    if alias_zlib.to_list() != expected_zlib.to_list():
        fail("Configured zlib alias does not resolve to the expected target")

    librdkafka_paths = {path: True for path in librdkafka.to_list()}
    for label, expected in [
        (str(ctx.attr.expected_crypto.label), expected_crypto),
        (str(ctx.attr.expected_ssl.label), expected_ssl),
        (str(ctx.attr.expected_zlib.label), expected_zlib),
    ]:
        found = False
        for path in expected.to_list():
            if path in librdkafka_paths:
                found = True
                break
        if not found:
            fail("@librdkafka//:librdkafka is missing link inputs from %s" % label)

    out = ctx.actions.declare_file(ctx.label.name + ".txt")
    ctx.actions.write(
        out,
        "\n".join([
            "crypto=%s" % ctx.attr.expected_crypto.label,
            "ssl=%s" % ctx.attr.expected_ssl.label,
            "zlib=%s" % ctx.attr.expected_zlib.label,
            "librdkafka=%s" % ctx.attr.rdkafka.label,
        ]) + "\n",
    )
    return DefaultInfo(files = depset([out]))

dep_paths = rule(
    implementation = _dep_paths_impl,
    attrs = {
        "crypto": attr.label(providers = [CcInfo]),
        "expected_crypto": attr.label(providers = [CcInfo]),
        "expected_ssl": attr.label(providers = [CcInfo]),
        "expected_zlib": attr.label(providers = [CcInfo]),
        "rdkafka": attr.label(providers = [CcInfo]),
        "ssl": attr.label(providers = [CcInfo]),
        "zlib": attr.label(providers = [CcInfo]),
    },
)
