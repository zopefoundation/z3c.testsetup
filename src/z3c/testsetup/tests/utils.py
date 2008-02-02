##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
===========================
Utilities for z3c.testsetup
===========================

The `util` module defines some helper functions of general use.

For most classes in this package, that accept packages as arguments,
these packages can be delivered as real packages or as strings
containing dotted names. To get a package of something, that is either
a string with dotted names or a real package, the `get_package`
function is provided.

Such we can get a package from a dotted name string::

   >>> from z3c.testsetup.util import get_package
   >>> get_package('z3c.testsetup.tests.cave')
   <module 'z3c.testsetup.tests.cave' from '...'>

The dotted name string can be unicode::

   >>> get_package(u'z3c.testsetup.tests.cave')
   <module 'z3c.testsetup.tests.cave' from '...'>

We can indeed pass a package as argument::

   >>> from z3c.testsetup.tests import cave
   >>> get_package(cave)
   <module 'z3c.testsetup.tests.cave' from '...'>


"""
