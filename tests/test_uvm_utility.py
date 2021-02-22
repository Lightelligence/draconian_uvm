import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.uvm_utility import UvmUtility

import test

lbc = filters.LineBroadcaster

class UvmUtilityTestCase(test.TestCase):
    cut = UvmUtility
    
    def test_uvm_component_util_match_expectation(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
        class sb_c extends uvm_component;
          cfg_c cfg;

          `uvm_component_utils_begin(core_env_pkg::sb_c)
            `uvm_field_object(cfg, UVM_REFERENCE)
          `uvm_component_utils_end
        endclass sb_c

        class random extends base_test;
          `uvm_component_utils(random)
        endclass : random

        class drv_c extends uvm_driver;
          `uvm_component_utils_begin(drv_c)
           `uvm_field_string(intf_name,     UVM_COMPONENT)
        endclass : drv_c

        class sub_drv_c extends drv_c;
          `uvm_component_utils_begin(sub_drv_c)
           `uvm_field_string(intf_name,     UVM_COMPONENT)
           `uvm_field_int(init_delay_ps,    UVM_COMPONENT | UVM_DEC)
           `uvm_field_int(init_value,       UVM_COMPONENT | UVM_DEC)
           `uvm_field_int(period_ps,        UVM_COMPONENT | UVM_DEC)
          `uvm_component_utils_end
        endclass : sub_drv_c

        class sqr_c #(int ADDR_WIDTH = 32,int DATA_WIDTH = 32) extends uvm_sequencer #(item_c #(ADDR_WIDTH,DATA_WIDTH), item_c #(ADDR_WIDTH,DATA_WIDTH));
          `uvm_component_param_utils_begin(apb_pkg::sqr_c#(ADDR_WIDTH,DATA_WIDTH))
          `uvm_component_utils_end
        endclass : sqr_c


        class seq_c #(int ADDR_WIDTH = 32, int DATA_WIDTH = 32) extends  uvm_sequence #(item_c);
          `uvm_object_param_utils_begin(apb_pkg::seq_c#(ADDR_WIDTH,DATA_WIDTH))
          `uvm_object_utils_end
        endclass :seq_c

        class a_seq_c extends  uvm_sequence #(item_c);
          `uvm_object_utils_begin(eu_core_pkg::seq_c)
          `uvm_object_utils_end
        endclass : seq_c

        class item_c #(int ADDR_WIDTH = 32, int DATA_WIDTH = 32) extends uvm_sequence_item;
          `uvm_object_param_utils_begin(apb_pkg::item_c#(ADDR_WIDTH,DATA_WIDTH))
            `uvm_field_object(id, UVM_REFERENCE)
          `uvm_object_utils_end
        endclass : item_c
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_uvm_component_use_object_util(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
        class random extends base_test;
          `uvm_object_utils(random)
        endclass : random
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Class random is uvm_component but using uvm_object_utils, should replace it with uvm_component_utils")

    def test_uvm_object_use_component_util(self):
        """using uvm_component_utils in the right scope """
        content = StringIO("""
         class a_seq_c extends  uvm_sequence #(item_c);
           `uvm_component_utils_begin(eu_core_pkg::seq_c)
           `uvm_component_utils_end
         endclass : seq_c
        """)
        content = StringIO(content.getvalue())
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Class a_seq_c is uvm_object but using uvm_component_utils, should replace it with uvm_object_utils")

if __name__ == '__main__':
    unittest.main()
