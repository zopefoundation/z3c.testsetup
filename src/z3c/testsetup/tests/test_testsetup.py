import os
import sys
import gc
import re
import unittest
from zope.testing import doctest, cleanup, renormalizing
import zope.component.eventtesting

TESTFILES = ['basicsetup.txt', 'functionaldoctestsetup.txt',
             'unitdoctestsetup.txt', 'util.txt']

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

def testrunner_suite():
    def setUp(test):
        test.globs['saved-sys-info'] = (
            sys.path[:],
            sys.argv[:],
            sys.modules.copy(),
            gc.get_threshold(),
            )
        test.globs['this_directory'] = os.path.split(__file__)[0]
        test.globs['testrunner_script'] = __file__

    def tearDown(test):
        sys.path[:], sys.argv[:] = test.globs['saved-sys-info'][:2]
        gc.set_threshold(*test.globs['saved-sys-info'][3])
        sys.modules.clear()
        sys.modules.update(test.globs['saved-sys-info'][2])
    suites = [
        doctest.DocFileSuite(
        os.path.join('..', 'testrunner.txt'),
        setUp=setUp, tearDown=tearDown,
        optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE,
        checker=checker),
        ]

    suite = unittest.TestSuite(suites)
    return suite


def suiteFromFile(filename):
    suite = unittest.TestSuite()
    dottedname = os.path.join('..', filename) #'../%s' % (filename[:],)
    test = doctest.DocFileSuite(dottedname,
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
    suite.addTest(testrunner_suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
