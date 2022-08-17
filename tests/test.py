import unittest
import lw


class TestCase(unittest.TestCase):

    # Class under test
    cut = None

    def build_restriction_filter(self, *args):
        mock_class_filter = set()
        for cls in args:
            mock_class_filter.add(cls)
            try:
                for subscription in cls.subscribe_to:
                    mock_class_filter.add(subscription)
                    mock_class_filter.update(self.build_restriction_filter(subscription))
            except AttributeError:
                pass
        return mock_class_filter

    def get_listener(self, broadcaster, listener_type):
        for listener in broadcaster.listener_instances:
            if isinstance(listener, listener_type):
                return listener
            if isinstance(listener, lw.base.Broadcaster):
                gl = self.get_listener(listener, listener_type)
                if gl:
                    return gl
        return None
