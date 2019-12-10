"""Tests for `oraculo` package."""
import os
import unittest
from mock import patch, MagicMock
from oraculo.gods import azul, exceptions


class TestAPIClient(unittest.TestCase):

    def test_initial_attribute(self):
        # WHEN
        client = azul.APIClient

        # THEN
        self.assertEqual(client._authenticated, False)
        self.assertIsNotNone(client.host)
        self.assertIsNotNone(client.auth_one)
        self.assertIsNotNone(client.auth_two)
        self.assertIsNotNone(client.certificate)
        self.assertIsNotNone(client.certificate_key)

    def test_success_authentication(self):
        # WHEN
        instance_client = azul.APIClient()

        # THEN
        self.assertEqual(instance_client._authenticated, True)
        self.assertIn('Auth1', instance_client._headers_base)
        self.assertIn('Auth2', instance_client._headers_base)

    def test_success_post(self):
        # GIVEN
        url = '/webservices/JSON/Default.aspx'

        body = {
            "AcquirerRefData": '1',
            "Amount": '1000',
            "CVC": "977",
            "CardNumber": "4035874000424977",
            "Channel": "EC",
            "CurrencyPosCode": "$",
            "CustomerServicePhone": "",
            "ECommerceURL": "https://app.puntacana.com",
            "Expiration": "202012",
            "ITBIS": "",
            "OrderNumber": "",
            "Payments": 1,
            "Plan": 0,
            "PosInputMode": "E-Commerce",
            "SaveToDataVault": "1",
            "Store": "39038540035",
            "TrxType": "Sale",
        }

        # WHEN
        response = azul.APIClient().post(url, body)

        # THEN
        self.assertIsInstance(response, dict)
