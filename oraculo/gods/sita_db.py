# -*- coding: utf-8 -*-

"""Main module."""
import os
import requests
from .base import BaseAPIClient
from .exceptions import CantAuthenticate, NotSetEnviromentVariable


class APIClient(BaseAPIClient):
    base_url = os.environ.get('SITA_DB_BASE_URL', None)

    _authenticated = False

    def authenticate(self, exception=CantAuthenticate):
        """
        Method to authenticate with Faveo.
        """
        if not self.base_url:
            msg = 'You need to put the oracle environment variables.'
            raise NotSetEnviromentVariable(msg)

        _authenticate_url = self.base_url + 'api/v1/ping/'
        response = requests.post(
            _authenticate_url,
            headers=self._headers_base)

        if response.status_code == 200:
            self._authenticated = True

        if response.status_code == 403:
            raise exception('msg')

        return self._authenticated

