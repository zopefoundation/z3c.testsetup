"""
Tests with real TestCase objects.

:unittest: python

"""

import unittest

class TestTest(unittest.TestCase):

    def setUp(self):
        pass

    def testFoo(self):
        self.assertEqual(2, 1+1)

