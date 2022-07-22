load("//:unit_test.bzl", "glob_to_individual_py_tests")

py_library(
    name = "lib",
    srcs = glob(["duvm/*.py"]),
    visibility = ["//visibility:public"],
    deps = ["@lintworks//:lib"],
)

exports_files([
    "duvm/lw_rc.py",
])

py_library(
    name = "test",
    srcs = ["test.py"],
)

glob_to_individual_py_tests(
    files = glob(["tests/*.py"]),
)
