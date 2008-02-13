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
"""Factories for testcollectors.
"""
import unittest
from z3c.testsetup.doctesting import UnitDocTestSetup, FunctionalDocTestSetup
from z3c.testsetup.testing import UnitTestSetup
from z3c.testsetup.util import get_package, get_keyword_params

class BasicTestGetter(object):
    """Abstract base.
    """
    defaults = {}
    settings = {}
    args = ()

    def __init__(self, pkg_or_dotted_name, *args, **kw):
        self.args = args
        if 'defaults' in kw.keys():
            self.defaults = kw['defaults']
            del kw['defaults']
        self.settings = kw
        self.package = get_package(pkg_or_dotted_name)
        self.initialize()
        return

    def initialize(self):
        self.filter_keywords()
        return

    def __call__(self):
        suite = unittest.TestSuite()
        suite.addTest(
            self.wrapped_class(
                self.package, **self.settings).getTestSuite()
            )
        return suite
    
    def filter_keywords(self):
        new_kws = self.defaults.copy()
        new_kws.update(self.settings)
        self.settings = new_kws
        if not getattr(self, 'wrapped_class', None):
            return
        supported_kws = get_keyword_params(self.wrapped_class, '__init__')
        for kw, val in new_kws.items():
            if (kw.startswith(self.special_char) and
                kw[1:] in supported_kws):
                new_kws[kw[1:]] = val
            if kw not in supported_kws:
                del new_kws[kw]
        self.settings = new_kws
        return


class FunctionalDocTestGetter(BasicTestGetter):
    """Collect functional doctests.
    """

    wrapped_class = FunctionalDocTestSetup
    special_char = 'f'

class UnitDocTestGetter(BasicTestGetter):
    """Collect unit doctests.
    """

    wrapped_class = UnitDocTestSetup
    special_char = 'u'
    
class PythonTestGetter(BasicTestGetter):
    """Collect 'normal' python tests.
    """

    wrapped_class = UnitTestSetup
    special_char = 'p'

    

class TestGetter(BasicTestGetter):
    """Handle and pass parameters to different test setup types.

    In fact ``TestGetter``s are a replacement for the normally used
    ``test_suite()`` functions in test setup modules. Because in that
    case only callables are expected, we can also use classes.
    """

    def __call__(self):
        """Return a test suite.
        """
        suite = unittest.TestSuite()
        for getter in [FunctionalDocTestGetter, UnitDocTestGetter,
                       PythonTestGetter]:
            suite_getter =  getter(self.package, **self.settings)
            suite_getter.defaults = getattr(self, 'defaults', {})
            suite.addTest(
                suite_getter()
            )
        return suite
