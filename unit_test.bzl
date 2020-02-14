def glob_to_individual_py_tests(files):
    for name in files:
        native.py_test(
            name = name.replace("/", "_").replace(".", "_"),
            srcs = [name],
            deps = [
                ":test",
                ":lib"
            ],
            main = name,
        )
