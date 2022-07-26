import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.dollar_display import DollarDisplay

import test

lbc = filters.LineBroadcaster


class DollarDisplayTestCase(test.TestCase):

    cut = DollarDisplay

    def test_no_display(self):
        """No $display here."""
        content = StringIO("""
        some other content
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_display(self):
        """$display here."""
        content = StringIO("""
        $display("Some unconditional message");
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv",
                     content,
                     parent=None,
                     gc=None,
                     restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Do not use $display. Use `uvm_info instead.")


if __name__ == '__main__':
    unittest.main()
