from z3c.testsetup.base import BasicTestSetup
from z3c.testsetup.doctesting import (UnitDocTestSetup, FunctionalDocTestSetup,
                                      register_doctests, collect_doctests)
from z3c.testsetup.testing import (UnitTestSetup, register_pytests,
                                   collect_pytests)
from z3c.testsetup.util import get_package
import unittest

def register_all_tests(pkg_or_dotted_name):
    pkg = get_package(pkg_or_dotted_name)
    def tempfunc():
        suite = unittest.TestSuite()
        suite.addTest(collect_pytests(pkg))
        suite.addTest(collect_doctests(pkg))
        return suite
    return tempfunc
