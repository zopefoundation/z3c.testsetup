from z3c.testsetup.base import BasicTestSetup
from z3c.testsetup.doctesting import (UnitDocTestSetup, FunctionalDocTestSetup,
                                      register_doctests, get_doctests_suite)
from z3c.testsetup.testing import (UnitTestSetup, register_pytests,
                                   get_pytests_suite)
from z3c.testsetup.util import get_package
from z3c.testsetup.testgetter import TestGetter
import unittest

def register_all_tests(pkg_or_dotted_name, *args, **kwargs):
    return TestGetter(pkg_or_dotted_name, *args, **kwargs)
