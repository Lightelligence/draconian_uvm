"""Checking files'name inside pkg.

"""
# Python Imports
import os
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters


class PkgName(filters.LineListener):
    """Check for the naming of files match pkg name.
    Support for directory ends with name *_env and *_pkg.
     #1: [PACKAGE_NAME]_pkg, then all the files `include in the PACKAGE_NAME_pkg should have prefix PACKAGE_NAME_*
         With certain package name, the files in the same package should share the same prefix to help locating and refering to the package components.
     #2: Directory name should match with the files name as prefix.
    """

    subscribe_to = [
        filters.TestbenchTopLineBroadcaster,
        filters.UVCLineBroadcaster,
        filters.TestLineBroadcaster,
    ]

    pkg_re = re.compile(r"(.*)_pkg.sv*")
    pkgdir_re = re.compile(r"(.*)\/(.*)_pkg")
    envdir_re = re.compile(r"(.*)\/(.*)_env")
    include_re = re.compile("^\s*`include\s+\"(.*)\"")

    def __init__(self, filename, fstream, *args, **kwargs):
        super(PkgName, self).__init__(filename, fstream, *args, **kwargs)
        self.filename = filename
        self._in_pkg_file = False
        basename = os.path.basename(filename)
        pkg_match = self.pkg_re.search(basename)
        if pkg_match:
            self._in_pkg_file = True
            self._pkg_name = pkg_match.group(1)
            file_base_name = os.path.splitext(os.path.basename(self.filename))[0]
            dirname = os.path.dirname(self.filename)
            pkgdirname_match = self.pkgdir_re.search(dirname)
            envdirname_match = self.envdir_re.search(dirname)
            exp_pkg_name = None
            if pkgdirname_match:
                fileprefix = pkgdirname_match.group(2)
                exp_pkg_name = fileprefix + "_pkg"
            elif envdirname_match:
                fileprefix = envdirname_match.group(2) + "_env"
                exp_pkg_name = fileprefix + "_pkg"
            else:
                return
            if not exp_pkg_name == file_base_name:
                self.error(
                    None, None,
                    "pkg file name not match with directory name. pkg_name({}) - suggested name ({}).".format(
                        file_base_name, exp_pkg_name))

    def _update(self, line_no, line):
        if self._in_pkg_file:
            # check if all the included files has expected names
            includematch = self.include_re.search(line)
            if includematch:
                representation = includematch.group(1)
                if representation.startswith("uvm_"):
                    return
                if not representation.startswith(self._pkg_name):
                    self.error(
                        line_no, line,
                        "include file but not with corresponding pkg name. pkg_name({}) - included file name ({}).".
                        format(self._pkg_name, representation))

    update_testbenchtopline = _update
    update_testline = _update
    update_uvcline = _update
