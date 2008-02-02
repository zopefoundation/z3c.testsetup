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
"""Helper functions for testsetup.
"""
from martian.scan import module_info_from_dotted_name

def get_package(pkg_or_dotted_name):
    """Get a package denoted by the given argument.

    If the given argument is a string, we try to load the module
    denoting that module and return it.

    Otherwise, the argument is believed to be a package and is
    returned as-is.
    """
    pkg = pkg_or_dotted_name
    if isinstance(pkg, basestring):
        info = module_info_from_dotted_name(pkg)
        pkg = info.getModule()
    return pkg
