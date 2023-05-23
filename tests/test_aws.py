import unittest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError
from aws import get_secret
import boto3

class TestGetSecret(unittest.TestCase):
    def setUp(self):
        self.secret_name = "test-secret-name"
        self.expected_secret_value = "test-secret-value"
        self.mock_client = MagicMock()
        self.mock_client.get_secret_value.return_value = {
            'SecretString': f'{{"{self.secret_name}": "{self.expected_secret_value}"}}'
        }
        self.original_session_client = boto3.session.Session.client
        boto3.session.Session.client = MagicMock(return_value=self.mock_client)

    def tearDown(self):
        boto3.session.Session.client = self.original_session_client

    def test_get_secret(self):
        secret_value = get_secret("test-secret-name")
        self.assertEqual(secret_value, "test-secret-value")
        self.mock_client.get_secret_value.assert_called_once_with(SecretId=self.secret_name)

if __name__ == '__main__':
    unittest.main()
