"""Calling super with wrong function name

"""
# Python Imports
import os
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters


class SuperFunction(filters.LineListener):
    """Check for the using super in functions
     super function name should match with current scope
    """

    subscribe_to = [filters.BeginFunctionBroadcaster, 
                    filters.EndFunctionBroadcaster,
                    filters.TestLineBroadcaster,
                    filters.UVCLineBroadcaster]

    super_re = re.compile(r"^\s*super\.([^ ]+)\(.*")

    class svfunction(object):
        def __init__(self, name, begin_line_no, begin_line):
            self.name = name
            self.begin_line_no = begin_line_no
            self.begin_line = begin_line
    
    def __init__(self, filename, fstream, *args, **kwargs):
        super(SuperFunction, self).__init__(filename, fstream, *args, **kwargs)
        self.sv_functions = []
        self.current_func = None
        self.eof_called = False

    def update_beginfunction(self, line_no, line, match):
         self.current_func = self.svfunction(match.group('name'), line_no, line)

    def update_endfunction(self, line_no, line, match):
        if self.current_func is None:
            self.error(line_no, line, "Saw endfunction before function definition")
            return
        self.current_func.end_line_no = line_no
        self.sv_functions.append(self.current_func)
        self.current_func = None

    def eof(self):
        if self.eof_called:
            return
        self.eof_called = True

    def _update(self, line_no, line):
        if not self.current_func == None:
             supermatch = self.super_re.search(line)
             if supermatch:
                 if not self.current_func.name == supermatch.group(1):
                     self.error(line_no, line, "Super called with {}, but not matching current function name: {}".format(supermatch.group(1), self.current_func.name))
            
    update_uvcline = _update
    update_testline = _update
