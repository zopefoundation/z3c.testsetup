""" Tests for `z3c.testsetup.util`.

Most of `z3c.testsetup.util` helper functions are tested in doctest
files called ``util.txt`` (yes, there are two of them). As this kind of
doctesting is a hell to debug and (in times of Sphinx) even not very
useful for documentation, we write down new tests in Python.
"""
import unittest
from z3c.testsetup.util import (
    got_working_zope_app_testing, get_keyword_params)


class TestUtil(unittest.TestCase):

    def test_got_working_zope_app_testing(self):
        # we can generally determine whether zope.app.testing is useable
        result = got_working_zope_app_testing()
        assert (result is True) or (result is False)

    def test_get_keyword_params(self):
        # we can get keyword parameters from methods
        class Foo(object):
            def bar(self, bar, baz="quix", bur="wer"):
                pass
        params = get_keyword_params(Foo, "bar")
        self.assertEqual(sorted(params), ["baz", "bur"])

    def test_get_keyword_params_wo_defaults(self):
        # we can get a list of keyword params if no defaults are defined
        class Foo(object):
            def bar(self):
                pass

            @classmethod
            def baz(cls):
                pass

        self.assertEqual(get_keyword_params(Foo, "bar"), [])
        self.assertEqual(get_keyword_params(Foo, "baz"), [])

    def test_get_keyword_params_w_varkw(self):
        # we can get a list of keyword params also if variable keywords
        # (`**kw`) are allowed.
        class Foo(object):
            def foo(self, bar="baz", **kw):
                pass

        self.assertEqual(get_keyword_params(Foo, "foo"), ["bar"])

    def test_get_keyword_params_inherited(self):
        # we can get inherited params.
        class Foo(object):
            def foo(self, foo="foo"):
                pass

        class Bar(Foo):
            def foo(self, bar="bar", **kw):
                pass

        class Baz(Bar):
            def foo(self, baz="baz", *args):
                pass

        self.assertEqual(
            sorted(get_keyword_params(Bar, "foo")), ["bar", "foo"])
        self.assertEqual(
            sorted(get_keyword_params(Baz, "foo")), ["baz"])
