=============
z3c.testsetup
=============

Easy testsetups for Zope 3 and Python projects.

Setting up tests for Zope 3 projects sometimes tends to be
cumbersome. ``z3c.testsetup`` jumps in here, to support much flatter
test setups. The package supports three kinds of tests:

- normal python tests: i.e. tests, that consist of python modules
  which in turn contain ``unittest.TestCase`` classes.

- unit doctests: i.e. tests, that are written as doctests, but require
  no complicated layer setup etc.

- functional doctests: i.e. tests, that are written as doctests, but
  also require a more or less complex framework to test for example
  browser requests.

``z3c.testsetup`` is package-oriented. That means, it registers more or
less automatically all the three kinds of tests mentioned above
insofar they are part of a certain package.

This is a general introduction to ``z3c.testsetup``. For setup
examples you might see the ``cave`` package contained in the `tests/`
directory. More details on special topics can be found in the
appropriate .txt files in this directory.


Basic Example
-------------

The shortest test setup possible with ``z3c.testsetup`` looks like
this::

   >>> import z3c.testsetup
   >>> test_suite = z3c.testsetup.register_all_tests(
   ...                   'z3c.testsetup.tests.cave')

It is sufficient to put this lines into a python module which is found
by your testrunner (see `samplesetup_short` examples in the ``cave``
package and `testrunner.txt`).

To sum it up, testsetup with ``z3c.testsetup`` is done in two steps:

1) Make sure your testfiles are named properly (.txt/.rst for
   doctests, valid python modules for usual unit tests) and provide a
   suitable marker string as explained below.

2) Write a test setup module which is named so that your testrunner
   finds it and in this module call::

      test_suite = z3c.testsetup.register_all_tests(<package>)

   where `<package>` must be a package object. Instead of a package
   object you can also pass the package's dotted name as string like
   `'z3c.testsetup.tests.cave'`.

To avoid non-wanted files and modules to be registered, you have to
mark your wanted test files/modules with a special string explicitly:

- python modules you want to register must provide a module docstring
  that contains a line::

    :Test-Layer: python

  A module doctring is written at the top of file like this:

  **Python Unit Test Example:**::

    """
    A module that tests things.

    :Test-Layer: python

    """
    import unittest
    class MyTest(unittest.TestCase):
        def testFoo(self):
            pass


- doctest files that contain unit tests must provide a string::

    :Test-Layer: unit

  to be registered. Futhermore, their filename extension must be by
  default '.txt' or '.rst'. A file `sampletest.txt` with a unit
  doctest therefore might look like this:

  **Unit Doctest Example 1:**::

     ==========
     My package
     ==========

     :Test-Layer: unit

     This is documentation for the MyPackage package.

        >>> 1+1
        2

  Also python modules which contain tests in doctests notation are
  doctests. As rule of thumb you can say: if a module contains tests
  that are written preceeded by '>>>', then this is a doctest. If
  ``unittest.TestCase`` classes are defined, then it is a 'normal'
  python testfile. Another valid unit doctest module therefore can
  look like this:

  **Unit Doctest Example 2:**::

     """
     ==========
     My package
     ==========

     A package for doing things.

     :Test-Layer: unit

     We check for basic things::

        >>> 1+1
        2

     """
     class MyClass:
         pass


- files that contain functional doctests must provide a string::

    :Test-Layer: functional

  to be registered. Furthermore they must by default have a filename
  extension `.txt` or `.rst`. A file `sampletest.txt` with functional
  tests might look like this:

  **Functional Doctest Example:**::

     ==========
     My package
     ==========

     :Test-Layer: functional

     This is documentation for the MyPackage package.

        >>> 1+1
        2


