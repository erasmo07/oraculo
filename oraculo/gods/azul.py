"""Main module."""
import os
import json
import ssl
import http.client
from .base import BaseAPIClient, logger
from .exceptions import CantAuthenticate, NotSetEnviromentVariable


class APIClient(BaseAPIClient):
    host = os.environ.get('AZUL_HOST', None)
    auth_one = os.environ.get('AZUL_AUTH_ONE', None)
    auth_two = os.environ.get('AZUL_AUTH_TWO', None)
    certificate = os.environ.get('AZUL_CERTIFICATE_PATH', None)
    certificate_key = os.environ.get('AZUL_CERTIFICATE_KEY_PATH', None)
    _authenticated = False

    def authenticate(self, exception=CantAuthenticate):
        """
        Method to authenticate with Azul.
        """
        if (
            not self.base_url
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
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.load_cert_chain(self.certificate, keyfile=self.certificate_key)
        return context

    def get_connection(self, port=443):
        return http.client.HTTPSConnection(
            self.host, port=port, context=self.get_context())

    def post(self, url, body, params=dict(), **kwargs):
        connection = self.get_connection()
        connection.request(
            method="POST",
            url=url,
            headers=self._headers_base,
            body=json.dumps(body))
        
        call_message = "METHOD: {0} URL: {1} - BODY: {2}".format('POST', url, body)
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
