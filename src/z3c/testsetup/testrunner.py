##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""Testrunner convenience stuff.
"""
from zope.testing import testrunner
from zope.testing.testrunner import run

# Convenience mapping to have run_internal() and run() always
# available and refering to the same function from zope.testing. See
# `testrunner.txt` (bottom) for details.
if hasattr(testrunner, 'run_internal'):
    run = testrunner.run_internal
run_internal = run
