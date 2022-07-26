"""Checking naming conventions of class names.

"""
# Python Imports
import os
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters


class ClassName(filters.LineListener):
    """Check for the naming of files vs. class name.
    Support for directory ends with name *_env and *_pkg.
    [PACKAGE_NAME]_*comp*, then the inner class should have *comp* keyword(env, sqr, drv), but not with [PACKAGE_NAME]
     Given the package name, it is redundant to name class with package name. It's easier to reference a package's component with :: to it's component name directly.
    """
    subscribe_to = [filters.BeginClassBroadcaster]

    pkgdir_re = re.compile(r"(.*)\/(.*)_pkg")
    envdir_re = re.compile(r"(.*)\/(.*)_env")
    exempt_include_seq_re = re.compile(r"seq")

    class svclass(object):

        def __init__(self, name, file_name, begin_line_no, begin_line):
            self.name = name
            self.file_name = file_name
            self.begin_line_no = begin_line_no
            self.begin_line = begin_line

    def __init__(self, filename, fstream, *args, **kwargs):
        super(ClassName, self).__init__(filename, fstream, *args, **kwargs)
        self.filename = filename
        self.eof_called = False
        self.sv_classes = []
        self.current_class = None

    def update_beginclass(self, line_no, line, match):
        self.add_svclass(match.group('name'), line_no, line)

    def add_svclass(self, name, line_no, line):
        self.current_class = self.svclass(name, self.filename, line_no, line)
        self.sv_classes.append(self.current_class)

    def eof(self):
        if self.eof_called:
            return
        self.eof_called = True

        dirname = os.path.dirname(self.filename)
        file_base_name = os.path.splitext(os.path.basename(self.filename))[0]
        pkgdirname_match = self.pkgdir_re.search(dirname)
        envdirname_match = self.envdir_re.search(dirname)
        if pkgdirname_match:
            fileprefix = pkgdirname_match.group(2)
        elif envdirname_match:
            fileprefix = envdirname_match.group(2) + "_env"
        else:
            return
        for c in self.sv_classes:
            filesuffix = file_base_name.split('_')[-1]
            expected_suffix = filesuffix + "_c"
            if self.exempt_include_seq_re.search(c.name):
                return
            if c.name.startswith(fileprefix):
                self.error(
                    c.begin_line_no, c.begin_line,
                    "class '{}' does not match naming convention: expected '{}'. Including the package name in the class name is redundant because we use explicit package scoping."
                    .format(c.name, expected_suffix))
            elif not c.name.endswith(expected_suffix):
                self.error(
                    c.begin_line_no, c.begin_line,
                    "class '{}' does not match naming convention: expected '{}'. Recommend use suffix '_c' for class naming."
                    .format(c.name, expected_suffix))
