"""Check all files for include guards.

"""
# Python Imports
import os
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters


class IncludeGuard(filters.LineListener):
    """Check for the presence of an include guard.
    Expecting:
      `ifndef __<FILENAME>__
        `define __<FILENAME>__
       ...   
      `endif // guard
    """
    subscribe_to = [filters.TestLineBroadcaster, filters.UVCLineBroadcaster]

    line_is_comment_or_empty_re = re.compile("^\s*((//.*)|())$")

    ifndef_re = re.compile("^\s*`ifndef\s+(\S+)")
    define_re = re.compile("^\s*`define\s+(\S+)")
    endif_re = re.compile("^\s*`endif(\s*//\s*(.*))")

    exempt_files_re = re.compile("_intf.sv[h]?")

    def __init__(self, filename, fstream, *args, **kwargs):
        super(IncludeGuard, self).__init__(filename, fstream, *args, **kwargs)
        self.filename = filename
        if self.exempt_files_re.search(filename):
            self.disable()
        self._in_first_comment = True
        self._looking_for_ifndef = False
        self._looking_for_define = False
        self._looking_for_endif = False
        self._guard_value = None
        self._endif_value = None
        self._saw_at_least_one_line = False
        self._in_block_comment = False

    def is_guard_value_legal(self):
        """Compare to see if the guard value is an expected format.

        Two commons patterns:
          __<FILENAME>
          __<FILENAME>__
        """
        filename_piece = re.sub("[^A-Z0-9_]", "_", os.path.basename(self.filename).upper())
        if self._guard_value in ["__{}".format(filename_piece), "__{}__".format(filename_piece)]:
            return True
        return False

    def _update(self, line_no, line):
        self._saw_at_least_one_line = True

        # TODO handle block comment
        if self._in_first_comment or self._in_block_comment:
            if self.line_is_comment_or_empty_re.search(line):
                return
            block_comment_start = re.search("/\*", line)
            if block_comment_start:
                self._in_block_comment = True
                if re.search("\*/", line[block_comment_start.end():]):
                    self._in_block_comment = False
                    return
            if self._in_block_comment:
                if re.search("\*/", line):
                    self._in_block_comment = False
                return
            self._in_first_comment = False
            self._looking_for_ifndef = True

        if self._looking_for_ifndef:
            match = self.ifndef_re.search(line)
            if match:
                self._guard_value = match.group(1)
                if not self.is_guard_value_legal():
                    self.error(line_no, line, "The include guard doesn't match expected format.")
                self._looking_for_ifndef = False
                self._looking_for_define = True
            else:
                self.error(
                    line_no, line,
                    "Expected an include guard `ifndef directive in the first non-comment, non-blank line of the file.")
            return

        if self._looking_for_define:
            match = self.define_re.search(line)
            if match:
                if match.group(1) != self._guard_value:
                    self.error(
                        line_no, line, "Include guard ifndef '{}' and define '{}' do not match.".format(
                            self._guard_value, match.group(1)))
                self._looking_for_define = False
                self._looking_for_endif = True
            else:
                self.error(line_no, line, "Did not find define on line immediately following indef")
            return

        if self._looking_for_endif:
            # Could hit other endif that are not part of the guard, so just keep recording until the end of file
            # TODO actually count ifdef/else/endif to find guard endif more precisely
            match = self.endif_re.search(line)
            if match:
                self._endif_value = match.group(2)

    def eof(self):
        if not self._saw_at_least_one_line:
            return
        if self._looking_for_ifndef:
            self.error(
                None, None,
                "Expected an include guard `ifndef directive in the first non-comment, non-blank line of the file.")
            return
        if self._looking_for_define:
            self.error(None, None, "Never saw matching define for include guard ifndef '{}'".format(self._guard_value))
            return
        if self._endif_value == None:
            self.error(None, None, "Never saw an endif for include guard '{}'".format(self._guard_value))
            return
        if self._endif_value not in ["guard", self._guard_value]:
            self.error(None, None,
                       "The endif comment for include guard '{0}' should be '{0}' or 'guard'".format(self._guard_value))

    def error(self, line_no, line, message):
        self.disable()
        self.update_testline = None
        self.update_uvcline = None
        self.eof = None # The errors in the eof step can be misleading if
        # previous errors have occurred.
        super(IncludeGuard, self).error(line_no, line, message)

    update_testline = _update
    update_uvcline = _update
