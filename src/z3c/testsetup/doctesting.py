##############################################################################
#
# Copyright (c) 2007-2008 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Test setup helpers for doctests.
"""
import unittest
import os.path
from zope.testing import doctest, cleanup
from z3c.testsetup.base import BasicTestSetup
from z3c.testsetup.util import get_package, get_marker_from_file

class DocTestSetup(BasicTestSetup):
    """A test setup for doctests."""

    globs = {}

    optionflags = (doctest.ELLIPSIS+
                   doctest.NORMALIZE_WHITESPACE+
                   doctest.REPORT_NDIFF)

    encoding = 'utf-8'

    def __init__(self, package, setup=None, teardown=None, globs=None,
                 optionflags=None, encoding=None, **kw):
        BasicTestSetup.__init__(self, package, **kw)
        self.setUp = setup or self.setUp
        self.tearDown = teardown or self.tearDown
        self.encoding = encoding or self.encoding
        if globs is not None:
            self.globs = globs
        if optionflags is not None:
            self.optionflags = optionflags
        

class UnitDocTestSetup(DocTestSetup):
    """A unit test setup for packages.

    A collection of methods to search for appropriate doctest files in
    a given package. ``UnitTestSetup`` is also able to 'register' the
    tests found and to deliver them as a ready-to-use
    ``unittest.TestSuite`` instance.

    While the functionality to search for testfiles is mostly
    inherited from the base class, the focus here is to setup the
    tests correctly.

    See file `unittestsetup.py` in the tests/testsetup directory to
    learn more about ``UnitTestSetup``.
    """

    optionflags = (doctest.ELLIPSIS+
                   doctest.NORMALIZE_WHITESPACE+
                   doctest.REPORT_NDIFF)

    regexp_list = [
        '^\s*:(T|t)est-(L|l)ayer:\s*(unit)\s*',
        ]

    globs = dict()

    def setUp(self, test):
        pass

    def tearDown(self, test):
        cleanup.cleanUp()

    def getTestSuite(self):
        docfiles = self.getDocTestFiles(package=self.package)
        suite = unittest.TestSuite()
        for name in docfiles:
            layerdef = get_marker_from_file('Test-Layerdef', name)
            if os.path.isabs(name):
                # We get absolute pathnames, but we need relative ones...
                common_prefix = os.path.commonprefix([self.package.__file__,
                                                      name])
                name = name[len(common_prefix):]
            test = doctest.DocFileSuite(
                name,
                package=self.package,
                setUp=self.setUp,
                tearDown=self.tearDown,
                globs=self.globs,
                optionflags=self.optionflags,
                **self.additional_options
                )
            if layerdef is not None:
                test.layer = layerdef
            suite.addTest(test)
        return suite
