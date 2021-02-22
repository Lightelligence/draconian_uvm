"""Top level filters to categorizes rules to file types.

"""

import os
import re
import glob

from lw import linebase as lb
from lw import base as lw

class LineBroadcaster(lb.LineBroadcaster):
    pass

class LineListener(lb.LineListener):
    pass


class TestbenchTopLineBroadcaster(lw.Broadcaster, lw.Listener):
    subscribe_to = [LineBroadcaster]

    # Naming conventions frequently used for Testbench Top files
    filename_filter_re = re.compile("(_tb_top\.)|"
                                    "(_sim_top\.)")

    def __init__(self, filename, fstream, *args, **kwargs):
        super(TestbenchTopLineBroadcaster, self).__init__(filename, fstream, *args, **kwargs)
        if not self.filename_filter_re.search(filename):
            self._ignore(LineBroadcaster)
    
    def update_line(self, line_no, line):
        self.broadcast(line_no, line)
        
    def eof(self):
        self._broadcast("eof")


class TestLineBroadcaster(lw.Broadcaster, lw.Listener):
    subscribe_to = [LineBroadcaster]

    # Naming conventions frequently used tests directory
    filename_filter_re = re.compile("/tests/.*sv")

    def __init__(self, filename, fstream, *args, **kwargs):
        super(TestLineBroadcaster, self).__init__(filename, fstream, *args, **kwargs)
        if not self.filename_filter_re.search(filename):
            self._ignore(LineBroadcaster)
    
    def update_line(self, line_no, line):
        self.broadcast(line_no, line)
        
    def eof(self):
        self._broadcast("eof")


class UVCLineBroadcaster(lw.Broadcaster, lw.Listener):
    subscribe_to = [LineBroadcaster]

    memoized_directories = {}

    def __init__(self, filename, fstream, *args, **kwargs):
        super(UVCLineBroadcaster, self).__init__(filename, fstream, *args, **kwargs)
        dirname = os.path.dirname(filename)
        try:
            inside_uvc = self.memoized_directories[dirname]
        except KeyError:
            inside_uvc = False

            dir_files = glob.glob(os.path.join(dirname, "*pkg.sv"))  + glob.glob(os.path.join(dirname, "../","*pkg.sv"))
            if len(dir_files):
                inside_uvc = True

            self.memoized_directories[dirname] = inside_uvc
        if not inside_uvc:
            self._ignore(LineBroadcaster)

    def update_line(self, line_no, line):
        self.broadcast(line_no, line)
            
    def eof(self):
        self._broadcast("eof")


class BeginClassBroadcaster(lw.Broadcaster, lw.Listener):
    subscribe_to = [LineBroadcaster]
    
    begin_class_re = re.compile("^\s*(?P<virtual>virtual){0,1}\s*class\s+(?P<name>[^\s#]+)\s*(?P<params>#\(.*?\)){0,1}(\s+extends\s+(?P<base>[^\s#]+)){0,1}\s*(?P<baseparams>#\(.*?\)){0,1}\s*;")

    def update_line(self, line_no, line):
        match = self.begin_class_re.search(line)
        if match:
            self.broadcast(line_no, line, match)

    def eof(self):
        self._broadcast("eof")


class EndClassBroadcaster(lw.Broadcaster, lw.Listener):
    subscribe_to = [LineBroadcaster]
    
    end_class_re = re.compile("^\s*endclass")

    def update_line(self, line_no, line):
        match = self.end_class_re.search(line)
        if match:
            self.broadcast(line_no, line, match)
    
    def eof(self):
        self._broadcast("eof")
