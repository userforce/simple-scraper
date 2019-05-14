import re
import requests
import collections
import pkgutil
from fake_useragent import UserAgent

class Scraper():

    __DEFAULT_PROXY_RESOURCES = [
        'https://free-proxy-list.net/',
        'https://www.us-proxy.org/'
    ]

    __requestAttempts = 5
    __proxyList = []
    __proxyIterator = None

    def __getDefaultProxyList(self, attempts: int = 0) -> list:
        list = []
        resource = self.__DEFAULT_PROXY_RESOURCES[0]
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

    def __getProxyList(self) -> list:
        if ( not self.__proxyList ):
            self.setProxyList(self.__getDefaultProxyList(self.__requestAttempts))
        return self.__proxyList

    def __getHeaders(self) -> dict:
        return { 'User-Agent': UserAgent().random }


    def __findInText(self, regex, text) -> dict:
        if ( type(regex) is dict ):
            result = self.__findAll(regex, text)
        else:
            result = self.__findOne(regex, text)
        return result

    def __findOne(self, regex, text) -> list:
        print(text)
        print(regex)
        result = re.findall(regex, text, flags=re.IGNORECASE)
        return result

    def __findAll(self, regex, text) -> dict:
        result = {}
        for key, value in regex.items():
            if ( type(value) is dict):
                result[key] = self.__findAll(value, text)
            else:
                result[key] = self.__findOne(value, text)
        return result

    def __getNextProxy(self) -> dict:
        if ( not self.__proxyIterator or not isinstance(self.__proxyIterator, collections.Iterable) ):
            self.__proxyIterator = iter(self.__getProxyList())
        proxy = next(self.__proxyIterator)
        return {
            "http": proxy,
            "https": proxy
        }

    def setProxyList(self, proxyList: list):
        self.__proxyList = proxyList

    def __checkConfigValidity(self, items, key) -> bool:
        isValid = False
        hasRequired = type(items) is dict and all(item in ['regex', 'url'] for item in items)
        if hasRequired:
            if not type(items['regex']) in [str, dict]:
                raise Exception('The [{}.regex] must be of type str or dict.'.format(key))
            if type(items['url']) is not str:
                raise Exception('The [{}.url] must be of type str.'.format(key))
            isValid = True
        return isValid

    def __request(self, regex, url: str):
        proxy=self.__getNextProxy()
        headers = self.__getHeaders()
        text = ''
        failed = False
        try:
            response = requests.get(url, headers=headers, proxies=proxy)
            if response.status_code != 200:
                failed = True
            else:
                text = self.__findInText(regex, request.text)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            failed = True
        if failed:
            print('Request failed using [{}] proxy server.'.format(proxy))
            text = self.__request(regex, url)
        return text

    def get(self, config: dict):
        result = {}
        for key, item in config.items():
            hasNoNestedConfig = self.__checkConfigValidity(item, key) 
            if hasNoNestedConfig:
                url = item['url']
                regex = item['regex']
                result[key] = self.__request(item['regex'], item['url'])
            else:
                result[key] = self.get(item)
        return result