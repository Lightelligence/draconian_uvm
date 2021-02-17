import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.cnstr_suffix import CnstrSuffix

import test

lbc = filters.LineBroadcaster

class CnstrSuffixTestCase(test.TestCase):
    cut = CnstrSuffix
    
    def test_constraint_endswith_cnstr(self):
        """constraint name ends with _cnstr."""
        content = StringIO("""
        constraint a_num_items_cnstr{
        constraint b_num_items_cnstr {
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_constraint_not_endswith_cnstr(self):
        """constraint name ends with _cnstr."""
        content = StringIO("""
        constraint csl_sclk_period_const { //MHz 60:8332, 50:10000, 40:12500, 25:20000, 1:500000
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Constraint name not ending with _cnstr instead (csl_sclk_period_const).")

if __name__ == '__main__':
    unittest.main()
