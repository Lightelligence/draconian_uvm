py_library(
    name = "lib",
    srcs = glob(["duvm/*.py"]),
    deps = ["@lintworks//:lib"],
    visibility = ["//visibility:public"],
)

exports_files([
    "duvm/lw_rc.py",
])


py_library(
    name = "test",
    srcs = ["test.py"],
)

load("//:unit_test.bzl", "glob_to_individual_py_tests")

glob_to_individual_py_tests(
    files = glob(["tests/*.py"]),
)
