import unittest

import ddt
import mock

from booger import Booger


class TestCaseWithSetupBoogers(unittest.TestCase):
    def setUp(self):
        self.thing = Booger("TestCaseWithSetupBoogers")

    def test_one(self):
        print("one")
        pass

    def test_two(self):
        print("two")
        pass


class MockedTestCaseMethod(unittest.TestCase):
    @mock.patch('os.listdir', Booger("test_with_mock"))
    def test_with_mock(self):
        pass


@mock.patch('os.listdir', Booger("MockedTestCaseClass", scope='class'))
class MockedTestCaseClass(unittest.TestCase):
    def test_first(self):
        pass

    def test_second(self):
        pass


@ddt.ddt
class DataTestCase(unittest.TestCase):

    if 0:
        @ddt.data(
            Booger("DataTestCase", scope='class'),
            Booger("DataTestCase", scope='class'),
        )
        def test_boogers(self, boog):
            self.assertIsInstance(boog, Booger)

    @ddt.data(
        (1, 2),
        (2, 4),
        (1000, 2000),
    )
    @mock.patch('os.listdir', Booger("DataTestCase", scope='class'))
    def test_double(self, ab):
        self.assertEqual(2*ab[0], ab[1])

    @mock.patch('os.listdir', Booger("DataTestCase", scope='class'))
    @ddt.data(
        (1, 3),
        (2, 6),
        (1000, 3000),
    )
    def test_triple(self, ab):
        self.assertEqual(3*ab[0], ab[1])
