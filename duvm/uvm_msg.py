"""Ban using uvm_* message macros in favor of cmn_*

"""
# Python Imports
import re
# Lintwork Imports
# Draconian UVM imports
from duvm import filters


class UvmMsg(filters.LineListener):
    """Ban using of uvm msg 

    instead should use cmn_msgs.
    """
    subscribe_to = [filters.TestbenchTopLineBroadcaster, filters.TestLineBroadcaster, filters.UVCLineBroadcaster]

    uvmmsg_re = re.compile(r"^\s*`uvm\_((info)|(debug)|(warning)|(error)|(fatal))\(")
    verbose_re = re.compile(r"UVM\_(.*)\)")

    def _update(self, line_no, line):
        match = self.uvmmsg_re.search(line)
        if match:
            uvmmacrotype = match.group(1)
            if (uvmmacrotype == 'info'):
                verbose_match = self.verbose_re.search(line)
                if verbose_match:
                    uvmverbose_type = verbose_match.group(1)
                    if (uvmverbose_type == 'LOW'):
                        self.error(
                            line_no, line,
                            "Usage of uvm_{} is not recommended, please use cmn_info() or cmn_dbg() instead.".format(
                                match.group(1)))
                    else:
                        self.error(
                            line_no, line,
                            "Usage of uvm_{} is not recommended, please use cmn_dbg() instead.".format(match.group(1)))
                else:
                    self.error(
                        line_no, line,
                        "Usage of uvm_{} is not recommended, please use cmn_info() instead.".format(match.group(1)))
            elif (uvmmacrotype == 'warning'):
                self.error(line_no, line,
                           "Usage of uvm_{} is not recommended, please use cmn_warn() instead.".format(match.group(1)))
            elif (uvmmacrotype == 'error'):
                self.error(line_no, line,
                           "Usage of uvm_{} is not recommended, please use cmn_err() instead.".format(match.group(1)))
            elif (uvmmacrotype == 'fatal'):
                self.error(line_no, line,
                           "Usage of uvm_{} is not recommended, please use cmn_fatal() instead.".format(match.group(1)))

    update_testbenchtopline = _update
    update_testline = _update
    update_uvcline = _update
