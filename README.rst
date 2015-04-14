
z3c.testsetup: easy test setup for zope 3 and python projects
*************************************************************

Setting up tests for Zope 3 projects sometimes tends to be cumbersome. You
often have to prepare complex things like test layers, setup functions,
teardown functions and much more. Often these steps have to be done again and
again.  ``z3c.testsetup`` jumps in here, to support much flatter test
setups. The package supports normal Python `unit tests
<http://docs.python.org/library/unittest.html>`_ and `doctests
<http://docs.python.org/library/doctest.html>`_.

Doctests and test modules are found throughout a whole package and registered
with sensible, modifiable defaults.  This saves a lot of manual work!

See `README.txt` and the other .txt files in the src/z3c/testsetup
directory for API documentation. (Or further down this page when reading this
on pypi).


.. contents::

