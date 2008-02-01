import re
import unittest
from zope.testing import doctest, cleanup, renormalizing
import zope.component.eventtesting

TESTFILES = ['basicsetup.py', 'functionalsetup.py', 'unittestsetup.py']

def setUpZope(test):
    zope.component.eventtesting.setUp(test)

def cleanUpZope(test):
    cleanup.cleanUp()

checker = renormalizing.RENormalizing([
    # str(Exception) has changed from Python 2.4 to 2.5 (due to
    # Exception now being a new-style class).  This changes the way
    # exceptions appear in traceback printouts.
    (re.compile(r"ConfigurationExecutionError: <class '([\w.]+)'>:"),
                r'ConfigurationExecutionError: \1:'),
    ])

def suiteFromFile(filename):
    suite = unittest.TestSuite()

    if not filename.endswith('.py'):
        continue
    if filename.endswith('_fixture.py'):
        continue
    if filename == '__init__.py':
        continue

    dottedname = 'z3c.testsetup.tests.%s' % (filename[:-3],)
    test = doctest.DocTestSuite(dottedname,
                                setUp=setUpZope,
                                tearDown=cleanUpZope,
                                checker=checker,
                                optionflags=doctest.ELLIPSIS+
                                doctest.NORMALIZE_WHITESPACE)

    suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in TESTFILES:
        suite.addTest(suiteFromFile(name))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
