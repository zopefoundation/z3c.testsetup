# this is a package that contains a testsetup.
#
# To let it be found by the testrunner, you must call the testrunner
# with the approriate options set.
import z3c.testsetup
test_suite = z3c.testsetup.register_all_tests('z3c.testsetup.tests.cave')
