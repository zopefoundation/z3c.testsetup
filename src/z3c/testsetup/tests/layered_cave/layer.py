"""Layer definitions.

This could also be done in the setup file itself.
"""

import os
from zope.app.testing.functional import ZCMLLayer

# We define a ZCML test layer. ZCML layers are special as they define
# some setup code for creation of empty ZODBs and more. If you only
# want some ZCML registrations to be done, you can use it like so:
FunctionalLayer1 = ZCMLLayer(
    # As first argument we need the absolute path of a ZCML file
    os.path.join(os.path.dirname(__file__), 'ftesting.zcml'),

    # Second argument is the module, where the layer is defined.
    __name__,

    # This is the name of our layer. It can be an arbitrary string.
    'FunctionalLayer1',

    # By default ZCML layers are not torn down. You should make sure,
    # that any registrations you do in your ZCML are removed in a
    # tearDown method if you specify this parameter to be `True`. This
    # parameter is optional.
    allow_teardown = True)

class UnitLayer1(object):
    """This represents a layer.
    A layer is a way to have common setup and teardown that happens 
    once for a whole group of tests.

    It must be an object with a `setUp` and a `tearDown` method, which
    are run once before or after all the tests applied to a layer
    respectively.

    Optionally you can additionally define `testSetUp` and
    `testTearDown` methods, which are run before and after each single
    test.

    This class is not instantiated. Therefore we use classmethods.
    """

    @classmethod
    def setUp(self):
        """This gets run once for the whole test run, or at most once per
        TestSuite that depends on the layer.
        (The latter can happen if multiple suites depend on the layer
        and the testrunner decides to tear down the layer after first 
        suite finishes.)
        """
        
    @classmethod
    def tearDown(self):
        """This gets run once for the whole test run, or at most
        once per TestSuite that depends on the layer,
        after all tests in the suite have finished.
        """

    @classmethod
    def testSetUp(self):
        """This method is run before each single test in the current
        layer. It is optional.
        """
        print "    Running testSetUp of UnitLayer1"

    @classmethod
    def testTearDown(self):
        """This method is run before each single test in the current
        layer. It is optional.
        """
        print "    Running testTearDown of UnitLayer1"
        
