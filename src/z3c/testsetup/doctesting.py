##############################################################################
#
# Copyright (c) 2007-2009 Zope Foundation and Contributors.
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
from os import listdir
from zope.testing import doctest, cleanup
from z3c.testsetup.base import BasicTestSetup
from z3c.testsetup.util import (get_package, get_marker_from_file, warn,
                                get_attribute)

class DocTestSetup(BasicTestSetup):
    """A test setup for doctests."""

    globs = {}

    optionflags = (doctest.ELLIPSIS+
                   doctest.NORMALIZE_WHITESPACE+
                   doctest.REPORT_NDIFF)

    encoding = 'utf-8'

    checker = None

    def __init__(self, package, setup=None, teardown=None, globs=None,
                 optionflags=None, encoding=None, checker=None,
                 allow_teardown=False, **kw):
        BasicTestSetup.__init__(self, package, **kw)
        self.setUp = setup or self.setUp
        self.tearDown = teardown or self.tearDown
        self.encoding = encoding or self.encoding
        self.checker = checker or self.checker
        if globs is not None:
            self.globs = globs
        if optionflags is not None:
            self.optionflags = optionflags
        self.allow_teardown = allow_teardown


class SimpleDocTestSetup(DocTestSetup):
    """A unified doctest setup for packages.
    """

    extensions = ['.rst', '.txt', '.py']

    def getTestSuite(self):
        docfiles = self.getDocTestFiles(package=self.package)
        suite = unittest.TestSuite()
        for name in docfiles:
            layerdef = get_marker_from_file('layer', name)
            if layerdef is not None:
                layerdef = get_attribute(layerdef)

            zcml_layer = self.getZCMLLayer(name, 'zcml-layer')
            if zcml_layer is not None:
                layerdef = zcml_layer

            functional_zcml_layer = self.getZCMLLayer(
                name, 'functional-zcml-layer')
            if functional_zcml_layer is not None:
                layerdef = functional_zcml_layer

            setup = get_marker_from_file('setup', name) or self.setUp
            if setup is not None and isinstance(setup, basestring):
                setup = get_attribute(setup)

            teardown = get_marker_from_file('teardown', name) or self.tearDown
            if teardown is not None and isinstance(teardown, basestring):
                teardown = get_attribute(teardown)

            if os.path.isabs(name):
                # We get absolute pathnames, but we need relative ones...
                common_prefix = os.path.commonprefix([self.package.__file__,
                                                      name])
                name = name[len(common_prefix):]

            suite_creator = doctest.DocFileSuite
            if functional_zcml_layer is not None:
                try:
                    from zope.app.testing.functional import (
                        FunctionalDocFileSuite)
                except ImportError:
                    warn("""You specified `:functional-zcml-layer:` in
    %s
but there seems to be no `zope.app.testing` package available.
Please include `zope.app.testing` in your project setup to run this testfile.
""" % (os.path.join(common_prefix, name),))
                    continue
                suite_creator = FunctionalDocFileSuite

            # If the defined layer is a ZCMLLayer, we also enable the
            # functional test setup.
            if layerdef is not None:
                try:
                    from zope.app.testing.functional import (
                        ZCMLLayer, FunctionalDocFileSuite)
                    if isinstance(layerdef, ZCMLLayer):
                        suite_creator = FunctionalDocFileSuite
                except ImportError:
                    # If zope.app.testing is not available, the layer
                    # cannot be a ZCML layer.
                    pass

            test = suite_creator(
                name,
                package=self.package,
                setUp=setup,
                tearDown=teardown,
                globs=self.globs,
                optionflags=self.optionflags,
                checker=self.checker,
                **self.additional_options
                )
            if layerdef is not None:
                test.layer = layerdef
            suite.addTest(test)
        return suite

    def getZCMLLayer(self, filepath, marker):
        """Create a ZCML layer out of a test marker.
        """
        zcml_file = get_marker_from_file(marker, filepath)
        if zcml_file is None:
            return
        try:
            # Late import. Some environments don't have
            # ``zope.app.testing`` available.
            from z3c.testsetup.functional.layer import DefaultZCMLLayer
        except ImportError:
            warn("""You specified `%s` in
    %s
but there seems to be no `zope.app.testing` package available.
Please include `zope.app.testing` in your project setup to run this testfile.
""" % (marker, filepath))

        layer = DefaultZCMLLayer(
            os.path.join(os.path.dirname(filepath), zcml_file),
            DefaultZCMLLayer.__module__,
            '%s [%s]' % (DefaultZCMLLayer.__name__,
                         os.path.join(os.path.dirname(filepath), zcml_file)),
            allow_teardown=self.allow_teardown)
        return layer

    def isTestFile(self, filepath):
        """Return ``True`` if a file matches our expectations for a
        doctest file.
        """
        if os.path.splitext(filepath)[1].lower() not in self.extensions:
            return False
        if os.path.basename(filepath).startswith('.'):
            # Ignore *nix hidden files
            return False
        if get_marker_from_file('doctest', filepath) is None:
            return False
        return True

    def getDocTestFiles(self, dirpath=None, **kw):
        """Find all doctest files filtered by filter_func.
        """
        if dirpath is None:
            dirpath = os.path.dirname(self.package.__file__)
        dirlist = []
        for filename in listdir(dirpath):
            abs_path = os.path.join(dirpath, filename)
            if not os.path.isdir(abs_path):
                if self.filter_func(abs_path):
                    dirlist.append(abs_path)
                continue
            # Search subdirectories...
            if not self.isTestDirectory(abs_path):
                continue
            subdir_files = self.getDocTestFiles(dirpath=abs_path, **kw)
            dirlist.extend(subdir_files)
        return dirlist


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
                checker=self.checker,
                **self.additional_options
                )
            if layerdef is not None:
                test.layer = layerdef
            suite.addTest(test)
        return suite
