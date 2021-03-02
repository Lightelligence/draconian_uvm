import unittest
from unittest import mock
from io import StringIO

from duvm import filters

import test

class FilterTestCase(test.TestCase):

    def tearDown(self):
        # Reset memoized_directories after each test otherwise test ordering matters
        filters.UVCLineBroadcaster.memoized_directories = {}
        super(FilterTestCase, self).tearDown()

    @staticmethod
    def _get_listener(broadcaster, listener_type):
        for listener in broadcaster.listener_instances:
            if isinstance(listener, listener_type):
                return listener
        return None

    def assertIgnoreLen(self, lb, testbench_top_len, test_len, uvc_len):
        testbench_top = self._get_listener(lb, filters.TestbenchTopLineBroadcaster)
        test          = self._get_listener(lb, filters.TestLineBroadcaster)
        uvc           = self._get_listener(lb, filters.UVCLineBroadcaster)
        self.assertEqual(len(testbench_top._ignored_broadcasters), testbench_top_len)
        self.assertEqual(len(test._ignored_broadcasters),          test_len)
        self.assertEqual(len(uvc._ignored_broadcasters),           uvc_len)

    def restrictions(self):
        return self.build_restriction_filter(filters.TestbenchTopLineBroadcaster, filters.TestLineBroadcaster, filters.UVCLineBroadcaster)

    def test_rtl_file(self):
        lb = filters.LineBroadcaster("/nfs/<user>/<checkout>/rtl/dma/dma.v", StringIO(), parent=None, gc=None, restrictions=self.restrictions())
        self.assertIgnoreLen(lb, 1, 1, 1)

    def test_testbench_top(self):
        lb = filters.LineBroadcaster("/nfs/<user>/<checkout>/dv/tb/dma_tb_top.sv", StringIO(), parent=None, gc=None, restrictions=self.restrictions())
        self.assertIgnoreLen(lb, 0, 1, 1)

    def test_test(self):
        fstream = StringIO()
        lb = filters.LineBroadcaster("/nfs/<user>/<checkout>/dv/tests/base_test.sv", StringIO(), parent=None, gc=None, restrictions=self.restrictions())
        self.assertIgnoreLen(lb, 1, 0, 1)
        
    def test_uvc(self):
        # This mocks the "<dir>_pkg.sv" file in to existance
        with mock.patch("glob.glob", lambda x : ["dma_pkg.sv"]):
            lb = filters.LineBroadcaster("/nfs/<user>/<checkout>/dv/agents/dma/dma_drv.sv", StringIO(), parent=None, gc=None, restrictions=self.restrictions())
            self.assertIgnoreLen(lb, 1, 1, 0)
        # The second time it is called in the same process, the directory should be memoized.
        lb = filters.LineBroadcaster("/nfs/<user>/<checkout>/dv/agents/dma/dma_mon.sv", StringIO(), parent=None, gc=None, restrictions=self.restrictions())
        self.assertIgnoreLen(lb, 1, 1, 0)

    def test_not_uvc(self):
        with mock.patch("glob.glob", lambda x : []):
            lb = filters.LineBroadcaster("/nfs/<user>/<checkout>/dv/agents/dma/dma_drv.sv", StringIO(), parent=None, gc=None, restrictions=self.restrictions())
            self.assertIgnoreLen(lb, 1, 1, 1)
        # The second time it is called in the same process, the directory should be memoized.
        lb = filters.LineBroadcaster("/nfs/<user>/<checkout>/dv/agents/dma/dma_mon.sv", StringIO(), parent=None, gc=None, restrictions=self.restrictions())
        self.assertIgnoreLen(lb, 1, 1, 1)


class ClassTestCase(test.TestCase):


    def test_simple(self):
        content = StringIO("""
        class base_test_c;
        """)
        cut = filters.BeginClassBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), None)
            self.assertEqual(match.group('name'), 'base_test_c')
            self.assertEqual(match.group('base'), None)

    def test_simple_inheritance(self):
        content = StringIO("""
        class base_test_c extends uvm_test; 
        """)
        cut = filters.BeginClassBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), None)
            self.assertEqual(match.group('name'), 'base_test_c')
            self.assertEqual(match.group('base'), 'uvm_test')

    def test_virtual(self):
        content = StringIO("""
        virtual class base_test_c extends uvm_test; 
        """)
        cut = filters.BeginClassBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), 'virtual')
            self.assertEqual(match.group('name'), 'base_test_c')
            self.assertEqual(match.group('base'), 'uvm_test')

    def test_params(self):
        content = StringIO("""
        virtual class base_test_c #(type T=int, type S=int) extends uvm_test; 
        """)
        cut = filters.BeginClassBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), 'virtual')
            self.assertEqual(match.group('name'), 'base_test_c')
            self.assertEqual(match.group('params'), '#(type T=int, type S=int)')
            self.assertEqual(match.group('base'), 'uvm_test')

    def test_both_side_params(self):
        content = StringIO("""
        virtual class seq_c #(type T=int, type S=int) extends uvm_sequence #(item_c); 
        """)
        cut = filters.BeginClassBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), 'virtual')
            self.assertEqual(match.group('name'), 'seq_c')
            self.assertEqual(match.group('params'), '#(type T=int, type S=int)')
            self.assertEqual(match.group('base'), 'uvm_sequence')
        
    def test_endclass(self):
        content = StringIO("""
        endclass : base_test_c
        """)
        cut = filters.EndClassBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()

    def test_extern_function(self):
        content = StringIO("""
        extern function poke();
        """)
        cut = filters.BeginFunctionBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_not_called()

    def test_simple_function(self):
        content = StringIO("""
        function pre_run_test();
        """)
        cut = filters.BeginFunctionBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), None)
            self.assertEqual(match.group('name'), 'pre_run_test')
            self.assertEqual(match.group('return'), None)

    def test_virtual_function(self):
        content = StringIO("""
        virtual function void put_up_response(UP_TRAFFIC _up_traffic);
        """)
        cut = filters.BeginFunctionBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), 'virtual')
            self.assertEqual(match.group('name'), 'put_up_response')

    def test_scope_function(self):
        content = StringIO("""
        function type_a v_mem_c::peek_mem(addr_type addr1, addr_type addr2);
        """)
        cut = filters.BeginFunctionBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), None)
            self.assertEqual(match.group('name'), 'v_mem_c::peek_mem')

    def test_param_function(self):
        content = StringIO("""
        virtual function void write_sqr_export(item_c #(ADDR_WIDTH,DATA_WIDTH) _item);
        """)
        cut = filters.BeginFunctionBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), 'virtual')
            self.assertEqual(match.group('name'), 'write_sqr_export')

    def test_static_function(self):
        content = StringIO("""
        static function void print_itemized_instr(instr_t _instr_q[$]) ;
        """)
        cut = filters.BeginFunctionBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), None)
            self.assertEqual(match.group('static'), 'static')
            self.assertEqual(match.group('name'), 'print_itemized_instr')

    def test_endfunction(self):
        content = StringIO("""
        endfunction : poke
        """)
        cut = filters.EndFunctionBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()

    def test_extern_task(self):
        content = StringIO("""
        extern task store();
        """)
        cut = filters.BeginTaskBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_not_called()

    def test_automatic_task(self):
        content = StringIO("""
        task automatic wait_clocks(input int unsigned num_clocks);
        """)
        cut = filters.BeginTaskBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), None)
            self.assertEqual(match.group('name'), 'wait_clocks')

    def test_simple_task(self):
        content = StringIO("""
        task pre_body();
        """)
        cut = filters.BeginTaskBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), None)
            self.assertEqual(match.group('name'), 'pre_body')

    def test_virtual_task(self):
        content = StringIO("""
        virtual task put_up_response(UP_TRAFFIC _up_traffic);
        """)
        cut = filters.BeginTaskBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), 'virtual')
            self.assertEqual(match.group('name'), 'put_up_response')

    def test_scope_task(self):
        content = StringIO("""
        task v_mem_c::peek_mem(addr_type addr1, addr_type addr2);
        """)
        cut = filters.BeginTaskBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), None)
            self.assertEqual(match.group('name'), 'v_mem_c::peek_mem')

    def test_param_task(self):
        content = StringIO("""
        virtual task write_sqr_export(item_c #(ADDR_WIDTH,DATA_WIDTH) _item);
        """)
        cut = filters.BeginTaskBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()
            match = iut.broadcast.call_args[0][3]
            self.assertEqual(match.group('virtual'), 'virtual')
            self.assertEqual(match.group('name'), 'write_sqr_export')

    def test_endtask(self):
        content = StringIO("""
        endtask : poke
        """)
        cut = filters.EndTaskBroadcaster
        lbc = filters.LineBroadcaster
        with mock.patch.object(cut, "broadcast", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(cut))
            iut = self.get_listener(lb, cut)
            iut.broadcast.assert_called_once()

if __name__ == '__main__':
    unittest.main()
