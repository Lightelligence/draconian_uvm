import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.pkg_name import PkgName

import test

lbc = filters.LineBroadcaster


class PkgNameTestCase(test.TestCase):
    cut = PkgName

    def test_pkgname_match_dirname(self):
        """include file name should match with directory name - env."""
        content = StringIO("""
        `include "sys_env_sampleone_reg_block.svh"
        `include "sys_env_sampletwo_reg_block.svh"
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/sys_env/sys_env_pkg.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_pkgname_not_match_dirname(self):
        """include file name should match with directory name - env."""
        content = StringIO("""
        `include "sys_env_sampleone_reg_block.svh"
        `include "sys_env_sampletwo_reg_block.svh"
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/sys_env/sys_pkg.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(
                mock.ANY, mock.ANY, mock.ANY,
                "pkg file name not match with directory name. pkg_name(sys_pkg) - suggested name (sys_env_pkg).")

    def test_include_file_name_match_expectation(self):
        """include file name should match with directory name - env."""
        content = StringIO("""
        `include "sys_env_sampleone_reg_block.svh"
        `include "sys_env_sampletwo_reg_block.svh"
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/sys_env/sys_env_pkg.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_include_file_name_not_match_expectation(self):
        """include file name should match with directory name - env."""
        content = StringIO("""
        `include "sys_env_sampleone_reg_block.svh"
        `include "sys_sampletwo_reg_block.svh"
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/sys_env/sys_env_pkg.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(
                mock.ANY, mock.ANY, mock.ANY,
                "include file but not with corresponding pkg name. pkg_name(sys_env) - included file name (sys_sampletwo_reg_block.svh)."
            )


if __name__ == '__main__':
    unittest.main()
