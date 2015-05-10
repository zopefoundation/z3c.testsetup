import doctest
import os
import re
import sys
import gc
import warnings
import unittest
from zope.testing import cleanup, renormalizing
import zope.component.eventtesting
from z3c.testsetup.util import get_package, got_working_zope_app_testing


TESTFILES = ['basicsetup.txt',
             'pythontestsetup.txt',
             'unitdoctestsetup.txt',
             'util.txt',
             'unittestsetup.txt',
             os.path.join('tests', 'util.txt'),
             ]


NON_FUNCTIONAL_TESTFILES = [
    # These tests work only _without_ a working zope.app.testing installed
    os.path.join('tests', 'setupininit_nonfunctional.txt'),
    ]


FUNCTIONAL_TESTFILES = [
    # These tests make only sense _with_ a working zope.app.testing installed
    os.path.join('tests', 'setupininit.txt'),
    os.path.join('functional', 'functionaldoctestsetup.txt'),
    ]


checker = renormalizing.RENormalizing([
    # Relevant normalizers from zope.testing.testrunner.tests:
    (re.compile(r'(\d minutes )?\d+[.]\d\d\d seconds'), 'N.NNN seconds'),
    # zope.testrunner changed its output format in 4.4.0:
    (re.compile(r'(Ran .*), (\d) errors and 0 skipped'), r'\1 and \2 errors'),
    (re.compile(r'(Total: .*), (\d) errors and 0 skipped'), r'\1, \2 errors'),
    # Our own one to work around
    # http://reinout.vanrees.org/weblog/2009/07/16/invisible-test-diff.html:
    (re.compile(r'.*1034h'), ''),
    #windows line endings:
    (re.compile('\r\n'), '\n'),
    #windows drive root:
    (re.compile(r'[a-zA-Z]:\\'), '/'),
    #windows path separator:
    (re.compile(r'\\\\'), '/'),
    (re.compile(r'\\'), '/'),
    ])


def get_testcases_from_suite(suite):
    result = []
    for elem in list(suite):
        if isinstance(elem, unittest.TestCase):
            result.append(elem)
        if isinstance(elem, unittest.TestSuite):
            result.extend(
                get_testcases_from_suite(elem))
    return result


def get_filenames_from_suite(suite):
    testcases = get_testcases_from_suite(suite)
    result = []
    for testcase in testcases:
        filename = str(testcase)
        if ' ' in filename:
            filename = str(get_package(testcase.__module__).__file__)
            filename = os.path.splitext(filename)[0] + '.py'
        result.append(filename)
    result.sort()
    return result


def get_basenames_from_suite(suite):
    basenames = [os.path.basename(x) for x in get_filenames_from_suite(suite)]
    basenames.sort()
    return basenames


def print_file(path):
    """Prints file contents with leading bar on each line.

    This way we prevent the testrunner to test the output.
    """
    contents = open(path, 'r').read()
    print('|  ' + '\n|  '.join(contents.split('\n')))
    return


def setUpZope(test):
    zope.component.eventtesting.setUp(test)


def cleanUpZope(test):
    cleanup.cleanUp()


def testrunner_suite():

    def setUp(test):
        test.globs['saved-sys-info'] = (
            sys.path[:],
            sys.argv[:],
            sys.modules.copy(),
            gc.get_threshold(),
            )
        test.globs['get_basenames_from_suite'] = get_basenames_from_suite
        test.globs['print_file'] = print_file
        zope.component.eventtesting.setUp(test)

    def tearDown(test):
        cleanup.cleanUp()
        sys.path[:], sys.argv[:] = test.globs['saved-sys-info'][:2]
        gc.set_threshold(*test.globs['saved-sys-info'][3])
        sys.modules.clear()
        sys.modules.update(test.globs['saved-sys-info'][2])

    suites = [
        doctest.DocFileSuite(
            'tests/README_OLD.txt',
            'testgetter.txt',
            'testrunner.txt',
            'README.txt',
            os.path.join('tests', 'util.txt'),
            package='z3c.testsetup',
            setUp=setUp, tearDown=tearDown,
            optionflags=(doctest.ELLIPSIS |
                         doctest.NORMALIZE_WHITESPACE |
                         doctest.REPORT_NDIFF),
            checker=checker),
        ]

    suite = unittest.TestSuite(suites)
    return suite


def zopeapptestingless_suite():

    def setUp(test):
        test.globs['saved-sys-info'] = (
            sys.path[:],
            sys.argv[:],
            sys.modules.copy(),
            gc.get_threshold(),
            )
        mlist = [x for x in sys.modules.keys()
                 if 'zope.app' in x or 'z3c.testsetup' in x]
        for m in mlist:
            del sys.modules[m]
        plist = [x for x in sys.path if 'zope.app' in x]
        for p in plist:
            del sys.path[sys.path.index(p)]

        test.globs['this_directory'] = os.path.split(__file__)[0]
        test.globs['testrunner_script'] = __file__
        test.globs['get_basenames_from_suite'] = get_basenames_from_suite

    def tearDown(test):
        sys.path[:], sys.argv[:] = test.globs['saved-sys-info'][:2]
        gc.set_threshold(*test.globs['saved-sys-info'][3])
        sys.modules.clear()
        sys.modules.update(test.globs['saved-sys-info'][2])

    suites = [
        doctest.DocFileSuite(
            'nozopeapptesting.txt',
            package='z3c.testsetup',
            setUp=setUp, tearDown=tearDown,
            optionflags=(doctest.ELLIPSIS |
                         doctest.NORMALIZE_WHITESPACE |
                         doctest.REPORT_NDIFF),
            checker=checker),
        ]

    suite = unittest.TestSuite(suites)
    return suite


def suiteFromFile(filename):
    suite = doctest.DocFileSuite(
        filename,
        package='z3c.testsetup',
        setUp=setUpZope,
        tearDown=cleanUpZope,
        globs={
            'get_basenames_from_suite': get_basenames_from_suite,
            'print_file': print_file},
        checker=checker,
        optionflags=(
            doctest.ELLIPSIS |
            doctest.NORMALIZE_WHITESPACE |
            doctest.REPORT_NDIFF)
        )
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in TESTFILES:
        suite.addTest(suiteFromFile(name))
    if got_working_zope_app_testing():
        for name in FUNCTIONAL_TESTFILES:
            suite.addTest(suiteFromFile(name))
    else:
        message = (
            "Skipped the following tests due to missing "
            "usable `zope.app.testing` package: %s" % FUNCTIONAL_TESTFILES
            )
        warnings.warn(message)
        for name in NON_FUNCTIONAL_TESTFILES:
            suite.addTest(suiteFromFile(name))
    suite.addTest(testrunner_suite())
    suite.addTest(zopeapptestingless_suite())
    return suite
