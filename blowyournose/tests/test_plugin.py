import unittest

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


@mock.patch('os.listdir', Booger("MockedTestCaseClass", when='class'))
class MockedTestCaseClass(unittest.TestCase):
    def test_first(self):
        pass

    def test_second(self):
        pass
