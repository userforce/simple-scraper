![Scraperex](https://i.ibb.co/NKNQj9m/scraper.png "Scraperex")

Web scraper using dynamic proxy and user agent.

#### Description

Scraperex is simple and easy to use web scraper for retreiving data from request and **avoiding HTTP 503 error** (usually emerges when server is watching for bots/crawlers/requests while regular scraping). 

Pakage is generating random user-agent headers using [fake-useragent](https://pypi.org/project/fake-useragent/), and a list of proxy servers that is used while maiking requests.


#### Installation
```python
pip install scraperex
```

#### Dependencies
* [requests](https://pypi.org/project/requests/)
* [fake-useragent](https://pypi.org/project/fake-useragent/)

#### Usage
Basic usage requires definition a dictionary with one item that contains ```url``` to the web resource, and ```regex``` which will extract the data from the response.
```python
from scraperex import Scraper

config = {
    'my_scraping': {
        'url': 'https://www.resource.for/scraping/1',
        'regex': r'my_regular_expression'
    }
}

scraper = Scraper()
result = scraper.get(config)
```

#### Config
Config ```config``` must be of type dictionary which contains items used for scraping (as you can guess the amount of the requests will equal at least to the items amount).

*Note: In case when current proxy fails next proxy server from the list will be used which will make one another request.*

```python
config = {
    'item_A': {...},
    'item_B': {...}
}
```
Each ```config``` item must contain two predefined properties ```url``` and ```regex```.

```python
    'item_A': {
        'url': 'https://www.resource.for/scraping/1',
        'regex': r'my_regular_expression'
    }
```
You can rescrape response content as many times as you wish by passing to ```regex``` property dictionary instead of string (also it is useful if you want to structure your results, scraping will result in the same structure you defined).

```python
    'item_B': {
        'url': 'https://www.resource.for/scraping/2',
        'regex': {
            'structure_item': {
               'child_structure_item_1': r'my_regular_expression'
            }
            'structure_item_1':  r'my_regular_expression_1'
        }
    }
```

*Note: Constructive criticism is always acceptable, please share your thoughts with me: [GitHub](https://github.com/userforce/scraper).*