"""Instance naming schema
   Instance name should hint the instance type.
"""
# Python Imports
import os
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters

class InstancenameSchema(filters.LineListener):
    """Check for the naming of uvm_component/uvm_object instance
     UVM components/objects's instance hash table for naming schema
    """

    subscribe_to = [filters.TestbenchTopLineBroadcaster,
                    filters.UVCLineBroadcaster,
                    filters.TestLineBroadcaster,]

    classname_re = re.compile(r"^\s*(uvm_analysis_port|uvm_event|uvm_analysis_imp).* (.*[^ ])\s*;")

    thisdict = {
        "uvm_analysis_port": "ap",
        "uvm_analysis_imp" : "imp",
        "uvm_event" : "event"
    }

    def _update(self, line_no, line):
        match = self.classname_re.search(line)
        if match:
            classname = match.group(1)
            instancename = match.group(2)
            if classname in self.thisdict:
                if not instancename.endswith(self.thisdict[classname]):
                   self.error(line_no, line, "Instance name '{}' not ending with '{}'. Recommend using suffix '{}' as instance name for '{}'".format(instancename, self.thisdict[classname], self.thisdict[classname], classname))


    update_testbenchtopline = _update
    update_testline = _update
    update_uvcline = _update
