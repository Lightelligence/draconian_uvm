load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")
load("@pip_deps//:requirements.bzl", "requirement")

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
