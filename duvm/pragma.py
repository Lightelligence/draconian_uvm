"""Allow waivers of rules via inline pragmas.

"""
# Python Imports
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters

class Pragma(filters.LineListener):
    """
    """
    subscribe_to = [filters.LineBroadcaster]

    pragma_re = re.compile("//\s*duvm: (disable|enable)=(\S+)")

    def update_line(self, line_no, line):
        match = self.pragma_re.search(line)
        if match:
            # Find root
            root = self.parent
            while (root.parent):
                root = root.parent

            method_name = match.group(1)
            class_names = match.group(2).split(',')

            for cn in class_names:
                listener = root.get_listener(cn)
                if not listener:
                    # FIXME what happens if you have two different lintworks tools using pragmas?
                    # Pragmas from the other tool would throw this error
                    self.error(line_no, line, "could not find listener ({}) class used in pragma".format(cn))
                    continue
                getattr(listener, method_name)()
