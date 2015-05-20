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
from __future__ import print_function

import codecs
import sys
import re

from inspect import getmro, ismethod, isfunction, getargspec
from martian.scan import resolve
from six import string_types


def get_package(pkg_or_dotted_name):
    """Get a package denoted by the given argument.

    If the given argument is a string, we try to load the module
    denoting that module and return it.

    Otherwise, the argument is believed to be a package and is
    returned as-is.
    """
    pkg = pkg_or_dotted_name
    if isinstance(pkg, string_types):
        pkg = resolve(pkg)
    elif isinstance(pkg, bytes):
        pkg = resolve(pkg.decode('utf-8'))
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
        if (not ismethod(init)) and (not isfunction(init)):
            # py2 methods are functions in py3, it seems.
            continue
        # Add all keywords, omitting parameters, for which no default
        # exists.
        args, varargs, varkw, defaults = getargspec(init)
        if defaults:
            result.update(args[-len(defaults):])
        if varkw is None:
            break
    return list(result)

marker_regexs = {}


def get_marker_from_string(marker, text):
    """Looks for a markerstring  in a string.

    Returns the found value or `None`. A markerstring has the form::

     :<Tag>: <Value>

    or

     .. :<Tag>: <Value>

    """
    marker = ":%s:" % marker.lower()
    if marker not in marker_regexs:
        marker_regexs[marker] = re.compile('^(\.\.\s+)?%s(.*)$' % (marker,),
                                           re.IGNORECASE)
    for line in text.split('\n'):
        line = line.strip()
        result = marker_regexs[marker].match(line)
        if result is None:
            continue
        result = result.groups()[1].strip()
        return result
    return None


def get_marker_from_file(marker, filepath):
    """Looks for a markerstring  in a file.

    Returns the found value or `None`. A markerstring has the form::

     :<Tag>: <Value>

    Files are assumed to be UTF-8 encoded. Incompatible characters are
    ignored.
    """
    with codecs.open(filepath, "rb", "utf-8", "ignore") as fd:
        return get_marker_from_string(marker, fd.read())
    return None


def warn(text):
    print("Warning: ", text)


def import_name(name):
    __import__(name)
    return sys.modules[name]


def get_attribute(name):
    name, attr = name.rsplit('.', 1)
    obj = import_name(name)
    return getattr(obj, attr)


def got_working_zope_app_testing():
    """Determine whether we have a working `zope.app.testing` installed.

    Please do not make any assumptions about how the "workingness" of
    `zope.app.testing` in an environment is determined.
    """
    try:
        from zope.app.testing.functional import (
            HTTPCaller, getRootFolder, sync, ZCMLLayer,
            FunctionalDocFileSuite, FunctionalTestSetup)
        return True
    except:
        # any problem here (not only ImportError) is an indicator for
        # serious trouble with zope.app.testing.
        pass
    return False
