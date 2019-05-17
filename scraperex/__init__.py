from .scraper import Scraperex
from .config import DEFAULT_REQUEST_ATTEMPTS

attempts = DEFAULT_REQUEST_ATTEMPTS

def find(config: dict, attempts = attempts):
    scraper = Scraperex()
    return scraper.find(config, attempts)