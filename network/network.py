import weakref
import requests

from settings.configuration import Configuration


class NetWorkConfiguration(Configuration):

    HTTP_TIMEOUT = 30
    STRICT = True
    USER_AGENT = 'Mozilla'

    def _init_properties(self):
        return [
            ['browser_user_agent', 'Mozilla', str],
            ['http_timeout', 30, int],
            ['strict', True, lambda v: str(v) == 'True']
        ]


class NetworkError(RuntimeError):

    def __init__(self, status_code, reason):
        self.reason = reason
        self.status_code = status_code


class NetworkFetcher(object):

    def __init__(self):
        self.config = NetWorkConfiguration()
        self.config.load('./settings/network.cfg')

        self._connection = requests.Session()
        self._connection.headers['User-agent'] = self.config.browser_user_agent
        self._finalizer = weakref.finalize(self, self.close)

        self._url = None
        self.response = None
        self.headers = None

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def get_url(self):
        return self._url

    def fetch(self, url):
        try:
            response = self._connection.get(url, timeout=self.config.http_timeout, headers=self.headers)
        except Exception:
            return None
        if response.ok:
            self._url = response.url
            text = response.content
        else:
            self._url = None
            text = None
            if self.config.strict:
                raise NetworkError(response.status_code, response.reason)

        return text
