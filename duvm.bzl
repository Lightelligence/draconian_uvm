"""DUVM"""

def duvm_test(name, srcs, ignored = [], waivers = [], tags = []):
    """Run draconian_uvm on source files."""
    ignore_config = waivers

    args = [
        "--rc $(location @draconian_uvm//:duvm/lw_rc.py)",
        " ".join(["$(locations {})".format(s) for s in srcs]),
    ]

    data = srcs + ["@draconian_uvm//:duvm/lw_rc.py", "@draconian_uvm//:lib"] + ignore_config

    for igr in ignored:
        args.append("--igr {}".format(igr))
    for igrc in ignore_config:
        args.append("--igrc $(location {})".format(igrc))

    native.py_test(
        name = name,
        srcs = ["@lintworks//:main"],
        data = data,
        args = args,
        main = "@lintworks//:main.py",  # Seems silly that this is necessary
        tags = tags,
    )
