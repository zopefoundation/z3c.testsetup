import os
import sys
import tempfile
import unittest
from z3c.testsetup import testrunner
from z3c.testsetup.util import got_working_zope_app_testing


CAVE_PATH = os.path.join(os.path.dirname(__file__), 'cave')
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
