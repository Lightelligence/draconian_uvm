load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")
load("//:unit_test.bzl", "glob_to_individual_py_tests")

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
    mode = "fix",
)

buildifier(
    name = "buildifier_fix",
    lint_mode = "fix",
    mode = "fix",
)

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
