import json
import unittest
from exchange_app import app


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_assets(self):
        response = self.app.get(
            '/api/v1.0/assets', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_asset(self):
        data = dict(assetid=1)
        response = self.app.get(
            '/api/v1.0/assets',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_pending_events_cashin(self):
        response = self.app.get(
            '/api/v1.0/pending-events/cashin',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_pending_events_cashout_started(self):
        response = self.app.get(
            '/api/v1.0/pending-events/cashout-started',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_pending_events_cashout_completed(self):
        response = self.app.get(
            '/api/v1.0/pending-events/cashout-completed',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_pending_events_cashout_failed(self):
        response = self.app.get(
            '/api/v1.0/pending-events/cashout-failed',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)


    def test_api_capabilities(self):
        response = self.app.get(
            '/api/v1.0/capabilities', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('isTransactionsRebuildingSupported', json_response)
        self.assertIn('areManyInputsSupported', json_response)
        self.assertIn('areManyOutputsSupported', json_response)


if __name__ == '__main__':
    unittest.main()
