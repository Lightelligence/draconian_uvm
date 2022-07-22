"""Check for accidental use of the wrong UVM utility macro.

"""
# Python Imports
import os
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters


class UvmUtility(filters.LineListener):
    """Check for the using of UVM utilities
     should use `uvm_component_utils and `uvm_object_utils in the right scopes.
    """

    subscribe_to = [
        filters.BeginClassBroadcaster, filters.EndClassBroadcaster, filters.TestLineBroadcaster,
        filters.UVCLineBroadcaster
    ]

    baseclassname_re = re.compile(r".*base(_.*)")

    uvm_utils_re = re.compile(r"^\s*\`((uvm_component_utils)|(uvm_object_utils)).*")

    class svclass(object):

        def __init__(self, name, base_class, begin_line_no, begin_line):
            self.name = name
            self.base_class = base_class
            self.begin_line_no = begin_line_no
            self.begin_line = begin_line
            self.use_uvm_utils = False
            self.uvm_util = None

    compdict = {
        "uvm_component": "ignore",
        "uvm_test": "_test",
        "uvm_env": "env_c",
        "uvm_agent": "agent_c",
        "uvm_monitor": "mon_c",
        "uvm_scoreboard": "sb_c",
        "uvm_sequencer": "sqr_c",
        "uvm_driver": "drv_c"
    }

    objdict = {
        "uvm_sequence_item": "item_c",
        "uvm_sequence": "seq_c",
        "uvm_sequence_base": "seq_c",
        "uvm_object": "ignore",
        "uvm_reg_block": "reg_block_c"
    }

    def __init__(self, filename, fstream, *args, **kwargs):
        super(UvmUtility, self).__init__(filename, fstream, *args, **kwargs)
        self.sv_classes = []
        self.current_class = None
        self.eof_called = False

    def update_beginclass(self, line_no, line, match):
        self.current_class = self.svclass(match.group('name'), match.group('base'), line_no, line)

    def update_endclass(self, line_no, line, match):
        if self.current_class is None:
            self.error(line_no, line, "Saw endclass before class definition")
            return
        self.current_class.end_line_no = line_no
        self.sv_classes.append(self.current_class)
        self.current_class = None

    def eof(self):
        if self.eof_called:
            return
        self.eof_called = True

        for c in self.sv_classes:
            if c.use_uvm_utils:
                suffixname = '_'.join(c.base_class.split('_')[-2:])
                baseclassname_match = self.baseclassname_re.search(suffixname)
                if baseclassname_match:
                    suffixname = baseclassname_match.group(1)

                if c.base_class in self.compdict or suffixname in self.compdict.values():
                    if not c.uvm_util == 'uvm_component_utils':
                        self.error(
                            c.begin_line_no, c.begin_line,
                            "Class {} is uvm_component but using {}, should replace it with uvm_component_utils".format(
                                c.name, c.uvm_util))

                if c.base_class in self.objdict or suffixname in self.objdict.values():
                    if not c.uvm_util == 'uvm_object_utils':
                        self.error(
                            c.begin_line_no, c.begin_line,
                            "Class {} is uvm_object but using {}, should replace it with uvm_object_utils".format(
                                c.name, c.uvm_util))

    def _update(self, line_no, line):
        if not self.current_class == None:
            utilmatch = self.uvm_utils_re.search(line)
            if utilmatch:
                self.current_class.use_uvm_utils = True
                self.current_class.uvm_util = utilmatch.group(1)

    update_uvcline = _update
    update_testline = _update
