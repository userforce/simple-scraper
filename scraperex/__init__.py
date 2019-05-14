from .scraper import Scraperex

def get(config: dict):
	scraper = Scraperex()
	return scraper.get(config)