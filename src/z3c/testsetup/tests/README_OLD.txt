z3c.testsetup
*************

.. warning:: THIS IS OUTDATED STUFF

   The tests in here exist only to check for compatibility with
   former releases.

   The methods and markers herein are mostly deprecated, subject to
   change or vanish completely and should not be used any more.

   See `README.txt` in the parent directory for up-to-date
   information.

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
=============

The shortest test setup possible with ``z3c.testsetup`` looks like
this::

   >>> import z3c.testsetup
   >>> test_suite = z3c.testsetup.register_all_tests(
   ...                   'z3c.testsetup.tests.cave')

It is sufficient to put this lines into a python module which is found
by your testrunner (see `samplesetup_short` examples in the ``cave``
package and ``testrunner.txt``).

To sum it up, testsetup with ``z3c.testsetup`` is done in two steps:

1) Make sure your testfiles are named properly (.txt/.rst for
   doctests, valid python modules for usual unit tests) and provide a
   suitable marker string as explained below (`How to mark
   testfiles/modules`_).

2) Write a test setup module which is named so that your testrunner
   finds it and in this module call::

      test_suite = z3c.testsetup.register_all_tests(<package>)

   where ``<package>`` must be a package object. Instead of a package
   object you can also pass the package's dotted name as string like
   `'z3c.testsetup.tests.cave'`.

Given that, this setup should find all doctests (unit and functional)
as well as python tests in the package and register them.


Customized Setups
=================

The `register_all_tests` function mentioned above accepts a bunch of
keyword parameters::

   register_all_tests(pkg_or_dotted_name, filter_func, extensions,
                      encoding, checker,
                      globs, setup, teardown, optionflags
                      zcml_config, layer_name, layer,
                      allow_teardown)

where all but the first parameter are keyword paramters and all but
the package parameter are optional.

While `filter_func` and `extensions` determine the set of testfiles to
be found, the other paramters tell how to setup single tests.


- **filter_func** (**ufilter_func**, **ffilter_func**)

   a function that takes an absolute filepath and returns `True` or
   `False`, depending on whether the file should be included in the
   test suite as doctest or not. `filter_func` applies only to
   doctests.

   We setup a few things to check that::

     >>> import os
     >>> import unittest
     >>> suite = test_suite()
     >>> suite.countTestCases()
     4

   Okay, the callable in `test_suite` we created above with
   `register_all_tests` apparently delivered four testcases. This is
   normally also the number of files involved, but let's check that
   correctly.

   We did setup a function `get_basenames_from_suite` in this testing
   environment (as a `globs` entry) which determines the basenames of
   the paths of all testcases contained in a `TestSuite`::

     >>> get_basenames_from_suite(suite)
     ['file1.py', 'file1.rst', 'file1.txt', 'subdirfile.txt']

   Ah, okay. There are in fact four files, in which testcases were
   found. Now, we define a plain filter function::

      >>> def custom_file_filter(path):
      ...     """Accept all txt files that are not hidden."""
      ...     if os.path.basename(path).startswith('.'):
      ...       return False
      ...     return path.endswith('.txt')

   This one accepts all '.txt' files. We run `register_all_tests`
   again, but this time with a `filter_func` parameter::

      >>> test_suite = z3c.testsetup.register_all_tests(
      ...     'z3c.testsetup.tests.cave',
      ...     filter_func=custom_file_filter)

   To get the resulting test suite, we again call the returned
   callable::

      >>> suite = test_suite()
      >>> get_basenames_from_suite(suite)
      ['file1.py', 'file1.txt', 'file1.txt', 'file1.txt', 'subdirfile.txt',
      'subdirfile.txt', 'subdirfile.txt']

   Compared with the first call to `register_all_tests` we got some
   strange results here: there is a '.py' file, which should have been
   refused by our filter function and the other two files appear
   twice. What happened?

   The python module is included, because python tests are not
   filtered by `filter_func`. Instead this value applies only to
   doctests.

   The second strange result, that every .txt file appears twice in
   the list, comes from the fact, that the filter is valid for unit
   and functional doctests at the same time. In other words: the tests
   in those .txt files are registered twice, as unittests and a second
   time as functional tests as well.

   If you want a filter function for functional doctests or unit
   doctests only, then you can use `ffilter_func` and `ufilter_func`
   respectively::

      >>> test_suite = z3c.testsetup.register_all_tests(
      ...     'z3c.testsetup.tests.cave',
      ...     ffilter_func=custom_file_filter,
      ...     ufilter_func=lambda x: False)

      >>> suite = test_suite()
      >>> get_basenames_from_suite(suite)
      ['file1.py', 'file1.txt', 'subdirfile.txt']

   As expected, every .txt file was only registered once. The same
   happens, when we switch and accept only unit doctests::

      >>> test_suite = z3c.testsetup.register_all_tests(
      ...     'z3c.testsetup.tests.cave',
      ...     ffilter_func=lambda x: False,
      ...     ufilter_func=custom_file_filter)

      >>> suite = test_suite()
      >>> get_basenames_from_suite(suite)
      ['file1.py', 'file1.txt', 'subdirfile.txt']

   If you specify both, a `filter_func` and a more specialized
   `ufilter_func` or `ffilter_func`, then this has the same effect as
   passing both, `ufilter_func` and `ffilter_func`::

      >>> test_suite = z3c.testsetup.register_all_tests(
      ...     'z3c.testsetup.tests.cave',
      ...     ffilter_func=lambda x: False,
      ...     filter_func=custom_file_filter)

      >>> suite = test_suite()
      >>> get_basenames_from_suite(suite)
      ['file1.py', 'file1.txt', 'file1.txt', 'subdirfile.txt', 
       'subdirfile.txt']


- **pfilter_func**:

    Does basically the same as the ``filter_funcs`` above, but handles
    Python modules instead of file paths. It therefore determines the
    set of 'normal' Python tests accepted and does not touch the set
    of doctests accepted.

    We define a simple custom filter::

      >>> def custom_module_filter(module_info):
      ...     return 'Tests with real' in open(module_info.path, 'r').read()

    that checks for a certain string in modules' doc strings.

    Now we start again with `pfilter_func` set::

      >>> test_suite = z3c.testsetup.register_all_tests(
      ...     'z3c.testsetup.tests.cave',
      ...     pfilter_func=custom_module_filter)
      >>> suite = test_suite()
      >>> get_basenames_from_suite(suite)
      ['file1.py', 'file1.rst', 'file1.txt', 'notatest2.py', 'subdirfile.txt']

    Because file1.py and notatest2.py in the cave package contain the
    required string, this is correct. Because the default function
    checks for the string `:Test-Layer: python`, the second module was
    omitted by default.

    Now let's use a filter, that refuses all modules::

      >>> test_suite = z3c.testsetup.register_all_tests(
      ...     'z3c.testsetup.tests.cave',
      ...     pfilter_func=lambda x: False)
      >>> suite = test_suite()
      >>> get_basenames_from_suite(suite)
      ['file1.rst', 'file1.txt', 'subdirfile.txt']

    All Python modules vanished from the list.
   
    In case you wonder, why not all the other Python files of the
    `cave` package (`__init__.py`, for example) appear in one of the
    lists: we get only the result list, which contains only such
    modules, which provide `unittest.TestCase` definitions. Because
    most modules of the `cave` package don't define test cases, they
    do not appear in the list. This automatism is driven by a
    `unittest.TestLoader`. See
    http://docs.python.org/lib/testloader-objects.html to learn more
    about test loaders.


- **extensions** (**uextensions**, **fextensions**):

    a list of filename extensions to be considered during test
    search. Default value is `['.txt', '.rst']`. Python tests are not
    touched by this (they have to be regular Python modules with '.py'
    extension).

    Note, that the `extensions` attribute is used by the default
    filter function. If you pass your own filter function using
    `[u|f]filter_func`, then the extensions filtering won't work any
    more. 

    If we want to register .foo files, we can do so::

      >>> test_suite = z3c.testsetup.register_all_tests(
      ...     'z3c.testsetup.tests.cave',
      ...     extensions=['.foo'])
      >>> suite = test_suite()
      >>> get_basenames_from_suite(suite)
      ['file1.py', 'notatest1.foo', 'notatest1.foo']

    Note, that only files that contain an appropriate marker are
    found, regardless of the filename extension. The new .foo file
    contains a marker for unit doctests and functional doctests, such
    it is included twice in the list.

    As we can see, the new file appears twice. This is, because it is
    registered as functional doctest and unitdoctest as well.

    To collect only functional doctests with a certain set of filename
    extensions you can use: `fextensions`::

      >>> test_suite = z3c.testsetup.register_all_tests(
      ...     'z3c.testsetup.tests.cave',
      ...     fextensions=['.foo'])
      >>> suite = test_suite()
      >>> get_basenames_from_suite(suite)
      ['file1.py', 'file1.rst', 'notatest1.foo']

    Here the .rst file were registered as unit doctest, while the .foo
    file was registered as functional doctest.

    To collect only unit doctests with a different set of filename
    extensions you can use `uextensions`::

      >>> test_suite = z3c.testsetup.register_all_tests(
      ...     'z3c.testsetup.tests.cave',
      ...     uextensions=['.foo'])
      >>> suite = test_suite()
      >>> get_basenames_from_suite(suite)
      ['file1.py', 'file1.txt', 'notatest1.foo', 'subdirfile.txt']

    Here the .foo file was registered as unit doctest and the .txt
    files as functional ones.


- **encoding**:   

    the encoding of testfiles. 'utf-8' by default. Setting this to `None`
    means using the default value. We've hidden one doctest file, that
    contains umlauts. If we set the encoding to `ascii`, we get an
    error::

      >>> test_suite = z3c.testsetup.register_all_tests(
      ...     'z3c.testsetup.tests.cave',
      ...     encoding='ascii')
      >>> suite = test_suite()
      Traceback (most recent call last):
      ...
      UnicodeDecodeError: 'ascii' codec can't decode ...: ordinal 
      not in range(128)

    While using 'latin-1' will work::

      >>> test_suite = z3c.testsetup.register_all_tests(
      ...     'z3c.testsetup.tests.cave',
      ...     encoding='latin-1')
      >>> suite = test_suite()
      
    No traceback here.

    You can always overwrite an encoding setting for a certain file by
    following PEP 0263 ( http://www.python.org/dev/peps/pep-0263/ ).


- **checker**:

    An output checker for functional doctests. `None` by default. A
    typical output checker can be created like this::

      >>> import re
      >>> from zope.testing import renormalizing
      >>> mychecker = renormalizing.RENormalizing([
      ...    (re.compile('[0-9]*[.][0-9]* seconds'), 
      ...     '<SOME NUMBER OF> seconds'),
      ...    (re.compile('at 0x[0-9a-f]+'), 'at <SOME ADDRESS>'),
      ... ])

    This would match for example output like `0.123 seconds` if you
    write in your doctest::

      <SOME NUBMER OF> seconds

    Please see ``testrunner.txt`` for examples of usage.

- **globs**:

    A dictionary of things that should be available immediately
    (without imports) during tests. Defaults are::

      dict(http=HTTPCaller(),
           getRootFolder=getRootFolder,
           sync=sync)

    for functional doctests and an empty dict for unit
    doctests. Python test globals can't be set this way.

    If you want to register special globals for functional doctest or
    unit doctests only, then you can use the `fglobs` and/or `uglobs`
    keyword respectively. These keywords replace any `globs` value for
    the respective kind of tests.

    For more extensive examples see ``testrunner.txt``.

- **setup**:

    A function that takes a `test` argument and is executed before
    every single doctest. By default it runs::

      zope.app.testing.functional.FunctionalTestSetup().setUp()

    for functional doctests and an empty function for unit
    doctests. Python tests provide their own setups.

    If you want to register special setup-functions for either
    functional or unit doctests, then you can pass keyword parameters
    `fsetup` or `usetup` respectively.

- **teardown**:   

    The equivalent to `setup`. Runs by default::

      FunctionalTestSetup().tearDown()

    for functional doctests and::

      zope.testing.cleanup.cleanUp()

    for unit doctests. Python tests have to provide their own teardown
    functions in TestCases.

- **optionflags**:

    Optionflags influence the behaviour of the testrunner. They are
    logically or'd so that you can add them arithmetically. See

      http://svn.zope.org/zope.testing/trunk/src/zope/testing/doctest.py

    for details.

- **zcml_config**:

    A filepath of a ZCML file which is registered with functional
    doctests. In the ZCML file you can for example register principals
    (users) usable by functional doctests.

    By default any `ftesting.zcml` file from the root of the given
    package is taken. If this does not exist, an empty ZCML file of
    the z3c.testsetup package is used (``ftesting.zcml``).

    This parameter has no effect, if also a ``layer`` parameter is
    given.

- **layer_name**:

    You can name your layer, to distinguish different setups of
    functional doctests. The layer name can be an arbitrary string.

    This parameter has no effect, if also a ``layer`` parameter is
    given.

- **layer**:

    You can register a ZCML layer yourself and pass it as the
    ``layer`` parameter. If you only have a filepath to the according
    ZCML file, use the ``zcml_config`` paramter instead.

    This parameter overrides any ``zcml_config`` and ``layer_name``
    parameter.

- **allow_teardown**:

    True by default.  This allows the testing mechanism to try to tear down
    ZCML layers.  If set to False, every ZCML layer is run in a separate
    process for really complete isolation.  Setting it to False leads to
    incomplete profiling and code coverage data.  It needs to be set to False
    in rare cases like setting interfaces on classes programmatically.


How to mark testfiles/modules
=============================

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


