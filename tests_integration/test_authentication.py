import os
import requests


def test_can_authenticate_faveo():
    username = os.environ.get("FAVEO_USERNAME")
    password = os.environ.get("FAVEO_PASSWORD")
    base_url = os.environ.get("FAVEO_BASE_URL")
    authenticate_url = base_url + 'api/v1/authenticate'
    headers = {'Content-Type': 'application/json'}

    response = requests.post(
        authenticate_url,
        params={'username': username, 'password': password},
        headers=headers)

    response.raise_for_status()
    assert(response.status_code == 200)
    assert('token' in response.json().get('data').keys())


def test_can_authenticate_sap():
    username = 'dchot'
    password = '1234567'
    base_url = 'http://athena.grupopuntacana.com:8000'
    headers = {'Content-Type': 'application/json',
               'X-CSRF-Token': 'Fetch'}

    url_test = '/api_portal_clie/crear_aviso?sap-client=300'

    response = requests.get(
        base_url + url_test,
        auth = requests.auth.HTTPBasicAuth(username, password),
        headers=headers)
    
    assert(response.status_code == 200)
    assert(response.content == b'You called GET Method!')