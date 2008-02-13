import z3c.testsetup

class CustomTestGetter(z3c.testsetup.TestGetter):
    defaults = {
        'extensions' : ['.bar',],
        'fextensions' : ['.baz',],
        }

    def dummyfunc(self):
        pass

test_suite=CustomTestGetter('z3c.testsetup.tests.cave')
