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

    classname_re = re.compile(r"^\s*class\s+([^ ]+)\s+.*extends\s+([^ ]+).*;")
    scopedname_re = re.compile(r"pkg\:\:\s*([^ \#]+)")
    baseclassname_re = re.compile(r".*base_(.*)")

    thisdict = {
        "uvm_env": "env_c",
        "uvm_agent" : "agent_c",
        "uvm_monitor" : "mon_c",
        "uvm_scoreboard" : "sb_c",
        "uvm_sequence_item" : "item_c",
        "uvm_sequencer" : "sqr_c",
        "uvm_driver": "drv_c",
        "uvm_sequence": "seq_c",
        "uvm_sequence_base": "seq_c",
        "uvm_component": "ignore",
        "uvm_object": "ignore",
        "uvm_reg_cbs": "cb_c"
    }

    def update_beginclass(self, line_no, line, match):
        match = self.classname_re.search(line)
        if match:
            derived_classname = match.group(1)
            base_classname = match.group(2)
            if base_classname in self.thisdict:
                if self.thisdict[base_classname] == 'ignore':
                    return
                if not derived_classname.endswith(self.thisdict[base_classname]):
                   self.error(line_no, line, "Derived class '{}' not ending with '{}'. Recommend using suffix '{}' as derived class for base class '{}'".format(derived_classname, self.thisdict[base_classname], self.thisdict[base_classname], base_classname))
            else :
                baseclassname_match = self.baseclassname_re.search(base_classname)
                if baseclassname_match:
                    base_classname = baseclassname_match.group(1)

                scopename_match = self.scopedname_re.search(base_classname)
                if scopename_match:
                    base_classname = scopename_match.group(1)

                if not derived_classname.endswith(base_classname):
                    self.error(line_no, line, "Derived class '{}' not ending with '{}'. Recommend using suffix '{}' as derived class for base class '{}'".format(derived_classname, base_classname, base_classname, base_classname))
