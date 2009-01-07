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

  >>> print_file(os.path.join(cavepath, 'doctest01.txt'))
  |  A doctest
  |  =========
  |  
  |  :doctest:
  |  
  |  This is a simple doctest.
  |  
  |    >>> 1+1
  |    2
  |  


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
    Running z3c.testsetup.tests.othercave.testing.UnitLayer2 tests:
      Running in a subprocess.
      Set up z3c.testsetup.tests.othercave.testing.UnitLayer1 in N.NNN seconds.
      Set up z3c.testsetup.tests.othercave.testing.UnitLayer2 in N.NNN seconds.
        Running testSetUp of UnitLayer1
        Running testSetUp of UnitLayer2
        Running testTearDown of UnitLayer2
        Running testTearDown of UnitLayer1
      Ran 1 tests with 0 failures and 0 errors in N.NNN seconds.
      Tear down z3c...tests.othercave.testing.UnitLayer2 in N.NNN seconds.
      Tear down z3c...tests.othercave.testing.UnitLayer1 in N.NNN seconds.
    Running zope.testing.testrunner.layer.UnitTests tests:
      Running in a subprocess.
      Set up zope.testing.testrunner.layer.UnitTests in N.NNN seconds.
        Custom setUp for  <DocTest doctest05.txt from ... (2 examples)>
        Custom tearDown for  <DocTest doctest05.txt from ... (2 examples)>
      Ran 6 tests with 0 failures and 0 errors in N.NNN seconds.
      Tear down zope.testing.testrunner.layer.UnitTests in N.NNN seconds.
    Total: 11 tests, 0 failures, 0 errors in N.NNN seconds.
    False

As we can see, there were regular unittests as well as functional
tests run. Some of the unittests used their own layer (``UnitLayer1``)
whose location were printed and the functional tests used different
ZCML-files for configuration.

Of course, there were more tests than only the ones defined in
``doctest01.txt``. Let's have a look at the other stuff.


Setting up a unittest layer
===========================

We can tell ``z3c.testsetup`` to use a certain unittest layer using
the ``:layer:`` marker as in the following example (see
``tests/othercave/doctest02.txt``)::

    A doctests with layer
    =====================
    <BLANKLINE>
    :doctest:
    :layer: z3c.testsetup.tests.othercave.testing.UnitLayer2
    <BLANKLINE>
      >>> 1+1
      2


The ``:doctest:`` marker was used here as well, because without it the
file would not have been detected as a registerable doctest file (we
want developers to be explicit about that).

The 

 `:layer: <DOTTED_NAME_OF_LAYER_DEF>`

marker then tells, where the testsetup machinery can
find the layer definition. It is given in dotted name notation.

How does the layer definition look like? It is defined as regualr
Python code::

  >>> print open(os.path.join(cavepath, 'testing.py')).read()
  import os
  ...
  class UnitLayer1(object):
      """This represents a layer.
      A layer is a way to have common setup and teardown that happens
      once for a whole group of tests.
  <BLANKLINE>
      It must be an object with a `setUp` and a `tearDown` method, which
      are run once before or after all the tests applied to a layer
      respectively.
  <BLANKLINE>
      Optionally you can additionally define `testSetUp` and
      `testTearDown` methods, which are run before and after each single
      test.
  <BLANKLINE>
      This class is not instantiated. Therefore we use classmethods.
      """
  <BLANKLINE>
      @classmethod
      def setUp(self):
          """This gets run once for the whole test run, or at most once per
          TestSuite that depends on the layer.
          (The latter can happen if multiple suites depend on the layer
          and the testrunner decides to tear down the layer after first
          suite finishes.)
          """
  <BLANKLINE>
      @classmethod
      def tearDown(self):
          """This gets run once for the whole test run, or at most
          once per TestSuite that depends on the layer,
          after all tests in the suite have finished.
          """
  <BLANKLINE>
      @classmethod
      def testSetUp(self):
          """This method is run before each single test in the current
          layer. It is optional.
          """
          print "    Running testSetUp of UnitLayer1"
  <BLANKLINE>
      @classmethod
      def testTearDown(self):
          """This method is run before each single test in the current
          layer. It is optional.
          """
          print "    Running testTearDown of UnitLayer1"
  <BLANKLINE>
  class UnitLayer2(UnitLayer1):
      """This Layer inherits ``UnitLayer1``.
  <BLANKLINE>
      This way we define nested setups. During test runs the testrunner
      will first call the setup methods of ``UnitTest1`` and then those
      of this class. Handling of teardown-methods will happen the other
      way round.
      """
  <BLANKLINE>
      @classmethod
      def setUp(self):
          pass
  <BLANKLINE>
      @classmethod
      def testSetUp(self):
          print "    Running testSetUp of UnitLayer2"
  <BLANKLINE>
      @classmethod
      def testTearDown(self):
          print "    Running testTearDown of UnitLayer2"

In a layer you can do all the special stuff that is needed to run a
certain group of tests properly. Our setup here is special in that we
defined a nested one: ``UnitLayer2`` inherits ``UnitLayer1`` so that
during test runs the appropriate setup and teardown methods are called
(see testrunner output above).

More about test layers can be found at the documentation of
`testrunner layers API
<http://apidoc.zope.org/++apidoc++/Code/zope/testing/testrunner-layers-api.txt/index.html>`_.

Specifying a ZCML file
======================

When it comes to integration or functional tests, we need to specify a
ZCML file to which configures the test environment for us. We can do
that using the

  `:zcml-layer: <ZCML-file-name>`

marker. It expects a ZCML filename as argument and sets up a
ZCML-layered testsuite for us. An example setup might look like so (see
``tests/othercave/doctest03.txt``)::

  A doctest with a ZCML-layer
  ===========================

  :doctest:
  :zcml-layer: ftesting.zcml

    >>> 1+1
    2

.. note:: Requires ``zope.app.testing``

   If you use ``:zcml-layer``, the ``zope.app.testing`` package must
   be available when running the tests and during test setup. This
   package is not fetched by default by ``z3c.testsetup``.

Here we say, that the the local file ``ftesting.zcml`` should be used
as ZCML configuration. As we can see in the above output of testruner,
this file is indeed read during test runs and used by a ZCML layer
called ``DefaultZCMLLayer``. This layer is in fact only a
``zope.app.testing.functional.ZCMLLayer``.

The ZCML file is looked up in the same directory as the doctest file.

When using the ``:zcml-layer:`` marker, the concerned tests are set up
via special methods and functions from `zope.app.testing`. This way
you get 'functional' or 'integration' tests out of the box: in the
beginning an empty ZODB db is setup, ``getRootFolder``, ``sync`` and
other functions are pulled into the test namespace and several things
more.

If you want a plain setup instead then use your own layer definition
using ``:layer:`` and remove the ``:zcml-layer:`` marker.


Setting up a functional ZCML layer
==================================

Sometimes we want tests to be registered using the
``FunctionalDocFileSuite`` function from
``zope.app.testing.functional`` (other tests are set up using
``zope.testing.doctest.DocFileSuite``). This function pulls in even
more functions into ``globs``, like ``http`` (a ``HTTPCaller``
instance), wraps your ``setUp`` and ``tearDown`` methods into
ZODB-setups and several things more. See the definition in
http://svn.zope.org/zope.app.testing/trunk/src/zope/app/testing/functional.py?view=auto.

This setup needs also a ZCML configuration file, which can be
specified via::

  :functional-zcml-layer: <ZCML-file-name>

If a functional ZCML layer is specified in a testfile this way, it
will override any simple ``:zcml-layer:`` or ``:layer:`` definition.

An example setup might look like this (see
``tests/othercave/doctest04.txt``)::

  >>> print_file(os.path.join(cavepath, 'doctest04.txt'))
  |  A functional doctest with ZCML-layer
  |  ====================================
  |
  |  :doctest:
  |  :functional-zcml-layer: ftesting.zcml
  |
  |  We didn't define a real environment in ftesting.zcml, but in
  |  functional tests certain often needed functions should be available
  |  automatically::
  |
  |    >>> getRootFolder()
  |    <zope.app.folder.folder.Folder object at 0x...>
  |

.. note:: Requires ``zope.app.testing``

   If you use ``:zcml-layer``, the ``zope.app.testing`` package must
   be available when running the tests and during test setup. This
   package is not fetched by default by ``z3c.testsetup``.

Specifying ``setUp`` and ``tearDown`` methods
=============================================

We can specify a ``setUp(test)`` and ``tearDown(test)`` method for the
examples in a doctest file, which will be executed once for the whole
doctest file. This can be done using::

  :setup: <dotted.name.of.callable>
  :teardown: <dotted.name.of.callable>

The callables denoted by the dotted names must accept a ``test``
parameter which will be the whole test suite of examples in the
current doctest file.

An example can be found in ``doctest05.txt``::

  >>> print_file(os.path.join(cavepath, 'doctest05.txt'))
  |  A doctest with custom setup/teardown functions
  |  ==============================================
  |  
  |  :doctest:
  |  :setup: z3c.testsetup.tests.othercave.testing.setUp
  |  :teardown: z3c.testsetup.tests.othercave.testing.tearDown
  |  
  |    >>> 1+1
  |    2
  |  
  |  We make use of a function registered during custom setup::
  |  
  |    >>> myfunc(2)
  |    4
  |

The setup/teardown functions denoted in the example look like this::

  >>> print open(os.path.join(cavepath, 'testing.py'), 'rb').read()
  import os
  ...
  def setUp(test):
      print "    Custom setUp for ", test
      # We register a function that will be available during tests.
       test.globs['myfunc'] = lambda x: 2*x
  <BLANKLINE>
  def tearDown(test):
      print "    Custom tearDown for ", test
      del test.globs['myfunc'] # unregister function
  ...

As we can see, there is a function ``myfunc`` pulled into the
namespace of the doctest. We could, however, do arbitrary other things
here, set up a relational test database or whatever.
