import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.coverage_suffix import CoverageSuffix

import test

lbc = filters.LineBroadcaster

class CoverageSuffixTestCase(test.TestCase):
    cut = CoverageSuffix
    
    def test_cov_endswith_cg(self):
        """covergroup ends with _cg."""
        content = StringIO("""
        covergroup core_id_cg;
        covergroup edl_comb_harvest_cg with function sample(edl_combination_req_cov_struct_t edl_combination_req_cov_st);
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_cov_not_endswith_cg(self):
        """covergroup ends with _cg."""
        content = StringIO("""
        covergroup core_id;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Coverage group name not ending with _cg instead (core_id).")

    def test_cov_endswith_only_cg(self):
        """covergroup ends with _cg."""
        content = StringIO("""
        covergroup cg;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()
            #iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Usage of uvm_info is not recommended, please use cmn_info() or cmn_dbg() instead.")

if __name__ == '__main__':
    unittest.main()
