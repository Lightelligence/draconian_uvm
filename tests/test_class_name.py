import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.class_name import ClassName

import test

lbc = filters.LineBroadcaster

class ClassNameTestCase(test.TestCase):
    cut = ClassName
    
    def test_component_name_match_expectation(self):
        """include file name should match with directory name - env."""
        content = StringIO("""
        class sb_c extends uvm_component;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/sys_env/sys_env_sb.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_component_prefix_not_match_expectation(self):
        content = StringIO()
        content.write("class sys_env_sb_c extends uvm_component;\n")
        for i in range(30):
            content.write("  boring content\n")
        content.write("endclass : sys_env_sb_c\n")
        content = StringIO(content.getvalue())

        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/sys_env/sys_env_sb.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "class name sys_env_sb_c does not match expectation. It's redundant to use pkg name sys_env as prefix.")


    def test_component_suffix_not_match_expectation(self):
        content = StringIO()
        content.write("class sb extends uvm_component;\n")
        for i in range(30):
            content.write("  boring content\n")
        content.write("endclass : sb\n")
        content = StringIO(content.getvalue())

        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/sys_env/sys_env_sb.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "class name sb does not match expectation. Recommend use suffix: sb_c")

if __name__ == '__main__':
    unittest.main()
