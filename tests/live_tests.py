import unittest
import os
from exchange_app import app
import json

class LiveTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_test(self):
        seeds_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                *('data/skycoin/seeds.json'.split('/')))
        file = open(seeds_path, "r")
        text = file.read()
        seeds = json.loads(text)
        file.close()
