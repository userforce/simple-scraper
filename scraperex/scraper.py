import re
import requests
from fake_useragent import UserAgent
from .config import DEFAULT_REQUEST_ATTEMPTS
from .proxy import ProxyGenerator
from .retreiver import JsonRetreiver, TextRetreiver

class Scraperex(object):

    proxyGen = None
    retreiver = None

    def __init__(self):
        self.proxyGen = ProxyGenerator()
        self.jsonRet = JsonRetreiver()
        self.textRet = TextRetreiver()

    def __getHeaders(self) -> dict:
        return { 'User-Agent': UserAgent().random }

    def __isSecuredUrl(self, url) -> bool:
        return (not not next(iter(re.findall('https', url)), False))

    def __configGet(self, item: dict, key: str, itemType, default):
        if key in item:
            return item[key] if type(item[key]) is itemType else default
        return default

    def __extract(self, regex, json, response):
        if not json:
            result = self.textRet.findInText(find = regex, text = response.text)
        else:
            result = self.jsonRet.findInJson(json = response.json())
        return result

    def __request(self, regex, url: str, method: str, json: bool = False, params: dict = {}, attempts: int = 1):
        result = {}
        failed = False
        attempts -= 1
        proxy = self.proxyGen.getNextProxy(self.__isSecuredUrl(url))
        headers = self.__getHeaders()
        try:
            response = requests.request(url = url, method = method, data = params, headers = headers, proxies = proxy)
            if response.status_code != 200:
                failed = True
            else:
                result = self.__extract(regex = regex, json = json, response = response)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as error:
            print(error)
            failed = True
        if failed and attempts > 0:
            self.__request(regex = regex, url = url, method = method, json = json, params = params, attempts = attempts)
        return result

    def __checkConfigValidity(self, items, key) -> bool:
        isValid = False
        hasRequired = type(items) is dict and all(item in items for item in ['url'])
        if hasRequired:
            if type(items['url']) is not str:
                raise Exception('The [{}.url] must be of type str.'.format(key))
            isValid = True
        return isValid

    def find(self, config: dict, attempts: int):
        result = {}
        for key, item in config.items():
            hasNestedConfig = not self.__checkConfigValidity(item, key)
            if hasNestedConfig:
                result[key] = self.find(item)
            else:
                regex = self.__configGet(item, 'regex', dict, {})
                url = self.__configGet(item, 'url', str, '')
                method = self.__configGet(item, 'method', str, 'get')
                json = self.__configGet(item, 'json', bool, False)
                params = self.__configGet(item, 'params', dict, {})
                result[key] = self.__request(regex = regex, url = url, method = method, json = json, params = params, attempts = attempts)
        return result
