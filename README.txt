
z3c.testsetup
*************

is a package that provides some convenience stuff to enable rapid test
setup for Zope 3 components and normal Python packages. Currently
doctests (normal unit doctests and functional doctests) and usual
Python tests made of ``unittest.TestCase`` definitions are supported.

Doctests and test modules are found throughout a whole package and
registered with sensible, modifiable defaults.

Also support for reusable test setups is provided by so-called
TestGetters and TestCollectors.

Setting up doctests (contrary to *writing* those tests) can become
cumbersome with Zope 3. In the environment you often have to prepare
complex things like test layers, setup functions, teardown functions
and much more. Often this steps have to be done again and again.

``z3c.testsetup`` can shorten this work by setting sensible defaults
for the most important aspects of test setups.

See `README.txt` in the src/z3c/testsetup directory for API
documentation. There is also extensive documentation for (hopefully)
every aspect of the package in this directory. See all the .txt files
to learn more.

Note, that this is alphaware! Do not use it in productive
environments!

**Important Note:**

  This version of ``z3c.testsetup`` uses a new set of testfile markers
  than previous releases did. If you are still using `Test-Layer:
  unit` or similar, please read the README2.txt in the source directory
  carefully to learn how to switch to the new names.


Prerequisites
=============

You need::

- Python 2.4. Rumors are, that also Python 2.5 will do.

- `setuptools`, available from 
  http://peak.telecommunity.com/DevCenter/setuptools

Other needed packages will be downloaded during
installation. Therefore you need an internet connection during
installation. 


Installation
============

From the root of the package run::

     $ python2.4 bootstrap/bootstrap.py

This will download and install everything to run `buildout` in the
next step. Afterwards an executable script `buildout` should be
available in the freshly created `bin/` directory.

Next, fetch all needed packages, install them and create provided
scripts::

     $ bin/buildout

This should create a `test` script in `bin/`.

Running::

     $ bin/test

you can test the installed package.


Usage
=====

See `README.txt` and the other .txt files in the src/z3c/testsetup
directory for API documentation.

**Note:** ``z3c.testsetup`` does **not** fetch all packages you might
  need to run your tests automatically by default. Namely the
  ``zope.app.testing`` and ``zope.component`` packages are not
  included if you require only z3c.testsetup in your `setup.py`.

  This is, to make ``z3c.testsetup`` compatible with packages that
  refuse collaboration when those packages are installed. For
  instance including ``zope.component`` in the dependencies would
  exclude Plone developers from using ``z3c.testsetup``.

  Therefore you must include ``zope.component`` and
  ``zope.app.testing`` to your ``requires`` list in `setup.py` if you
  want to use Zope 3 tests. This, however, is done anyway by other
  packages used in Zope 3 projects and in most cases you do not have
  to care about this matter.

