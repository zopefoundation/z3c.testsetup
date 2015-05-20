# -*- coding: utf-8 -*-
""" Tests for `z3c.testsetup.base`.
"""
import os
import shutil
import tempfile
import unittest
from z3c.testsetup.base import BasicTestSetup
from z3c.testsetup.tests import cave


class TestBasicTestSetup(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.workdir)

    def create_file(self, content):
        path = os.path.join(self.workdir, "myfile")
        with open(path, "wb") as fd:
            fd.write(content)
        return path

    def test_file_contains_match(self):
        # the fileContains method finds matches
        mysetup = BasicTestSetup(cave, regexp_list=["MARKER", ])
        path = self.create_file(b"Line 1\nLine 2\nMARKER in file\n\n")
        assert mysetup.fileContains(path) is True

    def test_file_contains_no_match(self):
        # fileContains might find no match
        mysetup = BasicTestSetup(cave, regexp_list=["MARKER", ])
        path = self.create_file(b"Line 1\nLine 2\nLine 3\n\n")
        assert mysetup.fileContains(path) is False

    def test_file_contains_copes_with_strange_encodings(self):
        # we can also parse files that are not utf-8 or similar
        mysetup = BasicTestSetup(cave, regexp_list=["MARKER", ])
        path = self.create_file(b"Line 1\n \xff\xfeW[ \nMARKER\n\n")
        assert mysetup.fileContains(path) is True
