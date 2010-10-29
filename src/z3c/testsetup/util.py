##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
from inspect import getmro, ismethod, getargspec
from martian.scan import resolve

def get_package(pkg_or_dotted_name):
    """Get a package denoted by the given argument.

    If the given argument is a string, we try to load the module
    denoting that module and return it.

    Otherwise, the argument is believed to be a package and is
    returned as-is.
    """
    pkg = pkg_or_dotted_name
    if isinstance(pkg, basestring):
        pkg = resolve(pkg)
    return pkg

def get_keyword_params(cls, method_name):
    """Get a list of args of a method of a class.

    Get a list containing all names of keyword parameters, that are
    passable to a method. To get a complete list, also inherited
    classes are visited.
    """
    result = set()
    for cls in getmro(cls):
        init = getattr(cls, method_name, None)
        if not ismethod(init):
            # skip 'object'...
            continue
        # Add all keywords, omitting parameters, for which no default
        # exists.
        args, varargs, varkw, defaults = getargspec(init)
        defaultlen = len(defaults)
        result.update(args[-defaultlen:])
        if varkw is None:
            break
    return list(result)
