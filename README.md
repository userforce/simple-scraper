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
```python
import scraperex
```
**Scrape textual response**
Basic usage requires one paramether of type dictionary which contains ```url``` to the web resource, and ```regex``` which will extract the data from the response.
```python
config = {
    'my_scraping': {
        'method': 'GET',
        'url': 'https://www.resource.for/scraping/1',
        'params': { perPage: 5 },
        'regex': r'my_regular_expression'
    }
}

result = scraperex.find(config)
```
**Scrape json response**
If you set configuration ```json``` option **True** then ```regex``` option will be ignored and ```(requests) response.json()``` will be invoked.
```python
config = {
    'my_scraping': {
        'method': 'GET',
        'url': 'https://www.resource.for/scraping/2',
        'params': { perPage: 5 },
        'json': True
    }
}

result = scraperex.find(config)
```

***Note**: If proxy server fails, next one from the list will be used, while proxy list is not exhausted or limit is not touched. You can set limitation by sending ```attempts``` parameter. By default attempts are set to 3.*
```python
result = scraperex.find(config, attempts = 1)
```

#### Config
Config ```config``` must be of type dictionary which must contain at least one item used for scraping (as you can guess the amount of the requests will equal at least to the items amount).

***Note**: You also can build a tree of configurations and the same structure will be in your result.*

```python
config = {
    'item_A': {...},
    'item_B': {
        'item_C': {..},
        'item_D': {..},
    }
}
```

***Structured textual ( regex ) results***
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

*Note: Constructive criticism is always awaited, please share your thoughts with me: [GitHub](https://github.com/userforce/scraper).*