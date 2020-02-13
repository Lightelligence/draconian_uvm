import unittest
from unittest import mock
from io import StringIO

from context import draconian_uvm
from draconian_uvm import filters
from draconian_uvm.misleading_sformat import MisleadingSformat

import test

lbc = filters.LineBroadcaster

class MisleadingSformatTestCase(test.TestCase):

    cut = MisleadingSformat

    def test_hex_hex(self):
        """Hex matches hex."""
        content = StringIO("""
        $sformatf("0x%0x", data);
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_hex_hex_upcase(self):
        """Hex mismatch bin"""
        content = StringIO("""
        $sformatf("0X%0x", data);
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_hex_bin(self):
        """Hex mismatch bin"""
        content = StringIO("""
        $sformatf("0x%-32b", data);
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Representation (0x) and format specifier (-32b) have mismatching bases.")

    def test_bin_hex(self):
        """Hex mismatch bin"""
        content = StringIO("""
        $sformatf("0b%0x", data);
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Representation (0b) and format specifier (0x) have mismatching bases.")

    def test_dec_bin(self):
        """Hex mismatch bin"""
        content = StringIO("""
        $sformatf("0d%0b", data);
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Representation (0d) and format specifier (0b) have mismatching bases.")

    def test_vhex_hex(self):
        """Hex mismatch bin"""
        content = StringIO("""
        $sformatf("'h%x", data);
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()
        
    def test_vhex_bin(self):
        """Hex mismatch bin"""
        content = StringIO("""
        $sformatf("'h%0b", data);
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Representation ('h) and format specifier (0b) have mismatching bases.")

if __name__ == '__main__':
    unittest.main()
