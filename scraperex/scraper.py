import re
import requests
from fake_useragent import UserAgent
from ._config import DEFAULT_REQUEST_ATTEMPTS
from .proxy import ProxyGenerator

class Scraperex(object):

    proxies = None

    def __init__(self):
        self.proxies = ProxyGenerator()

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
        proxy=self.proxies.getNextProxy()
        headers = self.__getHeaders()
        text = ''
        failed = False
        try:
            response = requests.get(url, headers=headers, proxies=proxy)
            if response.status_code != 200:
                print('Request failed with status code [{}] for proxy [{}]'.format(response.status_code, proxy))
                failed = True
            else:
                text = self.__findInText(regex, response.text)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as error:
            print(error)
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