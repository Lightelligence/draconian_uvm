"""Calling super with wrong function name

"""
# Python Imports
import os
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters


class SuperFuncTask(filters.LineListener):
    """Check for the using super in functions
     super function name should match with current scope
    """

    subscribe_to = [filters.BeginFunctionBroadcaster, 
                    filters.EndFunctionBroadcaster,
                    filters.BeginTaskBroadcaster, 
                    filters.EndTaskBroadcaster,
                    filters.TestLineBroadcaster,
                    filters.UVCLineBroadcaster]

    super_re = re.compile(r"^\s*super\.([^ ]+)\(.*")
    scopedname_re = re.compile(r"::\s*([^ \#]+)")

    class svfunction(object):
        def __init__(self, name, begin_line_no, begin_line):
            self.name = name
            self.begin_line_no = begin_line_no
            self.begin_line = begin_line

    class svtask(object):
        def __init__(self, name, begin_line_no, begin_line):
            self.name = name
            self.begin_line_no = begin_line_no
            self.begin_line = begin_line
    
    def __init__(self, filename, fstream, *args, **kwargs):
        super(SuperFuncTask, self).__init__(filename, fstream, *args, **kwargs)
        self.sv_functions = []
        self.sv_tasks = []
        self.current_func = None
        self.current_task = None
        self.eof_called = False

    def update_beginfunction(self, line_no, line, match):
        func_name = match.group('name')
        scopename_match = self.scopedname_re.search(func_name)
        if scopename_match:
            func_name = scopename_match.group(1)

        self.current_func = self.svfunction(func_name, line_no, line)

    def update_endfunction(self, line_no, line, match):
        if self.current_func is None:
            self.error(line_no, line, "Saw endfunction before function definition")
            return
        self.current_func.end_line_no = line_no
        self.sv_functions.append(self.current_func)
        self.current_func = None

    def update_begintask(self, line_no, line, match):
        task_name = match.group('name')
        scopename_match = self.scopedname_re.search(task_name)
        if scopename_match:
            task_name = scopename_match.group(1)

        self.current_task = self.svtask(task_name, line_no, line)

    def update_endtask(self, line_no, line, match):
        if self.current_task is None:
            self.error(line_no, line, "Saw endtask before task definition")
            return
        self.current_task.end_line_no = line_no
        self.sv_tasks.append(self.current_task)
        self.current_task = None

    def eof(self):
        if self.eof_called:
            return
        self.eof_called = True

    def _update(self, line_no, line):
        supermatch = self.super_re.search(line)
        if supermatch:
            if not self.current_func == None:
                if not self.current_func.name == supermatch.group(1):
                    self.error(line_no, line, "Super called with {}, but not matching current function name: {}".format(supermatch.group(1), self.current_func.name))
            elif not self.current_task == None:
                if not self.current_task.name == supermatch.group(1):
                    self.error(line_no, line, "Super called with {}, but not matching current task name: {}".format(supermatch.group(1), self.current_task.name))

    update_uvcline = _update
    update_testline = _update
