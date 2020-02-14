def duvm_test(name, srcs):
    """Run draconian_uvm on source files."""
    data = srcs + ["@draconian_uvm//:duvm/lw_rc.py"]
    native.py_test(
        name = name,
        srcs = ["@draconian_uvm//:draconian_uvm"],
        data = data,
        args = [
            "--rc $(location @draconian_uvm//:duvm/lw_rc.py)",
            " ".join(["$(location {})".format(s) for s in srcs]),
        ],
        main = "@draconian_uvm//:main.py", # Seems silly that this is necessary
    )
