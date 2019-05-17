import re

class Retreiver(object):
    pass

# TODO: Retrieve by dot notation
class JsonRetreiver(Retreiver):

    def findInJson(self, json):
        return json

class TextRetreiver(Retreiver):

    def findInText(self, find: dict, text) -> dict:
        if (type(find) is dict):
            result = self.__findAll(find, text)
        else:
            result = self.__findOne(find, text)
        return result

    def __findOne(self, regex, text) -> list:
        results = []
        items = re.findall(regex, text, flags=re.IGNORECASE)
        for item in items:
            results.append(re.sub('\\s+', ' ', item).strip())
        return results

    def __findAll(self, regex, text) -> dict:
        result = {}
        for key, value in regex.items():
            if (type(value) is dict):
                result[key] = self.__findAll(value, text)
            else:
                result[key] = self.__findOne(value, text)
        return result