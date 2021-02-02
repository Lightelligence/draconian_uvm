"""Ban $display in favor of `uvm_info

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
    subscribe_to = [filters.TestbenchTopLineBroadcaster,
                    filters.TestLineBroadcaster,
                    filters.UVCLineBroadcaster]

    uvmmsg_re = re.compile(r"^\s*`uvm\_(.+?)\(")
    verbose_re = re.compile(r"UVM\_(.*)\)")

    def _update(self, line_no, line):
        match = self.uvmmsg_re.search(line)
        str = "fixme-hw:inside uvm_msg"
        #print(str)
        #print(line)
        if match:
            #print(match.group(1))
            uvmmacrotype = match.group(1)
            if (uvmmacrotype == 'info'):
                verbose_match = self.verbose_re.search(line)
                if verbose_match:
                    #print(verbose_match.group(1))
                    uvmverbose_type = verbose_match.group(1)
                    if (uvmverbose_type == 'LOW'):
                        self.error(line_no, line, "Usage of uvm_{} is not recommended, please use cmn_info() or cmn_dbg() instead.".format(match.group(1)))
                    else :
                        self.error(line_no, line, "Usage of uvm_{} is not recommended, please use cmn_dbg() instead.".format(match.group(1)))
                else :
                    self.error(line_no, line, "Usage of uvm_{} is not recommended, please use cmn_info() instead.".format(match.group(1)))

            if (uvmmacrotype == 'warning'):
                self.error(line_no, line, "Usage of uvm_{} is not recommended, please use cmn_warn() instead.".format(match.group(1)))

            if (uvmmacrotype == 'error'):
                self.error(line_no, line, "Usage of uvm_{} is not recommended, please use cmn_err() instead.".format(match.group(1)))

            if (uvmmacrotype == 'fatal'):
                self.error(line_no, line, "Usage of uvm_{} is not recommended, please use cmn_fatal() instead.".format(match.group(1)))



    update_testbenchtopline = _update
    update_testline = _update
    update_uvcline = _update

