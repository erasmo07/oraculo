# -*- coding: utf-8 -*-

"""Main module."""
import requests


class CantAuthenticate(Exception):
    pass


class NotFound(Exception):
    pass


class APIClient(object):
    _authenticated = False
    _base_url = 'http://faveo.grupopuntacana.com:81'
    _authenticate_url = _base_url + '/api/v1/autenticate/'

    def __init__(self):
        self.authenticate()

    def authenticate(self, exception=CantAuthenticate):
        """
        Method to authenticate with Faveo.
        """
        params = {'username': 'username', 'password': 'password'}
        request = requests.get(self._authenticate_url, params=params)

        if request.status_code == 200:
            self._authenticated = True

        if request.status_code == 403:
            raise exception('msg')

        return self._authenticated

    def get(self, url, params=None):
        request = requests.get(self._base_url + url, params=params)

        if request.status_code is 200:
            return request.json()

        if request.status_code is 403:
            self.authenticated()
            self.get(url, params)

        if request.status_code is 404:
            raise NotFound(request.context)

    def post(self, url, body):
        request = requests.post(self._base_url + url, data=body)

        if request.status_code == 200:
            return request.json()

        if request.status_code == 403:
            self.authenticated()
            self.post(url, body)

        if request.status_code == 404:
            raise NotFound(request.context)
