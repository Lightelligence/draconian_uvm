"""Derived class naming schema

"""
# Python Imports
import os
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters


class ClassnameSchema(filters.LineListener):
    """Check for the naming of class should match with derived class
     UVM components/objects hash table for naming schema
    """

    subscribe_to = [filters.BeginClassBroadcaster]

    scopedname_re = re.compile(r"pkg::\s*([^ \#]+)")
    baseclassname_re = re.compile(r".*(base|top)_(.*)")

    schema_dict = {
        "uvm_env": "env_c",
        "uvm_agent": "agent_c",
        "uvm_monitor": "mon_c",
        "uvm_scoreboard": "sb_c",
        "uvm_sequence_item": "item_c",
        "uvm_sequencer": "sqr_c",
        "uvm_driver": "drv_c",
        "uvm_sequence": "seq_c",
        "uvm_sequence_base": "seq_c",
        "uvm_component": None,
        "uvm_object": None,
        "uvm_reg_adapter": "reg_adapter_c",
        "uvm_reg_block": "reg_block_c",
        "uvm_reg_cbs": "cb_c"
    }

    def update_beginclass(self, line_no, line, match):
        derived_classname = match.group('name')
        base_classname = match.group('base')
        if base_classname in self.schema_dict:
            if self.schema_dict[base_classname] == None:
                return
            if not derived_classname.endswith(self.schema_dict[base_classname]):
                self.error(
                    line_no, line,
                    "Derived class '{}' not ending with '{}'. Recommend using suffix '{}' as derived class for base class '{}'"
                    .format(derived_classname, self.schema_dict[base_classname], self.schema_dict[base_classname],
                            base_classname))
        else:
            baseclassname_match = self.baseclassname_re.search(base_classname)
            if baseclassname_match:
                base_classname = baseclassname_match.group(2)

            scopename_match = self.scopedname_re.search(base_classname)
            if scopename_match:
                base_classname = scopename_match.group(1)

            if not derived_classname.endswith(base_classname):
                self.error(
                    line_no, line,
                    "Derived class '{}' not ending with '{}'. Recommend using suffix '{}' as derived class for base class '{}'"
                    .format(derived_classname, base_classname, base_classname, base_classname))
