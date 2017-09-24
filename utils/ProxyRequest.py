# -*- coding: utf-8 -*-
import urllib2
import StringIO
import urllib

import socks
from sockshandler import SocksiPyHandler
import gzip


class ProxyRequests(object):
    @staticmethod
    def install_proxy(host, port, proxy_type=socks.HTTP):
        """
        :param host: proxy host
        :param port: proxy ip
        :param proxy_type: proxy type
        SOCKS4 = 1
        SOCKS5 = 2
        HTTP = 3
        """
        if proxy_type not in (socks.SOCKS5, socks.SOCKS4, socks.HTTP):
            raise RuntimeError("Not support proxy type")
        proxy = urllib2.ProxyHandler({'http': host + ":" + port}) if proxy_type == 1 \
            else SocksiPyHandler(proxy_type, host, port)
        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPSHandler(debuglevel=1), proxy)
        urllib2.install_opener(opener)

    @staticmethod
    def request(url, data=None, method='GET', headers=None, timeout=None):
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        if method and method.upper() == "GET":
            req = urllib2.Request((url if url.endswith("?") else url + "?") + urllib.urlencode(data),
                                  headers=headers)
        else:
            req = urllib2.Request(url, data=urllib.urlencode(data), headers=headers)
        return urllib2.urlopen(req, timeout=timeout)

    @staticmethod
    def unzip(data):
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data


if __name__ == '__main__':
    ProxyRequests.install_proxy('127.0.0.1', 1080, socks.SOCKS5)
    # ProxyRequests.install_proxy('127.0.0.1', 8888, socks.HTTP)
    response = ProxyRequests.request('https://google.com')
    print (response.read())
