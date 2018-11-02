import os
from requests import Session
from requests.auth import HTTPBasicAuth
from .base import BaseAPIClient
from .exceptions import CantAuthenticate, NotSetEnviromentVariable


class APIClient(BaseAPIClient):
    base_url = os.environ.get('SAP_BASE_URL', None)
    _params_base = {'sap-client': os.environ.get('SAP_CLIENT')}
    _username = os.environ.get('SAP_USERNAME', None)
    _password = os.environ.get('SAP_PASSWORD', None)
    _authentication_url = '/portal_clientes/lista_servicios?sap-client=300'
    _authenticated = False

    def authenticate(self, exception=CantAuthenticate):
        """
        Method to authenticate with Faveo.
        """
        if not self._username and not self._password:
            msg = 'You need to put the oracle environment variables.'
            raise NotSetEnviromentVariable(msg)

        session = Session()
        session.auth = (self._username, self._password) 
        session.headers.update(
            {'Content-type': 'application/json',
             'X-CSRF-Token': 'Fetch'})

        response = session.get(
            self.base_url + self._authentication_url)

        if response.status_code == 200:
            token = response.headers.get('x-csrf-token')
            session.headers.update({'X-CSRF-Token': token})
            self._lib = session
            self._authenticated = True

        if response.status_code == 403:
            raise exception(response.content)

        return self._authenticated