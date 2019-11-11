"""Main module."""
import os
import requests
from .base import BaseAPIClient, logger
from .exceptions import CantAuthenticate, NotSetEnviromentVariable


class APIClient(BaseAPIClient):
    base_url = os.environ.get('SITA_BASE_URL', None)
    base_token = os.environ.get('SITA_TOKEN', '6aed03fa-93f1-4733-b71d-a25935e318df')

    _authenticated = False
    _headers_base = {'Content-type': 'text/xml'}

    def authenticate(self, exception=CantAuthenticate):
        """
        Method to authenticate with Faveo.
        """
        if not self.base_url and self.base_token:
            msg = 'You need to put the oracle environment variables.'
            raise NotSetEnviromentVariable(msg)

        self._authenticated = True
        return self._authenticated

    def post(self, url, body, params=dict()):
        params.update(self._params_base)

        if not self._authenticated:
            self.authenticate()

        url = self.base_url + url
        response = self._lib.post(url, data=body, headers=self._headers_base)

        call_message = "METHOD: {0} URL: {1} - BODY: {2} - PARAMS: {3}".format(
            response.request.method, response.request.url, body, params)
        logger.info(call_message)

        if response.status_code == 401:
            self._authenticated = False
            self.authenticate()
            return self.post(url , body=body, params=params)
        
        if response.status_code == 403:
            self._authenticated = False
            self.authenticate()
            return self.post(url , body=body, params=params)
        
        if response.status_code == 200:
            return response

        return self.return_value(response)