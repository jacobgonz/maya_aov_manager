import unittest


class InitializationTests(unittest.TestCase):

    def test_initialization(self):
        """
        Check the test suite runs by affirming 2+2=4

        :return:
        """

        self.assertEqual(2+2, 4)

    def test_import(self):
        """
        Ensure the test unit can import our module
        :return:
        """

        try:
            import aov_manager
        except ImportError:
            self.fail("Was not able to import the aov_manager module")
