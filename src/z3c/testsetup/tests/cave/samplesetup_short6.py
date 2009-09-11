import re
from zope.testing import renormalizing
import z3c.testsetup
test_suite = z3c.testsetup.register_all_tests(
    'z3c.testsetup.tests.cave',
    extensions = ['.chk',],
    regexp_list = ['.*checker.*',],
    )
