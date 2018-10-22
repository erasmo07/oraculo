# -*- coding: utf-8 -*-

"""Main module."""
import os
import requests
from .base import BaseAPIClient
from .exceptions import CantAuthenticate, NotSetEnviromentVariable


class APIClient(BaseAPIClient):
    base_url = 'http://faveo.grupopuntacana.com:81/'

    _username = os.environ.get("FAVEO_USERNAME", None)
    _password = os.environ.get("FAVEO_PASSWORD", None)
    _authenticated = False
    _authenticate_url = base_url + 'api/v1/authenticate'

    def authenticate(self, exception=CantAuthenticate):
        """
        Method to authenticate with Faveo.
        """
        if not self._username and not self._password:
            msg = 'You need to put the oracle environment variables.'
            raise NotSetEnviromentVariable(msg)

        params = {'username': self._username, 'password': self._password}
        response = requests.post(
            self._authenticate_url,
            params=params, headers=self._headers_base)

        if response.status_code == 200:
            result = response.json()
            token = result.get('data').get('token')
            self._params_base.update(dict(token=token))
            self._authenticated = True

        if response.status_code == 403:
            raise exception('msg')

        return self._authenticated
