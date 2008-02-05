##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
"""Test setup helpers for non-doctests.
"""
import unittest
import re
import os.path
from zope.testing import doctest, cleanup
from zope.app.testing.functional import (
    HTTPCaller, getRootFolder, sync, ZCMLLayer, FunctionalDocFileSuite,
    FunctionalTestSetup)
from martian.scan import module_info_from_dotted_name
from z3c.testsetup.base import BasicTestSetup
from z3c.testsetup.util import get_package
from z3c.testsetup.doctesting import _collect_tests

class UnitTestSetup(BasicTestSetup):
    """A unit test setup for packages.

    A collection of methods to search for appropriate modules in
    a given package. ``UnitTestSetup`` is also able to 'register' the
    tests found and to deliver them as a ready-to-use
    ``unittest.TestSuite`` instance.

    While the functionality to search for testfiles is mostly
    inherited from the base class, the focus here is to setup the
    tests correctly.

    See file `unittestsetup.py` in the tests/testsetup directory to
    learn more about ``UnitTestSetup``.
    """

    regexp_list = [
        '^\s*:(T|t)est-(L|l)ayer:\s*(python)\s*',
        ]

    def __init__(self, package, filter_func=None):
        BasicTestSetup.__init__(self, package)
        self.filter_func = filter_func or self.isTestModule

    def docstrContains(self, docstr, regexp_list):
        """Does a docstring contain lines matching every of the regular
        expressions?
        """
        found_list = []
        if docstr is None:
            return False
        for line in docstr.split('\n'):
            for regexp in regexp_list:
                if re.compile(regexp).match(line) and (
                    regexp not in found_list):
                    found_list.append(regexp)
            if len(regexp_list) == len(found_list):
                break
        return len(regexp_list) == len(found_list)

    def isTestModule(self, module):
        """Return ``True`` if a module matches our expectations for a
        test file.

        This is the case if it got a module docstring which matches
        each of our regular expressions.
        """
        docstr = getattr(module, '__doc__', '')
        if not self.docstrContains(docstr, self.regexp_list):
            return False
        return True

    def getModules(self, package=None):
        result = []
        if package is None:
            package = self.package
        info = module_info_from_dotted_name(package.__name__)
        for submod_info in info.getSubModuleInfos():
            if submod_info.isPackage():
                result.extend(self.getModules(submod_info.getModule()))
            else:
                module = submod_info.getModule()
                if self.filter_func(module):
                    result.append(module)
        return result
        

    def getTestSuite(self):
        modules = self.getModules(package=self.package)
        suite = unittest.TestSuite()
        for module in modules:
            tests = unittest.defaultTestLoader.loadTestsFromModule(module)
            suite.addTest(tests)
        return suite

def get_pytests_suite(pkg_or_dotted_name, *args, **kwargs):
    kws = ['pfilter_func',]
    options = kwargs.copy()
    for optname in ['filter_func', 'extensions']:
        if optname in kwargs.keys():
            del (options[optname])
    return _collect_tests(pkg_or_dotted_name, UnitTestSetup,
                          typespec_kws=kws, *args, **options)


def register_pytests(pkg_or_dotted_name, *args, **kwargs):
    """Return a function that requires no argument and delivers a test
    suite.

    The resulting functions are suitable for use with unittest
    testrunners, that look for an attribute `test_suite` on module
    level. Such::

       test_suite = register_pytests(pkg)

    in a module should register all tests for the package `pkg`.
    """
    pkg = get_package(pkg_or_dotted_name)
    def tmpfunc():
        return get_pytests_suite(pkg, *args, **kwargs)
    return tmpfunc
    
