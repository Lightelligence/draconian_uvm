def duvm_test(name, srcs):
    """Run draconian_uvm on source files."""
    native.py_test(
        name = name,
        srcs = ["@draconian_uvm//:draconian_uvm"],
        data = srcs,
        args = [" ".join(["$(location {})".format(s) for s in srcs])],
        main = "@draconian_uvm//:main.py", # Seems silly that this is necessary
    )
