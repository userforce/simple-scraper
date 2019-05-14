from .scraper import Scraperex

def get(config: dict):
	instance = Scraperex()
	return instance.get(config)