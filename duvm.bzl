def duvm_test(name, srcs):
    """Run draconian_uvm on source files."""
    data = srcs + ["@draconian_uvm//:duvm/lw_rc.py", "@draconian_uvm//:lib"]

    native.py_test(
        name = name,
        srcs = ["@lintworks//:main"],
        data = data,
        args = [
            "--rc $(location @draconian_uvm//:duvm/lw_rc.py)",
            " ".join(["$(location {})".format(s) for s in srcs]),
        ],
        main = "@lintworks//:main.py", # Seems silly that this is necessary
    )
