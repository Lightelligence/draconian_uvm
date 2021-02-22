import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.classname_schema import ClassnameSchema

import test

lbc = filters.LineBroadcaster

class ClassnameSchemaTestCase(test.TestCase):
    cut = ClassnameSchema
    
    def test_uvm_derived_class_name_match_expectation(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        class a_env_c extends uvm_env;
        class b_c_agent_c extends uvm_agent;
        class mon_c extends uvm_monitor;
        class sb_c extends uvm_scoreboard;
        class d_drv_c extends uvm_driver;
        class e_item_c extends uvm_sequence_item;
        class base_seq_c extends uvm_sequence #(random_pkg::item_c);
        class base_sqr_c extends uvm_sequencer  #(random_pkg::item_c);
        class clr_cb_c extends uvm_reg_cbs;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()
            
    def test_uvm_derived_class_with_scope(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        class item_c extends hostmem_mirror_pkg::item_c;
        class mem_op_item_c extends probe_pkg::item_c#(mem_op_t);
        class lz_q_c #(type T=uvm_object) extends cmn_pkg::lz_q_c#(T);
        class tr_q_c #(type T=uvm_object) extends cmn_pkg::tr_q_c #(T);
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_derived_env_name_not_match_expectation(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        class a_env extends uvm_env;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Derived class 'a_env' not ending with 'env_c'. Recommend using suffix 'env_c' as derived class for base class 'uvm_env'")

    def test_derived_env_name_not_match_baseclass(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        class sb_c extends uvm_env;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Derived class 'sb_c' not ending with 'env_c'. Recommend using suffix 'env_c' as derived class for base class 'uvm_env'")

    def test_derived_class_a_name_match_expectation(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        class err_drv_c extends drv_c;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_derived_class_b_name_match_expectation(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        class db_err_drv_c extends err_drv_c;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_derived_class_name_not_match_expectation(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        class drv_instance_c extends drv_c;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Derived class 'drv_instance_c' not ending with 'drv_c'. Recommend using suffix 'drv_c' as derived class for base class 'drv_c'")

    def test_derived_class_from_base_class(self):
        """match rules for derived_class extends uvm_base_class """
        content = StringIO("""
        class derived_seq_c extends env_pkg::a_base_seq_c;
        class item_c extends env_pkg::base_item_c;
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()
      

if __name__ == '__main__':
    unittest.main()
