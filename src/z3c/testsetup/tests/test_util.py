""" Tests for `z3c.testsetup.util`.

Most of `z3c.testsetup.util` helper functions are tested in doctest
files called ``util.txt`` (yes, there are two of them). As this kind of
doctesting is a hell to debug and (in times of Sphinx) even not very
useful for documentation, we write down new tests in Python.
"""
import unittest
from z3c.testsetup.util import got_working_zope_app_testing


class TestUtil(unittest.TestCase):

    def test_got_working_zope_app_testing(self):
        # we can generally determine whether zope.app.testing is useable
        result = got_working_zope_app_testing()
        assert (result is True) or (result is False)
