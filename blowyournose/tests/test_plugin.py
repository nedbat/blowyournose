from __future__ import print_function

import os
import unittest

import ddt
from lazy import lazy
import mock

from booger import Booger


class TestCaseWithSetupBoogers(unittest.TestCase):
    def setUp(self):
        self.thing = Booger("TestCaseWithSetupBoogers")

    def test_one(self):
        print("one")

    def test_two(self):
        print("two")


class MockedTestCaseMethod(unittest.TestCase):
    @mock.patch('os.listdir', Booger("test_with_mock"))
    def test_with_mock(self):
        self.assertIsInstance(os.listdir, Booger)

    @mock.patch('os.listdir', Booger("test_with_many_mocks"))
    @mock.patch('os.getcwd', Booger("test_with_many_mocks"))
    @mock.patch('os.chdir', "Hey there")
    @mock.patch('os.getgid', Booger("test_with_many_mocks"))
    def test_with_many_mocks(self):
        self.assertIsInstance(os.listdir, Booger)
        self.assertIsInstance(os.getcwd, Booger)
        self.assertEqual(os.chdir, "Hey there")
        self.assertIsInstance(os.getgid, Booger)


@mock.patch('os.listdir', Booger("MockedTestCaseClass", scope='class'))
class MockedTestCaseClass(unittest.TestCase):
    def test_first(self):
        self.assertIsInstance(os.listdir, Booger)

    def test_second(self):
        self.assertIsInstance(os.listdir, Booger)


@ddt.ddt
class DataTestCase1(unittest.TestCase):

    if 0:   # This isn't expected to work, because we don't need it to.
        @ddt.data(
            Booger("DataTestCase1", scope='class'),
            Booger("DataTestCase1", scope='class'),
        )
        def test_boogers(self, boog):
            self.assertIsInstance(boog, Booger)

    @ddt.data(
        (1, 2),
        (2, 4),
    )
    @mock.patch('os.listdir', Booger("DataTestCase1", scope='class'))
    def test_double(self, ab):
        self.assertEqual(2*ab[0], ab[1])
        self.assertIsInstance(os.listdir, Booger)

@ddt.ddt
class DataTestCase2(unittest.TestCase):

    @mock.patch('os.listdir', Booger("DataTestCase2", scope='class'))
    @ddt.data(
        (1, 3),
        (2, 6),
    )
    def test_triple(self, ab):
        self.assertEqual(3*ab[0], ab[1])
        self.assertIsInstance(os.listdir, Booger)


class LazyTestCase(unittest.TestCase):

    @lazy
    def boog(self):
        return Booger("LazyTestCase")

    def test_one(self):
        self.boog
        print("one")

    def test_two(self):
        self.boog
        print("two")

class TestCaseWithSetupClassBoogers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.thing = Booger("TestCaseWithSetupClassBoogers", scope='class')

    def test_one(self):
        print("one")

    def test_two(self):
        print("two")
