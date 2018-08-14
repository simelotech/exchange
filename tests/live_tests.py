import unittest
from exchange_app import app

class LiveTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_test(self):
        self.assertEqual(100, 100)
