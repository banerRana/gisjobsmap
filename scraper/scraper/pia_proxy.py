import os
import socket

import requests
import socks


class Proxy():

    def __init__(self):
        self.s = socks.socksocket()
        self.socket = socket
        self._proxy_list = []
        self.proxy = None  # current active proxy
        self.test_url = 'http://www.indeed.com'

        # connection credentials
        self.url = os.environ.get('PROXY_URL')
        self.user = os.environ.get('PROXY_USER')
        self.pw = os.environ.get('PROXY_PW')

    def retrieve_proxies_list(self):
        try:
            self._proxy_list = []
            ais = socket.getaddrinfo(self.url, 0, 0, 0, 0)
            for a in ais:
                proxy_val = a[-1][0]
                if proxy_val not in self._proxy_list:
                    self._proxy_list.append(a[-1][0])
        except Exception as e:
            print(f'Error retrieving proxy addresses: {e}')
        finally:
            return

    def get_proxy_dict(self, proxy):
        return {
            'http': "socks5://{}:{}@{}:{}".format(self.user, self.pw, proxy, 1080),
            'https': "socks5://{}:{}@{}:{}".format(self.user, self.pw, proxy, 1080),
        }

    def is_valid_proxy(self, url, proxy):
        r = requests.get(url, proxies=self.get_proxy_dict(proxy), timeout=2.5)
        if r.ok:  # proxy success
            return True
        return False

    def retrieve_proxy(self, testurl):
        print("switching proxy...")
        self.test_url = testurl
        self.proxy = None
        while self.proxy is None:
            self.retrieve_proxies_list()
            for val in self._proxy_list:
                try:
                    if self.is_valid_proxy(testurl, val):
                        self.proxy = self.get_proxy_dict(val)
                        break
                except Exception as e:
                    continue
