
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

