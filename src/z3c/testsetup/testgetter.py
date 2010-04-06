##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
"""TestGetters and TestCollectors.

TestGetters wrap ordinary TestSetups and TestCollectors wrap
TestGetters. They ease the writing of often used ``test_suite()``
functions in test setup modules of projects.

See testgetter.txt to learn more about this stuff.
"""
import unittest
from z3c.testsetup.doctesting import UnitDocTestSetup, SimpleDocTestSetup
from z3c.testsetup.testing import UnitTestSetup
from z3c.testsetup.util import get_package, get_keyword_params

class BasicTestGetter(object):
    """Abstract base for TestGetters.

    TestGetters are a replacement for the test_suite() functions often
    defined in test setup modules. They are more elegant, more
    flexible, reusable and better looking ;-)
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
        try:
            self.package = get_package(pkg_or_dotted_name)
        except ImportError:
            # This might happen when we try to resolve the calling script.
            self.package = None
            pass
        self.initialize()
        return

    def initialize(self):
        """Convenience method called at end of constructor.

        Might be usable for derived classes.
        """
        pass

    def __call__(self):
        """Get a testsuite.
        """
        self.filterKeywords()
        suite = unittest.TestSuite()
        if self.package is None:
            return suite
        suite.addTest(
            self.wrapped_class(
                self.package, **self.settings).getTestSuite()
            )
        return suite
    
    def filterKeywords(self):
        """Filter keywords passed to the constructor.

        See testgetter.txt for deeper insights.
        """
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

    def getTestSuite(self):
        """A convenience method.

        Some people might expect this method to exist.
        """
        return self.__call__()


class SimpleDocTestGetter(BasicTestGetter):
    """Collect simple unit doctests.
    """
    wrapped_class = SimpleDocTestSetup
    special_char = 'd'

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


class BasicTestCollector(BasicTestGetter):
    """Abstract base of TestCollectors.

    TestCollectors are TestGetters, that can handle several TestGetter
    types at once.
    """
    
    handled_getters = []
    def __call__(self):
        """Return a test suite.
        """
        suite = unittest.TestSuite()
        for getter_cls in self.handled_getters:
            if self.package is None:
                continue
            getter = getter_cls(self.package, **self.settings)
            # Merge our defaults with target defaults...
            target_defaults = getattr(getter, 'defaults', {})
            self_defaults = getattr(self, 'defaults', {})
            getter.defaults = target_defaults.copy()
            getter.defaults.update(self_defaults)
            suite.addTest(getter.getTestSuite())
        return suite

class DocTestCollector(BasicTestCollector):
    """A TestCollector that wraps unit doctests.
    """
    handled_getters = [UnitDocTestGetter, SimpleDocTestGetter]

class TestCollector(BasicTestCollector):
    """A TestCollector that wraps doctests and PythonTests.
    """
    handled_getters = [SimpleDocTestGetter,
                       UnitDocTestGetter, PythonTestGetter]

