import unittest
import warnings
import z3c.testsetup
from z3c.testsetup.util import got_working_zope_app_testing
from z3c.testsetup.tests.test_testsetup import get_basenames_from_suite
from z3c.testsetup.tests import cave

GOT_WORKING_ZOPE_APP_TESTING = got_working_zope_app_testing()


class TestTestGettersAndCollectors(unittest.TestCase):

    def test_getter_gets_suite(self):
        # testgetters return unittest.TestSuite instances
        getter = z3c.testsetup.PythonTestGetter(cave)
        suite = getter()
        assert isinstance(suite, unittest.TestSuite)
        assert get_basenames_from_suite(suite) == ['file1.py']

    def test_collector_get_suite(self):
        # testcollectors return unittest.TestSuite instances
        collector = z3c.testsetup.TestCollector(cave)
        suite = collector()
        basenames = get_basenames_from_suite(suite)
        assert isinstance(suite, unittest.TestSuite)
        if GOT_WORKING_ZOPE_APP_TESTING:
            assert basenames == [
                'file1.py', 'file1.rst', 'file1.txt', 'subdirfile.txt']
        else:
            assert basenames == ['file1.py', 'file1.rst']

    def test_getter_accepts_unknow_keywords(self):
        # we can pass unknown keywords to testgetters
        getter = z3c.testsetup.PythonTestGetter(
            cave, non_existent_param='boo')
        assert isinstance(getter(), unittest.TestSuite)

    def test_collector_accepts_unknow_keywords(self):
        # we can pass unknown keywords to testcollectors
        collector = z3c.testsetup.TestCollector(
            cave, non_existent_param='boo')
        assert isinstance(collector(), unittest.TestSuite)

    def test_collector_passes_know_keywords(self):
        # known keywords are passed to wrapped test setups
        # we should only see .py and .txt files here.
        # .py is ok because Python test files getter does not support
        # 'extensions' keyword.
        collector = z3c.testsetup.TestCollector(
            cave, extensions=['.txt'])
        basenames = get_basenames_from_suite(collector())
        if GOT_WORKING_ZOPE_APP_TESTING:
            assert basenames == ['file1.py', 'file1.txt', 'subdirfile.txt']
        else:
            assert basenames == ['file1.py', ]  # other files are functional

    def test_handled_getters_nonfunctional(self):
        # we can get a set of handled TestGetters
        # of non-functional testcolletors.
        from z3c.testsetup.testgetter import TestCollector
        getter_classes = TestCollector.handled_getters
        assert z3c.testsetup.testgetter.UnitDocTestGetter in getter_classes
        assert z3c.testsetup.testgetter.PythonTestGetter in getter_classes
        assert z3c.testsetup.testgetter.SimpleDocTestGetter in getter_classes

    def test_handled_getters_nonfunctional_special_chars(self):
        # test getters provide special chars that are unique
        from z3c.testsetup.testgetter import TestCollector
        getter_classes = TestCollector.handled_getters
        cls_special_chars = [
            (x.__name__, x.special_char) for x in getter_classes]
        assert sorted(cls_special_chars) == [
            ('PythonTestGetter', 'p'), ('SimpleDocTestGetter', 'd'),
            ('UnitDocTestGetter', 'u')
        ]

    def test_collectors_respect_special_char(self):
        # test collectors pass keywords only to respective getters
        from z3c.testsetup.testgetter import TestCollector
        collector = TestCollector(cave, extensions=['.txt'])
        basenames = sorted(get_basenames_from_suite(collector()))
        assert basenames == ['file1.py']

    def test_collector_defaults(self):
        # there are defaults in collectors
        from z3c.testsetup.testgetter import TestCollector
        collector = TestCollector(cave)
        assert hasattr(collector, 'defaults')
        assert isinstance(collector.defaults, dict)

    def test_collector_defaults_modifiable(self):
        # we can change the defaults in collectors
        from z3c.testsetup.testgetter import TestCollector
        collector = TestCollector(cave)
        collector.defaults = {'uextensions': ['.foo']}
        basenames = sorted(get_basenames_from_suite(collector()))
        assert basenames == ['file1.py', 'notatest1.foo']

    def test_custom_collector(self):
        # we can create custom collectors
        from z3c.testsetup.testgetter import TestCollector

        class CustomCollector(TestCollector):
            defaults = {'extensions': ['.foo']}

        collector = CustomCollector(cave)
        basenames = sorted(get_basenames_from_suite(collector()))
        assert basenames == ['file1.py', 'notatest1.foo']


class TestFunctionalTestGettersAndCollectors(unittest.TestCase):

    def test_handled_getters_functional(self):
        # we can get a set of handled TestGetters
        # of functional testcolletors.
        from z3c.testsetup.functional.testgetter import (
            TestCollector, FunctionalDocTestGetter)
        getter_classes = TestCollector.handled_getters
        assert z3c.testsetup.testgetter.UnitDocTestGetter in getter_classes
        assert z3c.testsetup.testgetter.PythonTestGetter in getter_classes
        assert z3c.testsetup.testgetter.SimpleDocTestGetter in getter_classes
        assert FunctionalDocTestGetter in getter_classes

    def test_handled_getters_functional_special_chars(self):
        # test getters provide special chars that are unique
        # also functional ones
        from z3c.testsetup.functional.testgetter import TestCollector
        getter_classes = TestCollector.handled_getters
        cls_special_chars = [
            (x.__name__, x.special_char) for x in getter_classes]
        assert cls_special_chars == [
            ('FunctionalDocTestGetter', 'f'), ('UnitDocTestGetter', 'u'),
            ('PythonTestGetter', 'p'), ('SimpleDocTestGetter', 'd')
        ]

    def test_collectors_respect_functional_special_char(self):
        # test collectors pass keywords only to respective getters
        from z3c.testsetup.functional.testgetter import TestCollector
        collector = TestCollector(cave, fextensions=['.foo'])
        basenames = sorted(get_basenames_from_suite(collector()))
        assert basenames == ['file1.py', 'file1.rst', 'notatest1.foo']

    def test_collector_functional_defaults(self):
        # there are defaults in functional collectors
        from z3c.testsetup.functional.testgetter import TestCollector
        collector = TestCollector(cave)
        assert hasattr(collector, 'defaults')
        assert isinstance(collector.defaults, dict)

    def test_collector_functional_defaults_modifiable(self):
        # we can change the defaults in functional collectors
        from z3c.testsetup.functional.testgetter import TestCollector
        collector = TestCollector(cave)
        collector.defaults = {'fextensions': ['.foo']}
        basenames = sorted(get_basenames_from_suite(collector()))
        assert basenames == ['file1.py', 'file1.rst', 'notatest1.foo']

    def test_custom_functional_collector(self):
        # we can create custom functional collectors
        from z3c.testsetup.functional.testgetter import TestCollector

        class CustomCollector(TestCollector):
            defaults = {'extensions': ['.txt']}

        collector = CustomCollector(cave)
        basenames = sorted(get_basenames_from_suite(collector()))
        assert basenames == ['file1.py', 'file1.txt', 'subdirfile.txt']


def tests_from_testcase(case):
    return unittest.defaultTestLoader.loadTestsFromTestCase(case)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(tests_from_testcase(TestTestGettersAndCollectors))
    case = TestFunctionalTestGettersAndCollectors
    if GOT_WORKING_ZOPE_APP_TESTING:
        suite.addTests(tests_from_testcase(case))
    else:
        message = (
            "Skipped the following tests due to missing "
            "usable `zope.app.testing` package: %s" % case
            )
        warnings.warn(message)
    return suite
