import json
import unittest
from exchange_app import app


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_address_valid(self):
        data = dict(address=r'2GgFvqoyk9RjwVzj8tqfcXVXB4orBwoc9qv')
        response = self.app.get(
            '/api/v1.0/addresses/{}/isvalid'.format(data), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['isValid'], True)

    def test_address_invalid(self):
        data = dict(address=r'12345678')
        response = self.app.get(
            '/api/v1.0/addresses/{}/isvalid'.format(data), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['isValid'], False)

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
