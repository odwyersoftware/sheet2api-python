import logging

from requests.auth import HTTPBasicAuth
import requests

logger = logging.getLogger(__name__)


class Sheet2APIClient:
    def __init__(self, *, api_url, username=None, password=None):
        self._base_url = api_url.rstrip('/') + '/'
        self._auth = None
        if username:
            self._auth = HTTPBasicAuth(username, password)

    def read_rows(self, *, sheet=None, query=None):
        url = self._url(sheet=sheet)
        logger.info('Reading rows from sheet %s within %s...', sheet, url)
        resp = self._request('get', url, params=query)
        return resp.json()

    def delete_rows(self, *, sheet=None, query=None):
        url = self._url(sheet=sheet)
        logger.info('Deleting rows from sheet %s within %s...', sheet, url)
        resp = self._request('delete', url, params=query)
        return resp.ok

    def create_row(self, *, row, sheet=None):
        url = self._url(sheet=sheet)
        logger.info('Creating row in sheet %s within %s...', sheet, url)
        resp = self._request('post', url, json=row)
        return resp.json()

    def update_rows(self, *, row, sheet=None, query=None,
                    partial_update=False):
        url = self._url(sheet=sheet)
        logger.info('Updating rows from sheet %s within %s...', sheet, url)
        method = 'patch' if partial_update else 'put'
        resp = self._request(method, url, json=row, params=query)
        return resp.json()

    def _request(self, method, url, **kwargs):
        resp = getattr(requests, method)(url, auth=self._auth, **kwargs)
        resp.raise_for_status()
        return resp

    def _url(self, sheet=None):
        url = self._base_url
        if sheet:
            url = f'{url}{sheet}/'
        return url
