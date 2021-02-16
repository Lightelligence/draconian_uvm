"""Check all files for class names vs. pkg name

"""
# Python Imports
import os
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters


class ClassnameGuard(filters.LineListener):
    """Check for the naming of files vs. class name.
    Support for directory ends with name *_env and *_pkg.
     #1: [PACKAGE_NAME]_pkg, then all the files `include in the PACKAGE_NAME_pkg should have prefix PACKAGE_NAME_*
         With certain package name, the files in the same package should share the same prefix to help locating and refering to the package components.
     #2: [PACKAGE_NAME]_*comp*, then the inner class should have *comp* keyword(env, sqr, drv), but not with [PACKAGE_NAME]
         Given the package name, it is redundent to name class with package name. It's easier to reference a package's component with :: to it's component name directly.
     #3: Directory name should match with the files name as prefix.
    """
    subscribe_to = [filters.TestbenchTopLineBroadcaster,
                    filters.UVCLineBroadcaster,
                    filters.TestLineBroadcaster,]

    line_is_comment_or_empty_re = re.compile("^\s*((//.*)|())$")
    #filename_re = re.compile("/tests/.*sv[h]?")
    pkg_re = re.compile(r"(.*)_pkg.sv*")
    pkgdir_re = re.compile(r"(.*)\/(.*)_pkg")
    envdir_re = re.compile(r"(.*)\/(.*)_env")

    include_re = re.compile("^\s*`include\s+\"(.*)\"")
    exempt_include_seq_re = re.compile(r"seq")
    exempt_regblock_re = re.compile(r"reg_block")
    begin_class_re = re.compile("^\s*(?P<virtual>virtual){0,1}\s*class\s+(?P<name>[^\s#]+)\s*(?P<params>#\(.*\)){0,1}(\s+extends\s+(?P<base>[^;]+)){0,1}\s*;")
    end_class_re = re.compile("^\s*endclass")

    sb_re = re.compile(r"sb") # fixme-hw: for debug

    class svclass(object):
        def __init__(self, name, file_name, begin_line_no, begin_line):
            self.name = name
            self.file_name = file_name
            self.pkg_prefix = None
            self.begin_line_no = begin_line_no
            self.begin_line = begin_line
            self.end_line_no = None

    def __init__(self, filename, fstream, *args, **kwargs):
        super(ClassnameGuard, self).__init__(filename, fstream, *args, **kwargs)
        self.filename = filename
        self._checking_prefix = False
        self._in_pkg_file = False
        self.eof_called = False
        self.sv_classes = []
        self.current_class = None
        basename  = os.path.basename(filename)
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
            if not exp_pkg_name == file_base_name :
                self.error(None, None, "pkg file name not match with directory name. pkg_name({}) - suggested name ({}).".format(file_base_name, exp_pkg_name))

    def update_beginclass(self, line_no, line, match):
        self.current_class = self.svclass(match.group('name'), line_no, line)

    def _update(self, line_no, line):
        if self._in_pkg_file:
            #check if all the included files has expected names
            file_base_name = os.path.splitext(os.path.basename(self.filename))[0]
            dirname = os.path.dirname(self.filename)
            includematch = self.include_re.search(line)
            if includematch:
                representation = includematch.group(1)
                #if representation.startswith("uvm_") or self.exempt_include_seq_re.search(representation):
                if representation.startswith("uvm_"):
                    return
                if not representation.startswith(self._pkg_name):
                    self.error(line_no, line, "include file but not with corresponding pkg name. pkg_name({}) - included file name ({}).".format(self._pkg_name, representation))

        if not self._in_pkg_file:
            begin_class_match = self.begin_class_re.search(line)
            if begin_class_match:
                self.update_svclass(begin_class_match.group('name'), line_no, line)

    def update_svclass(self, name, line_no, line):
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
        class_name_regex = re.compile("(.*)_c")
        primary_c = None
        for c in self.sv_classes:
            filesuffix = file_base_name.split('_')[-1]
            expected_suffix = filesuffix + "_c"
            if self.exempt_include_seq_re.search(c.name):
                return
            if c.name.startswith(fileprefix):
                self.error(c.begin_line_no, c.begin_line, "class name {} does not match expectation. It's redundent to use pkg name {} as prefix.".format(c.name, fileprefix))
            elif not c.name.endswith(expected_suffix):
                self.error(c.begin_line_no, c.begin_line, "class name {} does not match expectation. Recommend use suffix: {}".format(c.name, expected_suffix))

    update_testbenchtopline = _update
    update_testline = _update
    update_uvcline = _update
