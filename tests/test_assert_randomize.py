import unittest
from unittest import mock
from io import StringIO

from duvm import filters
from duvm.assert_randomize import AssertRandomize

import test

lbc = filters.LineBroadcaster

class AssertRandomizeTestCase(test.TestCase):

    cut = AssertRandomize

    def test_no_randomizations(self):
        """No randomizations here."""
        content = StringIO("""
        some other content
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_randomize(self):
        """Randomize call without wrapping should fail."""
        content = StringIO("""
        cfg.randomize();
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Randomize call was not wrapped with a `cmn_assert or `cmn_fassert.")

    def test_randomize_with(self):
        """Randomize call without wrapping should fail (adding with block)"""
        content = StringIO("""
        cfg.randomize() with { period_ps == 1000};
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Randomize call was not wrapped with a `cmn_assert or `cmn_fassert.")

    def test_randomize_wrapped(self):
        """Randomize call is wrapped correctly with cmn_assert"""
        content = StringIO("""
        `cmn_assert(cfg.randomize());
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_randomize_wrapped_with(self):
        """Randomize call with with statement is wrapped correctly with cmn_assert."""
        content = StringIO("""
        `cmn_assert(cfg.randomize() with { period_ps == 1000});
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

    def test_std(self):
        """Randomize call without wrapping should fail (adding with block)"""
        content = StringIO("""
        std::randomize(seed);
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_called_with(mock.ANY, mock.ANY, mock.ANY, "Randomize call was not wrapped with a `cmn_assert or `cmn_fassert.")

    def test_comment_ok(self):
        """Commented out case"""
        content = StringIO("""
        // `cmn_assert(std::randomize(seed))
        """)
        with mock.patch.object(self.cut, "error", autospec=True):
            lb = lbc("/tests/base_test.sv", content, parent=None, gc=None, restrictions=self.build_restriction_filter(self.cut))
            iut = self.get_listener(lb, self.cut)
            iut.error.assert_not_called()

if __name__ == '__main__':
    unittest.main()
