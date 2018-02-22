import json
import unittest
from exchange_app import app


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_address_valid(self):
        pass

    def test_get_assets(self):
        pass

    def test_get_asset(self):
        pass

    def test_pending_events_cashin(self):
        pass

    def test_pending_events_cashin(self):
        pass

    def test_pending_events_cashout_failed(self):
        pass

    def test_pending_events_cashout_started(self):
        pass

    def test_wallets(self):
        pass

    def test_wallets_cashout(self):
        pass


if __name__ == '__main__':
    unittest.main()
