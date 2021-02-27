import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.super_functask import SuperFuncTask

import test

lbc = filters.LineBroadcaster

class SuperFuncTaskTestCase(test.TestCase):
    cut = SuperFuncTask
    
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

    def test_super_match_current_automatic_function(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
        task automatic wait_clocks(input int unsigned num_clocks);
          int unsigned clocks_waited = 0;
          while (clocks_waited < num_clocks) begin
            @(posedge clk);
            clocks_waited += 1;
          end
        endtask
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_super_not_match_current_function(self):
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

    def test_scop_match(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
        function type_a v_mem_c::peek_mem(addr_type addr1, addr_type addr2);
          super.peek_mem(addr1, addr2);
          code;
          code;
        endfunction 

        task v_mem_c::monitor_mem(addr_type addr1, addr_type addr2);
          super.monitor_mem(addr1, addr2);
          code;
          code;
        endtask
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_scop_mismatch_function(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
        function type_a v_mem_c::peek_mem(addr_type addr1, addr_type addr2);
          super.new(addr1, addr2);
          code;
          code;
        endfunction 
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Super called with new, but not matching current function name: peek_mem")

    def test_super_match_current_task(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
        virtual task run_phase(uvm_phase phase);
          super.run_phase(phase);
          code;
          code;
        endtask : run_phase

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

    def test_super_not_match_current_task(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
        virtual task run_phase(uvm_phase phase);
          super.pre_run_phase(phase);
          code;
          code;
        endtask : run_phase
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Super called with pre_run_phase, but not matching current task name: run_phase")

    def test_scop_task(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
        task v_mem_c::peek_mem(addr_type addr1, addr_type addr2);
          super.new(addr1, addr2);
          code;
          code;
        endtask
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Super called with new, but not matching current task name: peek_mem")

    def test_super_scope_missmatch(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
        task v_mem_c::monitor_mem(addr_type addr1, addr_type addr2);
          code;
          code;
        endtask

        function type_a v_mem_c::peek_mem(addr_type addr1, addr_type addr2);
          super.monitor_mem(addr1, addr2);
          code;
          code;
        endfunction 
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Super called with monitor_mem, but not matching current function name: peek_mem")

if __name__ == '__main__':
    unittest.main()
