"""Coverage instance always with suffix _cg

"""
# Python Imports
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters

class CoverageSuffix(filters.LineListener):
    """Coverage instance always with suffix _cg
    """
    subscribe_to = [filters.TestbenchTopLineBroadcaster,
                    filters.TestLineBroadcaster,
                    filters.UVCLineBroadcaster]

    covgroup_re = re.compile(r"^\s*covergroup(.*)\;")

    def _update(self, line_no, line):
        match = self.covgroup_re.search(line)
        if match:
            covname_str = match.group(1).split( )
            if covname_str[0]:
                if not covname_str[0].endswith("_cg"):
                    if not covname_str[0] == 'cg':
                        self.error(line_no, line, "Coverage group name not ending with _cg instead ({}).".format(covname_str[0]))
                    
    update_testbenchtopline = _update
    update_testline = _update
    update_uvcline = _update

