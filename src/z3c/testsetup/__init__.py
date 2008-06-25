from z3c.testsetup.doctesting import UnitDocTestSetup
from z3c.testsetup.testing import UnitTestSetup
from z3c.testsetup.util import get_package
try:
    import zope.app.testing
    from z3c.testsetup.functional.doctesting import FunctionalDocTestSetup
    from z3c.testsetup.functional.testgetter import (
        TestCollector, DocTestCollector, PythonTestGetter)
except ImportError:
    # if zope.app.testing is missing we get a reduced set of getters
    # and collectors, i.e. a set without functional testing machinery.
    from z3c.testsetup.testgetter import (TestCollector, DocTestCollector,
                                          PythonTestGetter)

def register_all_tests(pkg_or_dotted_name, *args, **kwargs):
    return TestCollector(pkg_or_dotted_name, *args, **kwargs)

def register_doctests(pkg_or_dotted_name, *args, **kwargs):
    return DocTestCollector(pkg_or_dotted_name, *args, **kwargs)

def register_pytests(pkg_or_dotted_name, *args, **kwargs):
    return PythonTestGetter(pkg_or_dotted_name, *args, **kwargs)

