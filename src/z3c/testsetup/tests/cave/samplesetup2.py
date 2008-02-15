import z3c.testsetup

class CustomTestCollector(z3c.testsetup.TestCollector):
    defaults = {
        'extensions' : ['.bar',],
        'fextensions' : ['.baz',],
        }

    def dummyfunc(self):
        pass

test_suite=CustomTestCollector('z3c.testsetup.tests.cave')
