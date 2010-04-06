##############################################################################
#
# Copyright (c) 2007-2008 Zope Foundation and Contributors.
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
"""Test setup helpers for functional doctests.
"""
import unittest
import os.path
from zope.testing import doctest, cleanup
from zope.app.testing.functional import (
    HTTPCaller, getRootFolder, sync, ZCMLLayer, FunctionalDocFileSuite,
    FunctionalTestSetup)
from z3c.testsetup.doctesting import DocTestSetup
from z3c.testsetup.util import get_package, get_marker_from_file

class FunctionalDocTestSetup(DocTestSetup):
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

    def __init__(self, package, checker=None, zcml_config = None,
                 layer_name='FunctionalLayer', layer=None,
                 allow_teardown=False, **kw):
        DocTestSetup.__init__(self, package, **kw)
        self.allow_teardown = allow_teardown
        self.checker = checker
        # Setup a new layer if specified in params...
        if zcml_config is not None and layer is None:
            if not os.path.isfile(zcml_config):
                zcml_config = os.path.join(
                    os.path.dirname(self.package.__file__),
                    zcml_config)
            self.layer = ZCMLLayer(zcml_config, self.package.__name__,
                                   layer_name,
                                   allow_teardown=self.allow_teardown)
        elif layer is None:
            # Look for ftesting.zcml in pkg-root...
            pkg_ftesting_zcml = os.path.join(
                os.path.dirname(self.package.__file__), 'ftesting.zcml')
            if os.path.isfile(pkg_ftesting_zcml):
                self.layer = ZCMLLayer(pkg_ftesting_zcml,
                                       self.package.__name__, layer_name,
                                       allow_teardown=self.allow_teardown)
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
        layer = get_marker_from_file('Test-Layerdef', name)
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
            checker=self.checker,
            **self.additional_options
            )
        test.layer = self.layer
        if layer is not None:
            test.layer = layer
        suite.addTest(test)
        return suite

    def getTestSuite(self):
        docfiles = self.getDocTestFiles(package=self.package)
        suite = unittest.TestSuite()
        for name in docfiles:
            suite.addTest(self.suiteFromFile(name))
        return suite

