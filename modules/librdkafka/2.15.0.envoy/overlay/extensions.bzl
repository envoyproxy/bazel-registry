"""Module extension for configuring librdkafka TLS and zlib deps."""

def _librdkafka_deps_repo_impl(repo_ctx):
    """Writes aliases for the resolved librdkafka dependency labels."""
    repo_ctx.file(
        "BUILD.bazel",
        """alias(
    name = \"crypto\",
    actual = \"{crypto}\",
    visibility = [\"//visibility:public\"],
)

alias(
    name = \"ssl\",
    actual = \"{ssl}\",
    visibility = [\"//visibility:public\"],
)

alias(
    name = \"zlib\",
    actual = \"{zlib}\",
    visibility = [\"//visibility:public\"],
)
""".format(
            crypto = str(repo_ctx.attr.crypto),
            ssl = str(repo_ctx.attr.ssl),
            zlib = str(repo_ctx.attr.zlib),
        ),
    )

_librdkafka_deps_repo = repository_rule(
    implementation = _librdkafka_deps_repo_impl,
    attrs = {
        "crypto": attr.label(doc = "Label to alias as :crypto."),
        "ssl": attr.label(doc = "Label to alias as :ssl."),
        "zlib": attr.label(doc = "Label to alias as :zlib."),
    },
)

def _value(tag, name):
    return getattr(tag, name, None)

def _module_id(mod):
    if mod.version:
        return "%s@%s" % (mod.name, mod.version)
    return mod.name

def _pick(label_name, values):
    """Chooses one label value or fails if multiple modules disagree."""
    chosen = None
    chosen_module = None
    for module_name, label in values:
        if label == None:
            continue
        if chosen == None:
            chosen = label
            chosen_module = module_name
            continue
        if chosen != label:
            fail(
                "Conflicting librdkafka.configure(%s=...) labels from modules %s (%s) and %s (%s)." % (
                    label_name,
                    chosen_module,
                    chosen,
                    module_name,
                    label,
                ),
            )
    return chosen

def _librdkafka_impl(module_ctx):
    """Resolves TLS/zlib labels and exposes them through @librdkafka_deps."""
    root = []
    non_root = []
    for mod in module_ctx.modules:
        for tag in mod.tags.configure:
            values = struct(
                module_name = _module_id(mod),
                ssl = _value(tag, "ssl"),
                crypto = _value(tag, "crypto"),
                zlib = _value(tag, "zlib"),
            )
            if mod.is_root:
                root.append(values)
            else:
                non_root.append(values)

    root_ssl = _pick("ssl", [(entry.module_name, entry.ssl) for entry in root])
    root_crypto = _pick("crypto", [(entry.module_name, entry.crypto) for entry in root])
    root_zlib = _pick("zlib", [(entry.module_name, entry.zlib) for entry in root])

    ssl = root_ssl if root_ssl != None else _pick(
        "ssl",
        [(entry.module_name, entry.ssl) for entry in non_root],
    )
    crypto = root_crypto if root_crypto != None else _pick(
        "crypto",
        [(entry.module_name, entry.crypto) for entry in non_root],
    )
    zlib = root_zlib if root_zlib != None else _pick(
        "zlib",
        [(entry.module_name, entry.zlib) for entry in non_root],
    )

    if ssl == None:
        ssl = Label("@openssl//:ssl")
    if crypto == None:
        crypto = Label("@openssl//:crypto")
    if zlib == None:
        zlib = Label("@zlib//:zlib")

    _librdkafka_deps_repo(
        name = "librdkafka_deps",
        ssl = ssl,
        crypto = crypto,
        zlib = zlib,
    )

    if hasattr(module_ctx, "extension_metadata"):
        return module_ctx.extension_metadata()
    return None

configure = tag_class(
    attrs = {
        "crypto": attr.label(doc = "Optional label to use for librdkafka's crypto dependency."),
        "ssl": attr.label(doc = "Optional label to use for librdkafka's TLS/SSL dependency."),
        "zlib": attr.label(doc = "Optional label to use for librdkafka's zlib dependency."),
    },
    doc = "Configures the TLS and zlib labels used by the librdkafka overlay.",
)

librdkafka = module_extension(
    implementation = _librdkafka_impl,
    tag_classes = {"configure": configure},
    doc = "Creates @librdkafka_deps aliases for librdkafka's configurable deps.",
)
