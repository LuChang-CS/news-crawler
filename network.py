import weakref
import requests

from configobj import ConfigObj

class NetWorkConfiguration:

    HTTP_TIMEOUT = 30
    STRICT = True
    USER_AGENT = 'Mozilla'

    def __init__(self):
        self.browser_user_agent = self.USER_AGENT
        self.http_timeout = self.HTTP_TIMEOUT
        self.strict = self.STRICT

    def load(self, path):
        config = ConfigObj(path, encoding='UTF-8')
        self.browser_user_agent = config.get('browser_user_agent', self.USER_AGENT)
        self.http_timeout = int(config.get('http_timeout', self.HTTP_TIMEOUT))
        self.strict = bool(config.get('strict', self.STRICT))


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
        response = self._connection.get(url, timeout=self.config.http_timeout, headers=self.headers)
        if response.ok:
            self._url = response.url
            text = response.content
        else:
            self._url = None
            text = None
            if self.config.strict:
                raise NetworkError(response.status_code, response.reason)

        return text
