"""Helper functions to run python unit tests."""

def glob_to_individual_py_tests(files):  # buildifier: disable=unnamed-macro
    for file_name in files:
        native.py_test(
            name = file_name.replace("/", "_").replace(".", "_"),
            srcs = [file_name],
            deps = [
                ":test",
                ":lib",
            ],
            main = file_name,
        )
