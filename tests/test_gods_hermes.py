"""Tests for `oraculo` package."""
import os
import unittest
from mock import patch, MagicMock
from oraculo.gods import hermes, exceptions


class TestAPIClient(unittest.TestCase):

    def test_initial_attribute(self):
        # GIVEN
        base_url = os.environ.get('HERMES_BASE_URL')

        # WHEN
        client = hermes.APIClient

        # THEN
        self.assertEqual(client._authenticated, False)
        self.assertEqual(
            client.base_url, base_url)
        _authenticate_url = base_url + ''
        self.assertEqual(client._authenticate_url, _authenticate_url)

    def test_success_authentication(self):
        # WHEN
        instance_client = hermes.APIClient()

        # THEN
        self.assertEqual(instance_client._authenticated, True)
