Plone tests with ``z3c.testsetup``
**********************************

The ``z3c.testsetup`` package provides limited support for writing
simple testsetups for Plone sites.

We configured a complete Plone policy package in the ``cave``
subdirectory. This package should execute some tests. But first we
have to setup some things, to let the tests run.

Determine our ``instance`` script path::

   >>> from os import path
   >>> import z3c
   >>> inst_script_path = path.join(path.dirname(path.dirname(path.dirname(
   ...     z3c.__file__))), 'bin', 'instance')
   >>> cavepath = path.abspath(path.join(path.dirname(__file__), 'cave'))

Now we can enter a request in a subshell to see, if all tests are
found and executed correctly. This one sets up and installs a complete
Plone site, which takes some time. It is only one test, but it takes
very much time::

   >>> output = get_output_from_cmd(inst_script_path, 'test', '-s',
   ...                              'z3c.testsetup.plone.cave',
   ...                              '--path=%s' % cavepath)
   >>> print output
   Running tests at level 1
   ...
   ...'A Cave Site'
   ...
   Tests with failures:
     ...functionaltest.txt
   Total: 2 tests, 1 failures, 0 errors in ... seconds.


Everything went well.
