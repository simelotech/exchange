import json
import unittest
from exchange_app import app


class APITestCase(unittest.TestCase):

    exchange_prefix = "/v1/api"

    def setUp(self):
        self.app = app.test_client()

    def test_is_alive(self):
        response = self.app.get(
            self.exchange_prefix + '/isalive', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('name', json_response)
        self.assertIn('version', json_response)
        self.assertIn('env', json_response)
        self.assertIn('isDebug', json_response)

if __name__ == '__main__':
    unittest.main()
