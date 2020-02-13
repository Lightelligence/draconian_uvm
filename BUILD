py_library(
    name = "lib",
    srcs = glob(["duvm/*.py"]),
    deps = ["@lintworks//:lintworks"],
)

py_binary(
    name = "draconian_uvm",
    srcs = ["main.py"],
    deps = [":lib"],
    main = "main.py",
    visibility = ["//visibility:public"],
)

# Would prefer not to export this, but py_test obnoxiously requries a main variable even when providing a py_binary
exports_files([
    "main.py",
])
