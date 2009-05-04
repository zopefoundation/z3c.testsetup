"""A utility that should be registered only with local ftesting.zcml.
"""
import zope.interface

class IFoo(zope.interface.Interface):
    def do_foo():
        pass


class FooUtility(object):
    zope.interface.implements(IFoo)

    def do_foo(self):
        print "Foo!"
