from z3c.testsetup.doctesting import UnitDocTestSetup, FunctionalDocTestSetup
from z3c.testsetup.testing import UnitTestSetup
from z3c.testsetup.util import get_package
from z3c.testsetup.testgetter import (TestCollector, DocTestCollector,
                                      PythonTestGetter)

def register_all_tests(pkg_or_dotted_name, *args, **kwargs):
    return TestCollector(pkg_or_dotted_name, *args, **kwargs)

def register_doctests(pkg_or_dotted_name, *args, **kwargs):
    return DocTestCollector(pkg_or_dotted_name, *args, **kwargs)

def register_pytests(pkg_or_dotted_name, *args, **kwargs):
    return PythonTestGetter(pkg_or_dotted_name, *args, **kwargs)

