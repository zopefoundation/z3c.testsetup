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
"""Basic test setup stuff.
"""

from os import listdir
import os.path
import re

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

    def __init__(self, package, filter_func=None, extensions=None, **kw):
        self.package = package
        self.filter_func = filter_func or self.isTestFile
        self.extensions = extensions or self.extensions
        self.additional_options = kw
        return

    def setUp(self, test):
        pass

    def tearDown(self, test):
        pass

    def fileContains(self, filename, regexp_list):
        """Does a file contain lines matching every of the regular
        expressions?
        """
        found_list = []
        try:
            for line in open(filename):
                for regexp in regexp_list:
                    if re.compile(regexp).match(line) and (
                        regexp not in found_list):
                        found_list.append(regexp)
                if len(regexp_list) == len(found_list):
                    break
        except IOError:
            # be gentle
            pass
        return len(regexp_list) == len(found_list)

    def isTestFile(self, filepath):
        """Return ``True`` if a file matches our expectations for a
        doctest file.
        """
        if os.path.splitext(filepath)[1].lower() not in self.extensions:
            return False
        if not self.fileContains(filepath, self.regexp_list):
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

