"""Import all the files so that derived listeners get registered."""
import glob
import importlib.util
import os

lib_dir = os.path.abspath(os.path.dirname(__file__))
srcs = glob.glob(os.path.join(lib_dir, "*.py"))

for src in srcs:
    if src == __file__:
        continue
    spec = importlib.util.spec_from_file_location("module.name", src)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
