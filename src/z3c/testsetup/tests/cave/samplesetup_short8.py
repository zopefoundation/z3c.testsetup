import os
from zope.testing import renormalizing
import z3c.testsetup
test_suite = z3c.testsetup.register_all_tests(
    'z3c.testsetup.tests.cave',
    extensions = ['.chk',],
    fregexp_list = [':Test-Layer:.*globs.*',],
    fglobs = {
        'basename' : os.path.basename
    }
    )
