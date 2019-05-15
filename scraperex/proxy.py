import re
import requests
import collections

from ._config import DEFAULT_PROXY_WEB_RESOURCES, DEFAULT_REQUEST_ATTEMPTS, DEFAULT_PROXY_API_RESOURCES

class ProxyGenerator(object):

    __proxyList = []
    __proxyListSecured = []

    __proxyIterator = None
    __proxyIteratorSecured = None

    __secured = False

    def getNextProxy(self, secured = False) -> dict:
        self.__secured = secured
        iterator = self.__getProxyIterator()
        proxy = next(iterator, False)
        if not self.__secured:
            return { "http": proxy }
        return { "https": proxy }

    def __getProxyIterator(self):
        iterator = self.__proxyIterator if not self.__secured else self.__proxyIteratorSecured
        if ( not iterator or not isinstance(iterator, collections.Iterable) ):
            self.__setProxyIterator(iter(self.getProxyList(self.__secured)))
        return self.__proxyIterator if not self.__secured else self.__proxyIteratorSecured

    def getProxyList(self, secured) -> list:
        proxyList = self.__proxyList if not self.__secured else self.__proxyListSecured
        if ( not proxyList ):
            self.setProxyList(self.__getDefaultProxyList())
        return self.__proxyList if not self.__secured else self.__proxyListSecured

    def __setProxyIterator(self, proxyIterator):
        if not self.__secured:
            self.__proxyIterator = proxyIterator
        else:
            self.__proxyIteratorSecured = proxyIterator

    def setProxyList(self, proxyList: list):
        if not self.__secured:
            self.__proxyList = proxyList
        else:
            self.__proxyListSecured = proxyList

    def __getDefaultProxyList(self) -> list:
        proxyList = self.__retry(DEFAULT_REQUEST_ATTEMPTS, self.__getApiProxyList)
        proxyList = []
        if not proxyList and not self.__secured:
            proxyList = self.__retry(DEFAULT_REQUEST_ATTEMPTS, self.__getWebProxyList)
        return proxyList

    def __getApiProxyList(self) -> list:
        proxyList = []
        url = DEFAULT_PROXY_API_RESOURCES
        protocol = 'http' if not self.__secured else 'https'
        params = { 'type': protocol }
        response = requests.get(url, params)
        if (response.status_code == 200):
            for line in response.text.splitlines():
                filteredLine = next(iter(re.findall('[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}:[\d]{1,4}', line)), None)
                if filteredLine: proxyList.append(filteredLine)
        return proxyList 

    def __getWebProxyList(self) -> list:
        proxyList = []
        resource = DEFAULT_PROXY_WEB_RESOURCES
        response = requests.get(DEFAULT_PROXY_WEB_RESOURCES)
        if response.status_code == 200:
            proxyList = self.__filterProxyListResponse(response.text)
        return proxyList

    def __filterProxyListResponse(self, content) -> list:
        proxyList = []
        ips = re.findall('<td>([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})</td>', content, flags=re.IGNORECASE)
        ports = re.findall('<td>([\d]+)</td>', content, flags=re.IGNORECASE)
        if ( len(ips) != len(ports) ):
            raise Exception('Can\'t find full list of proxy ips.')
        for index in range(len(ips)):
            proxyList.append(ips[index]+':'+ports[index])
        return proxyList

    def __retry(self, attempts: int = 0, callback = None) -> list:
        proxyList = []
        try:
            proxyList = callback()
            attempts -= 1
            if ( not proxyList and attempts > 0 ):
                proxyList = self.__retry(attempts, callback)
        except BaseException as error:
            raise Exception("An error occurred while getting proxy list from API.")
        return proxyList