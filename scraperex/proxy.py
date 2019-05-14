import re
import requests
import collections

from ._config import DEFAULT_PROXY_RESOURCES, DEFAULT_REQUEST_ATTEMPTS

class ProxyGenerator(object):

    __proxyList = []

    __proxyIterator = None

    def getProxyList(self) -> list:
        if ( not self.__proxyList ):
            self.setProxyList(self.__getDefaultProxyList(DEFAULT_REQUEST_ATTEMPTS))
        return self.__proxyList

    def setProxyList(self, proxyList: list):
        self.__proxyList = proxyList

    def getNextProxy(self) -> dict:
        if ( not self.__proxyIterator or not isinstance(self.__proxyIterator, collections.Iterable) ):
            self.__proxyIterator = iter(self.getProxyList())
        proxy = next(self.__proxyIterator)
        return {
            "http": proxy,
            "https": proxy
        }

    def __getDefaultProxyList(self, attempts: int = 0) -> list:

        # TODO: use proxy servers api
        url = "https://www.proxy-list.download/api/v1/get"
        payload = {'type':'https', 'country':'US'}
        response = requests.get(url, params=payload)
        print(response.text)

        ##

        list = []
        resource = DEFAULT_PROXY_RESOURCES[0]
        try:
            response = requests.get(resource)
        except:
            print('Can\'t connect to default proxy list resource.')
            exit()
        if response.status_code != 200:
            if ( attempts > 0 ):
                attempts -= 1
                response = self.__getDefaultProxyList(attempts)
            else:
                raise Exception('Can\'t retrieve proxy list from '+resource)
                exit()
        return self.__filterProxyListResponse(response.text)

    def __filterProxyListResponse(self, content) -> list:
        list = []
        ips = re.findall('<td>([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})</td>', content, flags=re.IGNORECASE)
        ports = re.findall('<td>([\d]+)</td>', content, flags=re.IGNORECASE)
        if ( len(ips) != len(ports) ):
            raise Exception('Can\'t find full list of proxy ips.')
        for index in range(len(ips)):
            list.append(ips[index]+':'+ports[index])
        return list