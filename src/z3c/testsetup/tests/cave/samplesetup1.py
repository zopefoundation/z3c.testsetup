import unittest
import z3c.testsetup
from z3c.testsetup.tests import cave # The package that contains
                                     # the doctest files
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest( # Add all unittests from `cave`
        z3c.testsetup.UnitDocTestSetup(cave).getTestSuite())
    suite.addTest( # Add all functional tests from `cave`
        z3c.testsetup.FunctionalDocTestSetup(cave).getTestSuite())
    return suite
