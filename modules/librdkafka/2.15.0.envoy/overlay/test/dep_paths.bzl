"""Writes resolved C/C++ library paths for configured librdkafka deps."""

def _dep_paths_impl(ctx):
    paths = []
    for dep in [ctx.attr.rdkafka, ctx.attr.crypto, ctx.attr.ssl, ctx.attr.zlib]:
        cc_info = dep[CcInfo]
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

    out = ctx.actions.declare_file(ctx.label.name + ".txt")
    ctx.actions.write(out, "\n".join(sorted(paths)) + "\n")
    return DefaultInfo(files = depset([out]))

dep_paths = rule(
    implementation = _dep_paths_impl,
    attrs = {
        "crypto": attr.label(providers = [CcInfo]),
        "rdkafka": attr.label(providers = [CcInfo]),
        "ssl": attr.label(providers = [CcInfo]),
        "zlib": attr.label(providers = [CcInfo]),
    },
)
