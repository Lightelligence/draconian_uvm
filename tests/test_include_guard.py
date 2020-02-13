import unittest
from unittest import mock
from io import StringIO

from context import draconian_uvm
from draconian_uvm import filters
from draconian_uvm.include_guard import IncludeGuard

import test

lbc = filters.LineBroadcaster

class IncludeGuardTestCase(test.TestCase):
    cut = IncludeGuard

    def test_minimum_pass(self):
        """Minimum legal subset."""
        content = StringIO("""`ifndef __BASE_TEST_SV__
         `define __BASE_TEST_SV__
        `endif // guard
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_header(self):
        """Adding a comment and whitespace header."""
        content = StringIO("""// Default header
        
        // Has some newlines, whitespace and comments
          // and poor indentation
        `ifndef __BASE_TEST_SV__
         `define __BASE_TEST_SV__
        `endif // guard
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_code_before_guard(self):
        content = StringIO("""// Default Header
        `include "rtl_defines.vh"
        `ifndef __BASE_TEST_SV__
         `define __BASE_TEST_SV__
          class base_test_c;
        `endif // guard
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Expected an include guard `ifndef directive in the first non-comment, non-blank line of the file.")
        
    def test_define_mismatch(self):
        content = StringIO("""// Default header
        `ifndef __BASE_TEST_SV__
         `define __BASE_TEST_SV_
        
        `endif // guard
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Include guard ifndef '__BASE_TEST_SV__' and define '__BASE_TEST_SV_' do not match.")

    def test_endif_mismatch(self):
        content = StringIO("""// Default header
        `ifndef __BASE_TEST_SV__
         `define __BASE_TEST_SV__
        
        `endif // guard
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Include guard ifndef '__BASE_TEST_SV__' and define '__BASE_TEST_SV_' do not match.")

    def test_missing_ifndef(self):
        content = StringIO("""// Default header
         `define __BASE_TEST_SV__
        `endif // guard
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Expected an include guard `ifndef directive in the first non-comment, non-blank line of the file.")
            
    def test_missing_define(self):
        content = StringIO("""// Default header
        `ifndef __BASE_TEST_SV__
        
        `endif // guard
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Never saw matching define for include guard ifndef '__BASE_TEST_SV__'")

    def test_missing_endif(self):
        content = StringIO("""// Default header
        `ifndef __BASE_TEST_SV__
         `define __BASE_TEST_SV__
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Never saw an endif for include guard '__BASE_TEST_SV__'")

    def test_endif_matches_guard(self):
        content = StringIO("""// Default header
        `ifndef __BASE_TEST_SV__
         `define __BASE_TEST_SV__
         `endif // __BASE_TEST_SV__
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_endif_mismatch(self):
        content = StringIO("""// Default header
        `ifndef __BASE_TEST_SV__
         `define __BASE_TEST_SV__
         `endif // __COPY_PASTE_LEFTOVERS__
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "The endif comment for include guard '__BASE_TEST_SV__' should be '__BASE_TEST_SV__' or 'guard'")

    def test_other_define_endif(self):
        content = StringIO("""// Default header
        `ifndef __BASE_TEST_SV__
         `define __BASE_TEST_SV__
         `define ONE 1
         `ifdef ONE
           `define TWO 2
         `endif // not_guard
         `endif // guard
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_mismatch_filename(self):
        content = StringIO("""// Default header
        `ifndef __TEST__
         `define __TEST__
         `endif // guard
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "The include guard doesn't match expected format.")

if __name__ == '__main__':
    unittest.main()
