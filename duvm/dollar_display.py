"""Ban $display in favor of `uvm_info

"""
# Python Imports
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters

class DollarDisplay(filters.LineListener):
    """Ban $display in favor of `uvm_info

    $display is an unconditional print.
    """
    subscribe_to = [filters.TestbenchTopLineBroadcaster,
                    filters.TestLineBroadcaster,
                    filters.UVCLineBroadcaster]

    display_re = re.compile("\$display")

    def _update(self, line_no, line):
        if self.display_re.search(line):
            self.error(line_no, line, "Do not use $display. Use `uvm_info instead.")

    update_testbenchtopline = _update
    update_testline = _update
    update_uvcline = _update
