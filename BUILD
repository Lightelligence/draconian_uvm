load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "lib",
    srcs = glob(["duvm/*.py"]),
    visibility = ["//visibility:public"],
    deps = ["@lintworks//:lib"],
)

exports_files([
    "duvm/lw_rc.py",
])

