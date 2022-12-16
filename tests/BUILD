load("@rules_python//python:defs.bzl", "py_library")
load("//:unit_test.bzl", "glob_to_individual_py_tests")

py_library(
    name = "test",
    srcs = ["test.py"],
)

glob_to_individual_py_tests(
    files = glob(["test_*.py"]),
)
