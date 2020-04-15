"""Main module."""
import os
import json
import ssl
import http.client
from .base import BaseAPIClient, logger
from .exceptions import CantAuthenticate, NotSetEnviromentVariable


class APIClient(BaseAPIClient):
    default_store = os.environ.get('AZUL_DEFAULT_STORE', None)
    host = os.environ.get('AZUL_HOST', None)
    certificate = os.environ.get('AZUL_CERTIFICATE_PATH', None)
    certificate_key = os.environ.get('AZUL_CERTIFICATE_KEY_PATH', None)
    connection_class = http.client.HTTPSConnection

    _authenticated = False
    _connection = None

    def __init__(self, store=None):
        self.store = store if store else self.default_store
        super(APIClient, self).__init__()

    @property
    def auth_one(self):
        value = os.environ.get('AZUL_%s_AUTH_ONE' % self.store)
        if not value:
            raise NotSetEnviromentVariable(
                'Need set Auth One to %s store' % self.store)
        return value

    @property
    def auth_two(self):
        value = os.environ.get('AZUL_%s_AUTH_TWO' % self.store)
        if not value:
            raise NotSetEnviromentVariable(
                'Need set Auth Two to %s store' % self.store)
        return value

    def authenticate(self, exception=CantAuthenticate):
        """
        Method to authenticate with Azul.
        """
        if (
            not self.host
            and not self.auth_one
            and not self.auth_two
            and not self.certificate
            and not self.certificate_key
        ):
            raise NotSetEnviromentVariable(
                'You need to put the environment variables for Azul.')

        self._authenticated = True
        self._headers_base.update(
            {'Auth1': self.auth_one, 'Auth2': self.auth_two}
        )
        return self._authenticated

    def get_context(self):
        """
        The way to load certification was provide for larsks on
        Stackoverflow, here are links.

        Solution:
            https://stackoverflow.com/questions/30109449/\
                what-does-sslerror-ssl-pem-lib-ssl-c2532-\
                    mean-using-the-python-ssl-libr
        Autor:
            https://stackoverflow.com/users/147356/larsks
        """
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(self.certificate, keyfile=self.certificate_key)
        return context

    def get_connection(self, port=443):
        if not self._connection:
            self._connection = self.connection_class(
                self.host, port=port, context=self.get_context())
        return self._connection

    def post(self, url, body, params=dict(), **kwargs):
        connection = self.get_connection()
        connection.request(
            method="POST",
            url=url,
            headers=self._headers_base,
            body=json.dumps(body))

        call_message = "METHOD: {0} URL: {1} - BODY: {2}".format(
            'POST', url, body)
        logger.info(call_message)

        response = connection.getresponse()
        return self.return_value(response)

    def return_value(self, response):
        if response.status == 200:
            try:
                content = response.read()
                return json.loads(content.decode())
            except json.decoder.JSONDecodeError:
                return {'message': 'Cant decode json response', 'content': content}

        response.status_code = response.status
        return super(APIClient, self).return_value(response)

    def __del__(self):
        if self._connection:
            self._connection.close()
