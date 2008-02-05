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

    globs = dict()

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
                globs=self.globs,
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

    checker = None

    param_list = BasicTestSetup.param_list + ['globs', 'setup', 'teardown',
                                              'optionflags', 'checker',
                                              'zcml_config', 'layer_name',
                                              'layer', 'encoding']

    def __init__(self, package, filter_func=None, extensions=None,
                 regexp_list=None, globs=None, setup=None, teardown=None,
                 optionflags=None, checker=None, zcml_config = None,
                 layer_name='FunctionalLayer', layer=None, encoding='utf-8',
                 **kw):
        BasicTestSetup.__init__(self, package, filter_func=filter_func,
                       extensions=extensions)
        self.checker = checker
        self.encoding = encoding
        # Setup a new layer if specified in params...
        if zcml_config is not None and layer is None:
            if not os.path.isfile(zcml_config):
                zcml_config = os.path.join(
                    os.path.dirname(self.package.__file__),
                    zcml_config)
            self.layer = ZCMLLayer(zcml_config, self.package.__name__,
                                   layer_name)
        # Passing a ready-for-use layer overrides layer specified by
        # zcml_config...
        if layer is not None:
            self.layer = layer
        return
        
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
            encoding=self.encoding,
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

def _collect_tests(pkg_or_dotted_name, setup_type,
                   typespec_kws=[], *args, **kwargs):
    pkg = get_package(pkg_or_dotted_name)
    options = kwargs.copy()
    for kw in typespec_kws:
        if kw in kwargs.keys():
            options[kw[1:]] = kwargs[kw]
            del options[kw]
    for kw in options.copy().keys():
        if kw not in setup_type.param_list:
            del options[kw]
    return setup_type(pkg, *args, **options).getTestSuite()
    

def get_unitdoctests_suite(pkg_or_dotted_name, *args, **kwargs):
    kws = ['ufilter_func', 'uextensions',
           'uglobs', 'uoptionflags', 'usetup', 'uteardown']
    return _collect_tests(pkg_or_dotted_name, UnitDocTestSetup,
                          typespec_kws=kws, *args, **kwargs)

def get_functionaldoctests_suite(pkg_or_dotted_name, *args, **kwargs):
    kws = ['ffilter_func', 'fextensions',
           'fglobs', 'foptionflags', 'fsetup', 'fteardown']
    return _collect_tests(pkg_or_dotted_name, FunctionalDocTestSetup,
                          typespec_kws=kws, *args, **kwargs)

def get_doctests_suite(pkg_or_dotted_name, *args, **kwargs):
    pkg = get_package(pkg_or_dotted_name)
    suite = unittest.TestSuite()
    suite.addTest(
        get_unitdoctests_suite(pkg, *args, **kwargs))
    suite.addTest(
        get_functionaldoctests_suite(pkg, *args, **kwargs))
    return suite

def register_doctests(pkg_or_dotted_name, *args, **kwargs):
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
        return get_doctests_suite(pkg, *args, **kwargs)
    return tmpfunc
    
