z3c.testsetup
*************

Easy testsetups for Zope 3 and Python projects.

Setting up tests for Zope 3 projects sometimes tends to be
cumbersome. ``z3c.testsetup`` jumps in here, to support much flatter
test setups.

The package works in two steps:

1) It looks for testfiles in a given package.

2) It registers the tests according to your specifications.

.. note: Important note for users of ':Test-Layer:':

  The marker strings of `z3c.testsetup` changed!

  Please switch to the new syntax described below, if you are still
  using the old ':Test-Layer:' marker. It is more powerful and less
  magic.


Basic Example
=============

Before we can find, register and execute tests, we first have to write
them down. We already have some ready to use tests available, which
can be found in a subpackage::

  >>> import os
  >>> cavepath = os.path.dirname(__file__)
  >>> cavepath = os.path.join(cavepath, 'tests', 'othercave')

In this subpackage there is a simple doctest `doctest01.txt`::

  >>> print open(os.path.join(cavepath, 'doctest01.txt')).read()
  A doctest
  =========
  <BLANKLINE>
  :doctest:
  <BLANKLINE>
  This is a simple doctest.
  <BLANKLINE>
  ...>>> 1+1
  ...2


As we can see, the doctest is marked by a special marker

   `:doctest:`. 

This marker tells the testsetup machinery, that this file contains
doctest examples that should be registered during test runs. Without
this marker, a testfile won't be registered during tests!

This is the only difference to 'normal' doctests here.

Now, that we have a doctest available, we can write a testsetup
routine, that collects all tests, registers them and passes them to
the testrunner.

We have such a simple testsetup already available::

  >>> print open(os.path.join(cavepath, 'simplesetup01.py')).read()
  import z3c.testsetup
  test_suite = z3c.testsetup.register_all_tests(
      'z3c.testsetup.tests.othercave')

This is all we need in simple cases. We use

   `register_all_tests(<dotted_pkg_name>)` 

to tell the setup machinery, where to look for test files. Note, that
also files in subpackages will be found, registered and executed, when
they are marked approriately.

Let's start the testrunner and see what it gives::

  >>> import sys
  >>> sys.argv = [sys.argv[0],]
  >>> defaults = [
  ...     '--path', cavepath,
  ...     '--tests-pattern', '^simplesetup01$',
  ...     ]
  >>> from zope.testing import testrunner
  >>> testrunner.run(defaults)
    Running z3c...functional.layer.DefaultZCMLLayer [ftesting.zcml] tests:
      Set up z3c....layer.DefaultZCMLLayer [ftesting.zcml] in N.NNN seconds.
      Ran 3 tests with 0 failures and 0 errors in N.NNN seconds.
    Running z3c...functional.layer.DefaultZCMLLayer [ftesting2.zcml] tests:
      Tear down z3c...layer.DefaultZCMLLayer [ftesting.zcml] ... not supported
      Running in a subprocess.
      Set up z3c...layer.DefaultZCMLLayer [ftesting2.zcml] in N.NNN seconds.
      Ran 1 tests with 0 failures and 0 errors in N.NNN seconds.
      Tear down z3c...layer.DefaultZCMLLayer [ftesting2.zcml] ... not supported
    Running z3c.testsetup.tests.othercave.testing.UnitLayer1 tests:
      Running in a subprocess.
      Set up z3c.testsetup.tests.othercave.testing.UnitLayer1 in N.NNN seconds.
        Running testSetUp of UnitLayer1
        Running testTearDown of UnitLayer1
      Ran 1 tests with 0 failures and 0 errors in N.NNN seconds.
      Tear down z3c...tests.othercave.testing.UnitLayer1 in N.NNN seconds.
    Running zope.testing.testrunner.layer.UnitTests tests:
      Running in a subprocess.
      Set up zope.testing.testrunner.layer.UnitTests in N.NNN seconds.
      Ran 2 tests with 0 failures and 0 errors in N.NNN seconds.
      Tear down zope.testing.testrunner.layer.UnitTests in N.NNN seconds.
    Total: 7 tests, 0 failures, 0 errors in N.NNN seconds.
    False
