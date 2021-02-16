"""

"""
# Python Imports
import os
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters


class MultipleClasses(filters.LineListener):
    """In general, each class should be in its own file.

    There are two main reasons to keep each class in its own file:
      1. Readability
         Files remain a reasonable size.
      2. Navigation
         If a class name matches its filename, its defintion can be found intuitively.

    There are several common patterns that lead to exceptions in this policy.
      1. "helper" classes act as data structure encapsulation for another class should live alongside that class.
        a. The "helper" class should only be referenced by the primary class in the file in which it resides
        b. The "helper" class should be relatively small
      2. Sequence libraries by definition have multiple class definitions.
         They are exempt from this rule.
    """
    subscribe_to = [filters.BeginClassBroadcaster,
                    filters.EndClassBroadcaster]

    size_threshold = 100

    exempt_files_re = re.compile("_((vseq)|(seq)|(seq_lib))\.sv[h]?")

    class svclass(object):
        def __init__(self, name, begin_line_no, begin_line):
            self.name = name
            self.begin_line_no = begin_line_no
            self.begin_line = begin_line
            self.end_line_no = None
    

    def __init__(self, filename, fstream, *args, **kwargs):
        super(MultipleClasses, self).__init__(filename, fstream, *args, **kwargs)
        if self.exempt_files_re.search(filename):
            self.disable()
        self.sv_classes = []
        self.current_class = None
        self.eof_called = False

    def update_beginclass(self, line_no, line, match):
        self.current_class = self.svclass(match.group('name'), line_no, line)

    def update_endclass(self, line_no, line, match):
        if self.current_class is None:
            self.error(line_no, line, "Saw endclass before class definition")
            return
        self.current_class.end_line_no = line_no
        self.sv_classes.append(self.current_class)
        self.current_class = None

    def eof(self):
        if self.eof_called:
            return
        self.eof_called = True

        if len(self.sv_classes) <= 1:
            return
        
        file_base_name = os.path.splitext(os.path.basename(self.filename))[0]
        class_name_regex = re.compile("(.*)_c")
        primary_c = None

        for c in self.sv_classes:
            match = class_name_regex.search(c.name)
            if match:
                class_base_name = match.group(1)
            else:
                class_base_name = c.name

            if class_base_name in file_base_name:
                # Primary class in file, allowed to be large
                primary_c = c
            else:
                size = c.end_line_no - c.begin_line_no
                if size > self.size_threshold:
                    self.error(c.begin_line_no, c.begin_line, "class {} looks like a 'helper' class, but exceeds {} lines. It deserves its own file.".format(c.name, self.size_threshold))



        
            

    
