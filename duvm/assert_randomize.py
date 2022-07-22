"""Check for assertions wrapping randomize calls.

"""
# Python Imports
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters


class AssertRandomize(filters.LineListener):
    """Check for assertions wrapping randomize calls.

    Quickly fail the test if randomization fails.
    """
    subscribe_to = [filters.TestbenchTopLineBroadcaster, filters.TestLineBroadcaster, filters.UVCLineBroadcaster]

    randomize_re = re.compile("(((\.)|(std::))randomize)\(")
    assert_re = re.compile("^\s*(//)*\s*`cmn_assert\(")

    def _update(self, line_no, line):
        if self.randomize_re.search(line):
            if not self.assert_re.search(line):
                self.error(line_no, line, "Randomize call was not wrapped with a `cmn_assert.")

    update_testbenchtopline = _update
    update_testline = _update
    update_uvcline = _update
