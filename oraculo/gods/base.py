import abc
import json
import requests 
from .exceptions import (
    NotFound, BadRequest, CantAuthenticate,
    InternalServer, NotHasResponse)


class BaseAPIClient(abc.ABC):
    _headers_base = {'content-type': 'application/json'}
    _params_base = dict()
    _auth = None 
    _lib = requests 

    @property
    @abc.abstractmethod
    def base_url(self):
        return 'Should set base_url property'

    def __init__(self):
        self.authenticate()

    @abc.abstractmethod
    def authenticate(self, exception=CantAuthenticate):
        """Method documentation"""
        return

    def get(self, url, params=dict()):
        """Method documentation"""
        params.update(self._params_base)
        request = self._lib.get(
            self.base_url + url,
            params=params,
            headers=self._headers_base)

        if request.status_code is 200:
            return request.json()

        if request.status_code is 401:
            self.authenticate()
            self.get(url, params)

        if request.status_code is 403:
            self.authenticate()
            self.get(url, params)

        if request.status_code is 404:
            raise NotFound(request.context)
        
        if request.status_code == 500:
            raise InternalServer(request.content)
        raise NotHasResponse(request.content)

    def post(self, url, body, params=dict()):
        params.update(self._params_base)

        request = self._lib.post(
            self.base_url + url,
            data=json.dumps(body),
            headers=self._headers_base,
            params=params)

        if request.status_code == 200:
            return request.json()

        if request.status_code == 400:
            raise BadRequest(request.content)

        if request.status_code == 401:
            self.authenticate()
            self.get(url, params)

        if request.status_code == 403:
            self.authenticate()
            self.post(url, body)

        if request.status_code == 404:
            raise NotFound(request.content)
        
        if request.status_code == 500:
            raise InternalServer(request.content)
        raise NotHasResponse(request.content)

    def patch(self, url, pk):
        url = "{self.base_url}{url}/{pk}"
        request = self._lib.patch(
            url=url,
            headers=self._headers_base,
            params=self._params_base)
