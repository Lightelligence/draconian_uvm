"""Catch misleading print statemtents."""

# Python Imports
import re
# Lintwork Imports
# Draconian UVM imports
from . import filters

class MisleadingSformat(filters.LineListener):
    """Catch misleading print statemetns.
    
    Given the nature of the work, messages are frequently printed in different
    bases. However, this leads to situations where one may think a number is
    printing in hexidecimal, but is actually printing in binary.

    This check looks for mismatching identifiers.

    """
    subscribe_to = [filters.TestbenchTopLineBroadcaster,
                    filters.TestLineBroadcaster,
                    filters.UVCLineBroadcaster]

    sformatf_re = re.compile(r"\$sformatf\(.*((0([xXdDbB]))|('([hdb])))%([-0-9]*([xXdDbB]))")
    
    def _update(self, line_no, line):
        match = self.sformatf_re.search(line)
        if match:
            if match.group(2):
                representation = match.group(3).lower()
            else:
                representation = match.group(5).lower()
            if representation == 'h':
                representation = 'x'
            format_specifier = match.group(7).lower()
            if representation != format_specifier:
                self.error(line_no, line, "Representation ({}) and format specifier ({}) have mismatching bases.".format(match.group(1), match.group(6)))
            

    update_testbenchtopline = _update
    update_testline = _update
    update_uvcline = _update

    def error(self, line_no, line, message):
        # FIXME implement
        pass
