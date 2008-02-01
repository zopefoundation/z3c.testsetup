=============
z3c.testsetup
=============

is a package that provides some convenience stuff to enable rapid
doctest setup for Zope 3 components. It finds doctests throughout a
whole file tree and registers them with sensible, modifiable
defaults. It is written for developers, that whish to test their code
with functional or unit doctests.

Setting up doctests (contrary to *writing* those tests) can become
cumbersome with Zope 3. In the environment you often have to prepare
complex things like test layers, setup functions, teardown functions
and much more. Often this steps have to be done again and again.

``z3c.testsetup`` can shorten this work by setting sensible defaults
for the most important aspects of test setups.

Currently only doctests (contrary to 'real' Python tests) are
supported.

See `README.txt` in the src/z3c/testsetup directory for API
documentation.


Prerequisites
-------------

You need::

- Python 2.4. Rumors are, that also Python 2.5 will do.

- `setuptools`, available from 
  http://peak.telecommunity.com/DevCenter/setuptools

Other needed packages will be downloaded during
installation. Therefore you need an internet connection during
installation. 


Installation
------------

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
-----

See `README.txt` in the src/z3c/testsetup directory for API
documentation.
