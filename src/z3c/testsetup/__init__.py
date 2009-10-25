from z3c.testsetup.testing import UnitTestSetup
from z3c.testsetup.util import get_package
from z3c.testsetup.testgetter import (TestCollector, DocTestCollector,
                                      PythonTestGetter)
try:
    # It seems like This must work to make internal functional tests
    # work(?)
    import zope.app.testing.functional

except ImportError:
    # if zope.app.testing is missing, other things should still work.
    pass

def register_all_tests(pkg_or_dotted_name, *args, **kwargs):
    return TestCollector(pkg_or_dotted_name, *args, **kwargs)

def register_doctests(pkg_or_dotted_name, *args, **kwargs):
    return DocTestCollector(pkg_or_dotted_name, *args, **kwargs)

def register_pytests(pkg_or_dotted_name, *args, **kwargs):
    return PythonTestGetter(pkg_or_dotted_name, *args, **kwargs)

