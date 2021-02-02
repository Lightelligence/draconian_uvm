import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.uvm_msg import UvmMsg

import test

lbc = filters.LineBroadcaster

class UvmMsgTestCase(test.TestCase):
    cut = UvmMsg
#        `uvm_info("msg_header", $sformatf("val: %0d", val), UVM_LOW)
    
    def test_uvm_info_low(self):
        """uvm_info not recommended."""
        content = StringIO("""
        `uvm_info("eic_intr_sb:", $sformatf("Receive pre_write ictl_intr_sum_w1c_reg[%0s]", rw.convert2string()), UVM_LOW);
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Usage of uvm_info is not recommended, please use cmn_info() or cmn_dbg() instead.")

    def test_uvm_info_high(self):
        """uvm_info not recommended."""
        content = StringIO("""
        `uvm_info("msg_header", $sformatf("val: %0d", val), UVM_HIGH)
        """) 
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Usage of uvm_info is not recommended, please use cmn_dbg() instead.")

    def test_cmn_dbg(self):
        """uvm_info not recommended."""
        content = StringIO("""
        `cmn_dbg(UVM_HIGH, ("val_0[%0d], val_1[%0d]", 0, 1));
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut)) 
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()
                              
    def test_uvm_warning(self):
        """uvm_warning not recommended."""
        content = StringIO("""
        `uvm_warning("msg_header", $sformatf("val: %0d", val))
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Usage of uvm_warning is not recommended, please use cmn_warn() instead.")

    def test_uvm_error(self):
        """uvm_error not recommended."""
        content = StringIO("""
        `uvm_error("msg_header", $sformatf("val: %0d", val))
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Usage of uvm_error is not recommended, please use cmn_err() instead.")

    def test_uvm_fatal(self):
        """uvm_fatal not recommended."""
        content = StringIO(""" 
        `uvm_fatal("msg_header", $sformatf("val: %0d", val))
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut)) 
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Usage of uvm_fatal is not recommended, please use cmn_fatal() instead.")    


if __name__ == '__main__':
    unittest.main()
