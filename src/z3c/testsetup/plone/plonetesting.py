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
"""Test setup helpers for Plone.
"""

import os.path
import unittest
from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml, fiveconfigure

from z3c.testsetup.doctesting import UnitDocTestSetup, FunctionalDocTestSetup
from z3c.testsetup.testgetter import (BasicTestGetter, UnitDocTestGetter,
                                      PythonTestGetter, BasicTestCollector)
from z3c.testsetup.util import get_package


class SimplePloneTestCase(ptc.PloneTestCase):
    """A simple Plone test case.
    """
    def afterSetUp(self):
        pass
    def beforeTearDown(self):
        pass

class SimpleFunctionalPloneTestCase(ptc.FunctionalTestCase):
    """A simple functional Plone test case.
    """
    pass

class PloneIntegrationTestSetup(UnitDocTestSetup):
    """An integration test setup for Plone.
    """
    regexp_list = [
        '^\s*:(T|t)est-(L|l)ayer:\s*(integration)\s*',
        ]

    def setUp(self, test):
        pass
    def tearDown(self, test):
        pass
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
                ztc.ZopeDocFileSuite(
                name,
                package=self.package,
                setUp=self.setUp,
                tearDown=self.tearDown,
                globs=self.globs,
                optionflags=self.optionflags,
                test_class=SimpleFunctionalPloneTestCase,
                **self.additional_options
                ))
        return suite

class PloneFunctionalDocTestSetup(FunctionalDocTestSetup):
    regexp_list = [
        '^\s*:(T|t)est-(L|l)ayer:\s*(plone-functional)\s*',
        ]

    def setUp(self, test):
        pass
    def tearDown(self, test):
        pass

    def suiteFromFile(self, name):
        suite = unittest.TestSuite()
        if os.path.isabs(name):
            # We get absolute pathnames, but we need relative ones...
            common_prefix = os.path.commonprefix([self.package.__file__, name])
            name = name[len(common_prefix):]
        test = ztc.FunctionalDocFileSuite(
            name, package=self.package,
            setUp=self.setUp, tearDown=self.tearDown,
            globs=self.globs,
            optionflags=self.optionflags,
            encoding=self.encoding,
            checker=self.checker,
            test_class=SimpleFunctionalPloneTestCase,
            **self.additional_options
            )
        suite.addTest(test)
        return suite

class PloneIntegrationTestGetter(BasicTestGetter):
    """Collect Plone Integration tests.
    """
    wrapped_class = PloneIntegrationTestSetup
    special_char = 'i'

class PloneFunctionalDocTestGetter(BasicTestGetter):
    """A test collector for Plone functional doctests.
    """
    wrapped_class = PloneFunctionalDocTestSetup
    special_char = 'f'

class PloneTestCollector(BasicTestCollector):
    """A test collector that collects, unittests, python tests and the
    two plone specific tests defined here.

    Setting up Plone tests is special, because you have to pass the
    root of packages as argument (currently; subject to change). This
    is, because we have to register the packages with the Plone Site
    before doing integration tests and functional doc tests.
    """
    handled_getters = [PloneFunctionalDocTestGetter,
                       PloneIntegrationTestGetter,
                       UnitDocTestGetter,
                       PythonTestGetter]

    def __init__(self, pkg_or_dotted_name, package_zcml='configure.zcml',
                 extra_packages=[], **kw):
        """Initialize a Plone test collection.

        For this purpose we first setup each package (including the
        pkg_or_dotted_name) and then setup a Plone site with all those
        products.

        The ``pkg_or_dotted_name`` parameter gives a package as real
        package or as a dotted string like ``my.package``.

        The ``package_zcml`` parameter tells, which ZCML file should
        be used for package initialization. It's optional and the
        default is ``'configure.zcml'``.

        The ``extra_packages`` parameter is a list of packages, that
        should be initialized during setup. The list can contain
        dotted names like ``'my.other.package'`` or tuples of dotted
        names and ZCML config file names. A typical list can look like
        this::

          extra_packages = ['some.package',
                            ('another.package', 'blah.zcml'),
                            'third.package',
                            'foo.bar'
                            ]

        and would setup four packages, which are all initialized using
        a local ``configure.zcml`` except ``another.package``, which
        would be initialized with a ``blah.zcml``.

        """
        pkg = get_package(pkg_or_dotted_name)
        dotted_name = pkg.__name__
        package_list = extra_packages
        package_list = [
            isinstance(x, tuple) and x
            or isinstance(x, basestring) and (x, 'configure.zcml')
            for x in extra_packages
            ]
        package_list.insert(0, (dotted_name, package_zcml))
        self.setup_packages(package_list)
        flat_package_list = [x for x in package_list
                             if isinstance(x, basestring)]
        flat_package_list.extend([x[0] for x in package_list
                             if isinstance(x, tuple)])
        ptc.setupPloneSite(products=flat_package_list)
        BasicTestCollector.__init__(self, pkg, **kw)

    @onsetup
    def setup_packages(self, package_list):
        """Setup a list of packages.

        The package list must be a list of tuples, each one containg a
        dotted name and a ZCML filename (pkg related). A typical list
        might look like this::

          [('my.packages.foo', 'configure.zcml'),
           ('another.package.bar', 'configure.zcml')]

        Packages are processed in order of the list.
        """
        fiveconfigure.debug_mode = True
        for dotted_name, zcml_config in package_list:
            zcml.load_config(zcml_config, get_package(dotted_name))
        fiveconfigure.debug_mode = False
        for dotted_name, zcml_config in package_list:
            ztc.installPackage(dotted_name)
        return


