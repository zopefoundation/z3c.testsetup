# -*- coding: utf-8 -*-
""" Tests for `z3c.testsetup.util`.

Most of `z3c.testsetup.util` helper functions are tested in doctest
files called ``util.txt`` (yes, there are two of them). As this kind of
doctesting is a hell to debug and (in times of Sphinx) even not very
useful for documentation, we write down new tests in Python.
"""
import os
import shutil
import tempfile
import unittest
from z3c.testsetup.util import (
    got_working_zope_app_testing, get_keyword_params, get_marker_from_file)


class TestUtil(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.workdir)

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

    def test_get_marker_from_file(self):
        # we can find markers in files
        path = os.path.join(self.workdir, "myfile")
        content = "Some text\n :TeSt-lAyEr:   foo \n\nSome other text\n"
        with open(path, "w") as fd:
            fd.write(content)
        result = get_marker_from_file("test-layer", path)
        self.assertEqual(result, "foo")

    def test_get_marker_from_file_utf8(self):
        #  we can get markers from files with non-ascii encodings
        path = os.path.join(self.workdir, "myfile")
        content = u"Line1\n :some-layer:   foo \n Umlauts: äöü\n"
        content = content.encode("utf-8")  # transform to binary stream
        with open(path, "wb") as fd:
            fd.write(content)
        result = get_marker_from_file("some-layer", path)
        self.assertEqual(result, "foo")

    def test_get_marker_from_file_non_utf8(self):
        # even files incompatible with UTF-8 can be parsed
        path = os.path.join(self.workdir, "myfile")
        content = b"Line1\n :some-layer:   foo \n Strange: \xff\xfeW[ \n"
        with open(path, "wb") as fd:
            fd.write(content)
        result = get_marker_from_file("some-layer", path)
        self.assertEqual(result, "foo")
