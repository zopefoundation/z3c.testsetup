from z3c.testsetup.base import BasicTestSetup
from z3c.testsetup.doctesting import (UnitDocTestSetup, FunctionalDocTestSetup,
                                      register_doctests, get_doctests_suite)
from z3c.testsetup.testing import (UnitTestSetup, register_pytests,
                                   get_pytests_suite)
from z3c.testsetup.util import get_package
import unittest

def register_all_tests(pkg_or_dotted_name, *args, **kwargs):
    pkg = get_package(pkg_or_dotted_name)
    def tempfunc():
        suite = unittest.TestSuite()
        suite.addTest(get_pytests_suite(pkg, *args, **kwargs))
        suite.addTest(get_doctests_suite(pkg, *args, **kwargs))
        return suite
    return tempfunc
