"""Top-level macro for running draconian_uvm tests."""

load("@rules_python//python:defs.bzl", "py_test")

def duvm_test(name, srcs, tags = []):
    """Run draconian_uvm on source files."""
    data = srcs + ["@draconian_uvm//:duvm/lw_rc.py", "@draconian_uvm//:lib"]

    py_test(
        name = name,
        srcs = ["@lintworks//:main"],
        data = data,
        args = [
            "--rc $(location @draconian_uvm//:duvm/lw_rc.py)",
            " ".join(["$(locations {})".format(s) for s in srcs]),
        ],
        main = "@lintworks//:main.py",  # Seems silly that this is necessary
        tags = tags,
    )
