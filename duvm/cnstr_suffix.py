"""Constraint instances shall end with suffix '_cnstr'

"""
# Python Imports
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters

class CnstrSuffix(filters.LineListener):
    """Constraint instance always with suffix _cnstr
    """
    subscribe_to = [filters.TestbenchTopLineBroadcaster,
                    filters.TestLineBroadcaster,
                    filters.UVCLineBroadcaster]

    covgroup_re = re.compile(r"^\s*constraint(.*)\{")

    def _update(self, line_no, line):
        match = self.covgroup_re.search(line)
        if match:
            constraint_str = match.group(1).strip()
            if not constraint_str.endswith("_cnstr"):
                    self.error(line_no, line, "Constraint name not ending with _cnstr instead ({}).".format(constraint_str))

    update_testbenchtopline = _update
    update_testline = _update
    update_uvcline = _update

