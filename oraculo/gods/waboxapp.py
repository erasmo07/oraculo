import os
import requests
from .base import BaseAPIClient
from .exceptions import CantAuthenticate, NotSetEnviromentVariable


class APIClient(BaseAPIClient):
    base_url = os.environ.get('WABOXAPP_BASE_URL', None)
    _authenticated = False
    _params_base = dict()

    def authenticate(self, exception=CantAuthenticate):
        """
        Method to authenticate with Faveo.
        """
        uid = os.environ.get('WABOXAPP_UID')
        token = os.environ.get('WABOXAPP_TOKEN')
        if not uid or not token or not self.base_url:
            msg = 'You need to put the WABOXAPP environment variables.'
            raise NotSetEnviromentVariable(msg)

        self._params_base.update(dict(uid=uid, token=token))
        self._authenticated = True
        return self._authenticated