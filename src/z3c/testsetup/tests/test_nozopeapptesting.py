import unittest
import z3c.testsetup
from z3c.testsetup.util import got_working_zope_app_testing


class TestNoZopeAppTesting(unittest.TestCase):
    # If zope.app.testing is not working/available, we get different sets
    # of testgetters: functional ones rely on zope.app.testing and are
    # excluded.
    #
    # In a test we would like to check that, but we have to provide
    # zope.app.testing then (which is not working for Python 3 at the
    # time of writing) and have to fiddle around with sys.modules then.
    # This has too many unwanted side effects.
    #
    # To sum it up: as long as we cannot rely on zope.app.testing being
    # available during tests, we disable most getter tests here.

    def test_getter_number(self):
        # we get 4 testgetters with zope.app.testing avail. (3 else)
        getters = z3c.testsetup.TestCollector.handled_getters
        if got_working_zope_app_testing():
            assert len(getters) == 4
        else:
            assert len(getters) == 3
