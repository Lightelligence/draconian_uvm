import unittest
from unittest import mock
from io import StringIO

from context import draconian_uvm
from draconian_uvm import filters
from draconian_uvm.multiple_classes import MultipleClasses

import test

lbc = filters.LineBroadcaster

class MultipleClassesTestCase(test.TestCase):
    cut = MultipleClasses

    def test_simple_helper(self):
        content = StringIO()
        content.write("class special_cfg_c extends foo_pkg::cfg_c;\n")
        for i in range(10):
            content.write("  boring content\n")
        content.write("endclass : special_cfg_c\n")
        content.write("class base_test_c extends uvm_test;\n")
        for i in range(1000):
            content.write("  boring content\n")
        content.write("endclass : base_test_c\n")
        content = StringIO(content.getvalue())

        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_helper_too_large(self):
        content = StringIO()
        content.write("class special_cfg_c extends foo_pkg::cfg_c;\n")
        for i in range(150):
            content.write("  boring content\n")
        content.write("endclass : special_cfg_c\n")
        content.write("class base_test_c extends uvm_test;\n")
        for i in range(1000):
            content.write("  boring content\n")
        content.write("endclass : base_test_c\n")
        content = StringIO(content.getvalue())

        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "class special_cfg_c looks like a 'helper' class, but exceeds 100 lines. It deserves its own file.")

            
if __name__ == "__main__":
    unittest.main()
