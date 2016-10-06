import unittest

import mock

from booger import Booger


class TestCaseWithSetupBoogers(unittest.TestCase):
    def setUp(self):
        self.thing = Booger()

    def test_one(self):
        print("one")
        pass

    def test_two(self):
        print("two")
        pass


class MockedTestCase(unittest.TestCase):
    @mock.patch('os.listdir', Booger())
    def test_with_mock(self):
        pass
