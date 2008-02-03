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
from zope.app.testing.functional import (
    HTTPCaller, getRootFolder, sync, ZCMLLayer, FunctionalDocFileSuite,
    FunctionalTestSetup)
from z3c.testsetup.base import BasicTestSetup
from z3c.testsetup.util import get_package

class UnitDocTestSetup(BasicTestSetup):
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


    def tearDown(self, test):
        cleanup.cleanUp()

    def getTestSuite(self):
        docfiles = self.getDocTestFiles(package=self.package)
        suite = unittest.TestSuite()
        for name in docfiles:
            if os.path.isabs(name):
                # We get absolute pathnames, but we need relative ones...
                common_prefix = os.path.commonprefix([self.package.__file__,
                                                      name])
                name = name[len(common_prefix):]
            suite.addTest(
                doctest.DocFileSuite(
                name,
                package=self.package,
                setUp=self.setUp,
                tearDown=self.tearDown,
                optionflags=self.optionflags,
                **self.additional_options
                ))
        return suite


class FunctionalDocTestSetup(BasicTestSetup):
    """A functional test setup for packages.

    A collection of methods to search for appropriate doctest files in
    a given package. ``FunctionalTestSetup`` is also able to
    'register' the tests found and to deliver them as a ready-to-use
    ``unittest.TestSuite`` instance.

    While the functionality to search for testfiles is mostly
    inherited from the base class, the focus here is to setup the
    tests correctly.
    """
    ftesting_zcml = os.path.join(os.path.dirname(__file__),
                                 'ftesting.zcml')
    layer = ZCMLLayer(ftesting_zcml, __name__,
                      'FunctionalLayer')

    globs=dict(http=HTTPCaller(),
               getRootFolder=getRootFolder,
               sync=sync
               )

    optionflags = (doctest.ELLIPSIS+
                   doctest.NORMALIZE_WHITESPACE+
                   doctest.REPORT_NDIFF)

    regexp_list = [
        '^\s*:(T|t)est-(L|l)ayer:\s*(functional)\s*',
        ]

    def setUp(self, test):
        FunctionalTestSetup().setUp()

    def tearDown(self, test):
        FunctionalTestSetup().tearDown()

    def suiteFromFile(self, name):
        suite = unittest.TestSuite()
        if os.path.isabs(name):
            # We get absolute pathnames, but we need relative ones...
            common_prefix = os.path.commonprefix([self.package.__file__, name])
            name = name[len(common_prefix):]
        test = FunctionalDocFileSuite(
            name, package=self.package,
            setUp=self.setUp, tearDown=self.tearDown,
            globs=self.globs,
            optionflags=self.optionflags,
            **self.additional_options
            )
        test.layer = self.layer
        suite.addTest(test)
        return suite

    def getTestSuite(self):
        docfiles = self.getDocTestFiles(package=self.package)
        suite = unittest.TestSuite()
        for name in docfiles:
            suite.addTest(self.suiteFromFile(name))
        return suite

def collect_doctests(package, *args, **kwargs):
    suite = unittest.TestSuite()
    test = UnitDocTestSetup(package).getTestSuite()
    suite.addTests(
        UnitDocTestSetup(package).getTestSuite())
    suite.addTest(
        FunctionalDocTestSetup(package).getTestSuite())
    return suite

def register_doctests(pkg_or_dotted_name):
    """Return a function that requires no argument and delivers a test
    suite.

    The resulting functions are suitable for use with unittest
    testrunners, that look for an attribute `test_suite` on module
    level. Such::

       test_suite = register_doctests(pkg)

    in a module should register all tests for the package `pkg`.
    """
    pkg = get_package(pkg_or_dotted_name)
    def tmpfunc():
        return collect_doctests(pkg)
    return tmpfunc
    
