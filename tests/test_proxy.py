import unittest
import re
from scraperex.proxy import ProxyGenerator

class TestProxy(unittest.TestCase):

	proxyGen = None

	def setUp(self):
		self.proxyGen = ProxyGenerator()
	
	def test_proxyList(self):
		proxyList = self.proxyGen.getNextProxy()
		self.assertTrue('http' in proxyList)
		self.assertTrue(self.isIp(proxyList['http']))

	def test_apiProxyList(self):
		securedProxyList = self.proxyGen.getNextProxy(secured = True)
		self.assertTrue('https' in securedProxyList)
		self.assertTrue(self.isIp(securedProxyList['https']))

	def isIp(self, string: str) -> bool:
		return bool(re.search(r'[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}:[\d]{1,4}', string))
