import logging
import os
import requests

from requests.auth import HTTPBasicAuth

BASE_URL = "https://modac.cancer.gov/api"

_token = None
_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)


def authenticate() -> bool:
    global _token
    url = "/".join((BASE_URL, "authenticate"))
    auth_resp = requests.get(url, auth=_login_headers())
    auth_resp.raise_for_status()
    _token = auth_resp.content.decode("utf-8")
    return True


def download_asset_files(path: str) -> bool:
    global _token
    if not _token:
        authenticate()

    url = "/".join((BASE_URL, "v2", "dataObject", path, "download"))
    _logger.warning(f"Making requests to {url}")
    resp = requests.post(url, headers=_token_headers(), json={})
    resp.raise_for_status()
    local_filename = url.split("/")[-2]
    with open(local_filename, "wb") as f:
        f.write(resp.content)
    return True


def _token_headers() -> dict:
    global _token
    headers = {"Authorization": f"Bearer {_token}"}
    return headers


def _login_headers() -> HTTPBasicAuth:
    username = os.getenv("MODAC_USER")
    password = os.getenv("MODAC_PASS")
    if not username or not password:
        _logger.warning(
            "Define your MODAC username by setting MODAC_USER='my-username'\nAlternatively, you can call os.environ['MODAC_USER'] = 'my-username'"
        )
        _logger.warning(
            "Define your MODAC username by setting MODAC_PASS='my-password'\nAlternatively, you can call os.environ['MODAC_PASS'] = 'my-password'"
        )
        raise Exception("Undefined username and/or password")
    return HTTPBasicAuth(username=username, password=password)
