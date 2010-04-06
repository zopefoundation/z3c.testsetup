##############################################################################
#
# Copyright (c) 2008-2009 Zope Foundation and Contributors.
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
"""Basic test setup stuff.
"""

from os import listdir
import os.path
import re
from z3c.testsetup.util import get_package

class BasicTestSetup(object):
    """A basic test setup for a package.

    A basic test setup is a aggregation of methods and attributes to
    search for appropriate doctest files in a package. Its purpose is
    to collect all basic functionality, that is needed by derived
    classes, that do real test registration.
    """

    extensions = ['.rst', '.txt']
    regexp_list = []
    additional_options = {}

    param_list = ['filter_func', 'extensions']

    def __init__(self, package, regexp_list=None, filter_func=None,
                 extensions=None, **kw):
        self.package = get_package(package)
        self.filter_func = filter_func or self.isTestFile
        self.extensions = extensions or self.extensions
        if regexp_list is not None:
            self.regexp_list = regexp_list
        self.additional_options = kw
        self._init(package, filter_func, extensions, **kw)
        return

    def _init(self, package, *args, **kw):
        """Derived classes can overwrite this method for specialized
        setups.
        """
        pass

    @property
    def regexs(self):
        """Return compiled regexs (cached version, if possible)"""
        cached = getattr(self, '_regexs', None)
        if cached is not None:
            return cached
        self._regexs = [re.compile(regex) for regex in self.regexp_list]
        return self._regexs

    def setUp(self, test):
        pass

    def tearDown(self, test):
        pass

    def fileContains(self, filename):
        """Does a file contain lines matching every of the regular
        expressions?
        """
        found_list = []
        content = open(filename).read()
        return self.textContains(content)

    def textContains(self, text):
        lines = text.split('\n')
        for regexp in self.regexs:
            found = [True for line in lines if regexp.match(line)]
            if len(found):
                # Yeah, found a match, continue to the next regex.
                continue
            else:
                return False
        return True

    def isTestFile(self, filepath):
        """Return ``True`` if a file matches our expectations for a
        doctest file.
        """
        if os.path.splitext(filepath)[1].lower() not in self.extensions:
            return False
        if os.path.basename(filepath).startswith('.'):
            # Ignore *nix hidden files
            return False
        if not self.fileContains(filepath):
            return False
        return True

    def isTestDirectory(self, dirpath):
        """Check whether a given directory should be searched for tests.
        """
        if os.path.basename(dirpath).startswith('.'):
            # We don't search hidden directories like '.svn'
            return False
        return True

    def getDocTestFiles(self, dirpath=None, **kw):
        """Find all doctest files filtered by filter_func.
        """
        if dirpath is None:
            dirpath = os.path.dirname(self.package.__file__)
        dirlist = []
        for filename in listdir(dirpath):
            abs_path = os.path.join(dirpath, filename)
            if not os.path.isdir(abs_path):
                if self.filter_func(abs_path):
                    dirlist.append(abs_path)
                continue
            # Search subdirectories...
            if not self.isTestDirectory(abs_path):
                continue
            subdir_files = self.getDocTestFiles(dirpath=abs_path, **kw)
            dirlist.extend(subdir_files)
        return dirlist

