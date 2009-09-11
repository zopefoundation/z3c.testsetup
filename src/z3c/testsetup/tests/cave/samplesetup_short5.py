import re
from zope.testing import renormalizing
import z3c.testsetup
mychecker = renormalizing.RENormalizing([
    (re.compile('[0-9]*[.][0-9]* seconds'), 
     '<SOME NUMBER OF> seconds'),
    (re.compile('at 0x[0-9a-f]+'), 'at <SOME ADDRESS>'),
    ])
test_suite = z3c.testsetup.register_all_tests(
    'z3c.testsetup.tests.cave',
    checker = mychecker,
    extensions = ['.chk',],
    regexp_list = ['.*checker.*',],
    )
