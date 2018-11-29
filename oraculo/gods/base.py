import abc
import json
import requests 
import logging 
from .exceptions import (
    NotFound, BadRequest, CantAuthenticate,
    InternalServer, NotHasResponse, Forbidden,
    Unauthorized)


logging.basicConfig(format='%(asctime)s %(message)s') 
logger = logging.getLogger() 
logger.setLevel(logging.INFO) 


class BaseAPIClient(abc.ABC):
    _auth = None 
    _headers_base = {'content-type': 'application/json'}
    _params_base = dict()
    _lib = requests 
    _refresh_token_status = [401, 403]
    _authenticated = None 

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

        if not self._authenticated:
            self.authenticate()

        response = self._lib.get(
            self.base_url + url,
            params=params,
            headers=self._headers_base)

        call_message = "METHOD: {2} URL: {0} - PARAMS: {1}".format(
            response.request.url, params, response.request.method)
        logger.info(call_message)
        
        if response.status_code == 401:
            self.authenticate()
            self.get(url , params=params)

        if response.status_code == 403:
            self.authenticate()
            self.get(url, params)

        return self.return_value(response)

    def post(self, url, body, params=dict()):
        params.update(self._params_base)

        if not self._authenticated:
            self.authenticate()
        
        response = self._lib.post(
            self.base_url + url,
            data=json.dumps(body),
            headers=self._headers_base,
            params=params)

        call_message = "URL: {0} - BODY: {1} - PARAMS".format(
            response.request.url, body, params)
        logger.info(call_message)

        if response.status_code == 401:
            self.authenticate()
            self.post(url , body=body, params=params)
        
        if response.status_code == 403:
            self.authenticate()
            self.post(url , body=body, params=params)

        return self.return_value(response)
        

    def patch(self, url, pk):
        url = "{self.base_url}{url}/{pk}"

        if not self._authenticated:
            self.authenticate()

        response = self._lib.patch(
            url=url,
            headers=self._headers_base,
            params=self._params_base)
        
        if response.status_code == 401:
            self.authenticate()
            self.patch(url , pk=pk)
        
        if response.status_code == 403:
            self.authenticate()
            self.patch(url , pk=pk)

        return self.return_value(response)

    def return_value(self, request):
        if request.status_code == 200:
            try:
                return request.json()
            except json.decoder.JSONDecodeError:
                return {}

        if request.status_code == 400:
            raise BadRequest(request.content)

        if request.status_code == 401:
            raise Unauthorized(request.content)

        if request.status_code == 403:
            raise Forbidden(request.content)

        if request.status_code == 404:
            raise NotFound(request.content)
        
        if request.status_code == 500:
            raise InternalServer(request.content)
        raise NotHasResponse(request.content)