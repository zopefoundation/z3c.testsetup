import os
import sys
import tempfile
import unittest
import warnings
from z3c.testsetup import testrunner
from z3c.testsetup.util import got_working_zope_app_testing


CAVE_PATH = os.path.join(os.path.dirname(__file__), 'cave')
LAYERED_CAVE_PATH = os.path.join(os.path.dirname(__file__), 'layered_cave')
GOT_WORKING_ZOPE_APP_TESTING = got_working_zope_app_testing()


class Capture(object):
    # a contextmanager for capturing simple testrunner output

    def __init__(self):
        sys.stdout.flush()
        self.out = None
        self.err = None

    def __enter__(self):
        sys.stdout.flush()
        self.new_stdout, self.new_stderr = (
            tempfile.TemporaryFile(mode="w+"),
            tempfile.TemporaryFile(mode="w+"))
        self.old_stdout, sys.stdout = sys.stdout, self.new_stdout
        self.old_stderr, sys.stderr = sys.stderr, self.new_stderr
        return self

    def __exit__(self, *args):
        sys.stdout.flush()
        self.new_stdout.seek(0)
        self.new_stderr.seek(0)
        self.out, self.err = self.new_stdout.read(), self.new_stderr.read()
        sys.stdout, sys.stderr = self.old_stdout, self.old_stderr


class TestSamples(unittest.TestCase):

    def setUp(self):
        self._sys_argv_old = sys.argv[:]
        sys.argv = ['test', '--no-color']

    def tearDown(self):
        sys.argv[:] = self._sys_argv_old

    def test_sample_short0(self):
        # we can run sample samplesetupt_short0 in cave
        defaults = [
            '--path', CAVE_PATH,
            '--tests-pattern', '^samplesetup_short0$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Ran 2 tests with 0 failures, 0 errors and 0 skipped" in cap.out
        if GOT_WORKING_ZOPE_APP_TESTING:
            assert "Total: 4 tests, 0 failures, 0 errors and 0 skipped" in (
                cap.out)

    def test_sample_short1(self):
        # we can run sample samplesetup_short1 in cave
        defaults = [
            '--path', CAVE_PATH,
            '--tests-pattern', '^samplesetup_short1$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Ran 1 tests with 0 failures, 0 errors and 0 skipped" in cap.out
        if GOT_WORKING_ZOPE_APP_TESTING:
            assert "Total: 3 tests, 0 failures, 0 errors and 0 skipped" in (
                cap.out)

    def test_sample_short2(self):
        # we can run sample samplesetup_short2 in cave
        defaults = [
            '--path', CAVE_PATH,
            '--tests-pattern', '^samplesetup_short2$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Ran 1 tests with 0 failures, 0 errors and 0 skipped" in cap.out
        if GOT_WORKING_ZOPE_APP_TESTING:
            assert "Total: 3 tests, 0 failures, 0 errors and 0 skipped" in (
                cap.out)

    def test_sample_short3(self):
        # we can run sample samplesetup_short3 in cave
        defaults = [
            '--path', CAVE_PATH,
            '--tests-pattern', '^samplesetup_short3$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Ran 1 tests with 0 failures, 0 errors and 0 skipped" in cap.out

    def test_sample_short4(self):
        # we can run sample samplesetup_short4 in cave
        defaults = [
            '--path', CAVE_PATH,
            '--tests-pattern', '^samplesetup_short4$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Ran 2 tests with 0 failures, 0 errors and 0 skipped" in cap.out
        if GOT_WORKING_ZOPE_APP_TESTING:
            assert "Total: 4 tests, 0 failures, 0 errors and 0 skipped" in (
                cap.out)

    def test_sample_short5(self):
        # we can run sample samplesetup_short5 in cave
        defaults = [
            '--path', CAVE_PATH,
            '--tests-pattern', '^samplesetup_short5$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Ran 1 tests with 0 failures, 0 errors and 0 skipped" in cap.out
        if GOT_WORKING_ZOPE_APP_TESTING:
            assert "Total: 2 tests, 0 failures, 0 errors and 0 skipped" in (
                cap.out)

    def test_sample_short6(self):
        # we can run sample samplesetup_short6 in cave
        # This one is supposed to fail and give hints.
        defaults = [
            '--path', CAVE_PATH,
            '--tests-pattern', '^samplesetup_short6$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Failed example:" in cap.out
        assert "- A memory address at <SOME ADDRESS>" in cap.out
        assert "+ A memory address at 0x1a0322ff" in cap.out

    def test_sample_short7(self):
        # we can run sample samplesetup_short7 in cave.
        # This is about globals
        defaults = [
            '--path', CAVE_PATH,
            '--tests-pattern', '^samplesetup_short7$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Ran 1 tests with 0 failures, 0 errors and 0 skipped" in cap.out
        if GOT_WORKING_ZOPE_APP_TESTING:
            assert "Total: 2 tests, 0 failures, 0 errors and 0 skipped" in (
                cap.out)

    def test_sample_short8(self):
        # we can run sample samplesetup_short8 in cave.
        # This is about "fglobs", functional globals
        defaults = [
            '--path', CAVE_PATH,
            '--tests-pattern', '^samplesetup_short8$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Ran 1 tests with 0 failures, 0 errors and 0 skipped" in cap.out
        if GOT_WORKING_ZOPE_APP_TESTING:
            assert "Total: 2 tests, 0 failures, 0 errors and 0 skipped" in (
                cap.out)

    def test_sample_short9(self):
        # we can run sample samplesetup_short9 in cave.
        # This is about "uglobs", unittest globals
        defaults = [
            '--path', CAVE_PATH,
            '--tests-pattern', '^samplesetup_short9$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Ran 2 tests with 0 failures, 0 errors and 0 skipped" in cap.out


class TestFunctionalOnlySamples(unittest.TestCase):

    def setUp(self):
        self._sys_argv_old = sys.argv[:]
        sys.argv = ['test', '--no-color']

    def tearDown(self):
        sys.argv[:] = self._sys_argv_old

    def test_sample_setup1(self):
        # we can run sample samplesetup1 in cave.
        defaults = [
            '--path', CAVE_PATH,
            '--tests-pattern', '^samplesetup1$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Ran 1 tests with 0 failures, 0 errors and 0 skipped" in cap.out
        if GOT_WORKING_ZOPE_APP_TESTING:
            assert "Total: 3 tests, 0 failures, 0 errors and 0 skipped" in (
                cap.out)

    def test_layeredsetup01(self):
        # we can run sample layeredsetup01 from layered_cave.
        defaults = [
            '--path', LAYERED_CAVE_PATH, '-f',
            '--tests-pattern', '^layeredsetup01$',
        ]
        with Capture() as cap:
            testrunner.run(defaults)
        assert "Total: 4 tests, 0 failures, 0 errors and 0 skipped" in (
                cap.out)


def tests_from_testcase(test_case):
    return unittest.defaultTestLoader.loadTestsFromTestCase(test_case)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(tests_from_testcase(TestSamples))
    test_case = TestFunctionalOnlySamples
    if GOT_WORKING_ZOPE_APP_TESTING:
        suite.addTests(tests_from_testcase(test_case))
    else:
        message = (
            "Skipped the following tests due to missing "
            "usable `zope.app.testing` package: %s" % test_case
            )
        warnings.warn(message)
    return suite
