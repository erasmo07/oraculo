import os
import requests
from .base import BaseAPIClient
from .exceptions import CantAuthenticate, NotSetEnviromentVariable


class APIClient(BaseAPIClient):
    base_url = os.environ.get('HERMES_BASE_URL', None)
    _authenticate_url = base_url + ''
    _authenticated = False
    _params_base = dict()

    def authenticate(self, exception=CantAuthenticate):
        """
        Method to authenticate with Faveo.
        """
        if not self.base_url:
            msg = 'You need to put the HERMES environment variables.'
            raise NotSetEnviromentVariable(msg)

        self._authenticated = True
        return self._authenticated