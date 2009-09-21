Developing on z3c.testsetup itself
**********************************

Prerequisites
=============

You need::

- Python 2.4 or 2.5 (status of 2.6 is unknown right now).

- `setuptools`, available from 
  http://peak.telecommunity.com/DevCenter/setuptools

Other needed packages will be downloaded during installation. Therefore you
need an internet connection during installation.


Installation
============

From the root of the package run::

     $ python bootstrap/bootstrap.py

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
