py_library(
    name = "draconian_uvm_lib",
    srcs = glob(["duvm/*.py"]),
    deps = ["@lintworks//:lintworks"],
)

py_binary(
    name = "draconian_uvm_bin",
    srcs = ["main.py"],
    deps = [":draconian_uvm_lib"],
    main = "main.py",
)
