"""Helper functions to run python unit tests."""

load("@rules_python//python:defs.bzl", "py_test")

def glob_to_individual_py_tests(files):  # buildifier: disable=unnamed-macro
    for file_name in files:
        py_test(
            name = file_name.replace("/", "_").replace(".", "_"),
            srcs = [file_name],
            deps = [
                ":test",
                "//:lib",
            ],
            main = file_name,
        )
