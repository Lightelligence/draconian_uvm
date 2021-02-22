import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.super_function import SuperFunction

import test

lbc = filters.LineBroadcaster

class SuperFunctionTestCase(test.TestCase):
    cut = SuperFunction
    
    def test_super_match_current_function(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
        virtual function void build_phase(uvm_phase phase);
          super.build_phase(phase);
          code;
          code;
        endfunction : build_phase

        virtual function void build_phase(uvm_phase phase);
          super.build_phase (phase);
          code;
          code;
        endfunction : build_phase
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_super_match_current_function(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
        virtual function void build_phase(uvm_phase phase);
          super.new();
          code;
          code;
        endfunction : build_phase
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Super called with new, but not matching current function name: build_phase")

if __name__ == '__main__':
    unittest.main()
