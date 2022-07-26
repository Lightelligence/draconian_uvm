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
    subscribe_to = [filters.TestbenchTopLineBroadcaster, filters.TestLineBroadcaster, filters.UVCLineBroadcaster]

    covgroup_re = re.compile(r"^\s*covergroup\s+([^ ]+).*;")

    def _update(self, line_no, line):
        match = self.covgroup_re.search(line)
        if match:
            if not match.group(1).endswith("_cg"):
                if not match.group(1) == 'cg':
                    self.error(line_no, line,
                               "Coverage group name not ending with _cg instead ({}).".format(match.group(1)))

    update_testbenchtopline = _update
    update_testline = _update
    update_uvcline = _update
