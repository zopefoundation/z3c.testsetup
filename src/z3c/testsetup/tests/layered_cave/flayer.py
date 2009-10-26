"""Functional layer definitions.

This could also be done in the setup file itself.
"""
import os
import zope.app.testing
from zope.app.testing.functional import ZCMLLayer

# We define a ZCML test layer. ZCML layers are special as they define
# some setup code for creation of empty ZODBs and more. If you only
# want some ZCML registrations to be done, you can use it like so:
FunctionalLayer1 = ZCMLLayer(
    # As first argument we need the absolute path of a ZCML file
    os.path.join(os.path.dirname(zope.app.testing.functional.__file__),
                 'ftesting.zcml'),

    # Second argument is the module, where the layer is defined.
    __name__,

    # This is the name of our layer. It can be an arbitrary string.
    'FunctionalLayer1',

    # By default ZCML layers are not torn down. You should make sure,
    # that any registrations you do in your ZCML are removed in a
    # tearDown method if you specify this parameter to be `True`. This
    # parameter is optional.
    allow_teardown = True)
