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
"""TestGetters and TestCollectors that include functional tests.

TestGetters wrap ordinary TestSetups and TestCollectors wrap
TestGetters. They ease the writing of often used ``test_suite()``
functions in test setup modules of projects.

See testgetter.txt to learn more about this stuff.
"""
import unittest
from z3c.testsetup.doctesting import UnitDocTestSetup
from z3c.testsetup.functional.doctesting import FunctionalDocTestSetup
from z3c.testsetup.testgetter import (BasicTestGetter, UnitDocTestGetter,
                                      PythonTestGetter, BasicTestCollector,
                                      SimpleDocTestGetter)
from z3c.testsetup.testing import UnitTestSetup
from z3c.testsetup.util import get_package, get_keyword_params

class FunctionalDocTestGetter(BasicTestGetter):
    """Collect functional doctests.
    """
    wrapped_class = FunctionalDocTestSetup
    special_char = 'f'

class DocTestCollector(BasicTestCollector):
    """A TestCollector that wraps functional doctests and unit doctests.
    """
    handled_getters = [FunctionalDocTestGetter, UnitDocTestGetter,
                       SimpleDocTestGetter]

class TestCollector(BasicTestCollector):
    """A TestCollector that wraps doctests and PythonTests.
    """
    handled_getters = [FunctionalDocTestGetter, UnitDocTestGetter,
                       PythonTestGetter, SimpleDocTestGetter]

