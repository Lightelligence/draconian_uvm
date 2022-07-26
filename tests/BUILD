load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")
load("//:unit_test.bzl", "glob_to_individual_py_tests")
py_library(
    name = "test",
    srcs = ["test.py"],
)

buildifier(
    name = "buildifier_format_diff",
    diff_command = "diff",
    mode = "diff",
)

buildifier(
    name = "buildifier_lint",
    lint_mode = "warn",
    lint_warnings = [
        "-function-docstring-args",
        "-function-docstring",
    ],
    mode = "check",
)

buildifier(
    name = "buildifier_fix",
    lint_mode = "fix",
    mode = "fix",
)


glob_to_individual_py_tests(
    files = glob(["test_*.py"]),
    lib = "//:lib"
)
