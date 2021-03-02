import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.instancename_schema import InstancenameSchema

import test

lbc = filters.LineBroadcaster

class InstancenameSchemaTestCase(test.TestCase):
    cut = InstancenameSchema
    
    def test_instance_name_match_expectation(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        uvm_analysis_port#(UP_TRAFFIC) up_traffic_port_ap;
        uvm_analysis_port #(item_c) rx_data_ap;
        uvm_analysis_imp_iid_instr #(iid_instr_pkg::item_c, sb_c) iid_instr_imp;
        uvm_event edl_cmd_finished_event;
        uvm_event edl_cmd_finished_event ;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_analysisimp_not_match_expectation(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        uvm_analysis_imp_iid_instr #(iid_instr_pkg::item_c, sb_c) iid_instr_xp;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Instance name 'iid_instr_xp' not ending with 'imp'. Recommend using suffix 'imp' as instance name for 'uvm_analysis_imp'")

    def test_analysisimp_not_match_expectation(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        uvm_analysis_imp_iid_instr #(iid_instr_pkg::item_c, sb_c) iid_instr_xp;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Instance name 'iid_instr_xp' not ending with 'imp'. Recommend using suffix 'imp' as instance name for 'uvm_analysis_imp'")

    def test_event_not_match_expectation(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        uvm_event edl_cmd_finished;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Instance name 'edl_cmd_finished' not ending with 'event'. Recommend using suffix 'event' as instance name for 'uvm_event'")

if __name__ == '__main__':
    unittest.main()
