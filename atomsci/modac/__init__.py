import logging
import os
import requests

from requests.auth import HTTPBasicAuth

BASE_URL = 'https://modac.cancer.gov/api'

_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)

def authenticate():
    url = "/".join((BASE_URL, 'authenticate'))
    auth_resp = requests.get(url, auth=_auth_headers())
    auth_resp.raise_for_status()
    return auth_resp


def _auth_headers():
    username = os.getenv('MODAC_USER')
    password = os.getenv('MODAC_PASS')
    if not username or not password:
        _logger.warn("Define your MODAC username by setting MODAC_USER='my-username'\nAlternatively, you can call os.environ['MODAC_USER'] = 'my-username'")
        _logger.warn("Define your MODAC username by setting MODAC_PASS='my-password'\nAlternatively, you can call os.environ['MODAC_PASS'] = 'my-password'")
        raise Exception("Undefined username and/or password")
    return HTTPBasicAuth(username=username, password=password)
