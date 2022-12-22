load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "lib",
    srcs = glob(["duvm/*.py"]),
    visibility = ["//visibility:public"],
    deps = ["@lintworks//:lib"],
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

exports_files([
    "duvm/lw_rc.py",
])
