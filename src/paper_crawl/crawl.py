#!/usr/bin/env python

__author__ = "chengenbao"
__version__ = 1.0
__email__ = "genbao.chen@gmail.com"

'''
A easy python crawler for paper
'''

import urllib2
import cStringIO
import gzip
from urlparse import urlparse

from culparser import CULParser

READ_BLOCK_SIZE = 1024*8

class PaperCrawler:
	def __init__(self, url, parser):
		self._url = url
		self._parser = parser
	def crawl(self, url = None):
		try:
			if not url:
				url = self._url
			p = urlparse(url)
			host = p.netloc.split(':')[0]
			referer = p.scheme + '://' + host
			headers = []
			headers.append(('Accept', 'text/html, application/xhtml+xml, */*'))
			headers.append(('Referer', referer))
			headers.append(('Accept-Language', 'en-US'))
			headers.append(('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'))
			headers.append(('Accept-Encoding', 'gzip, deflate'))
			headers.append(('Host', host))
			headers.append(('Connection', 'Keep-Alive'))
			opener = urllib2.build_opener()
			opener.addheaders = headers
			f = opener.open(url)
			print repr(f.info().items())
			isGzipped = f.headers.get('content-encoding', '').find('gzip') >= 0
			data = ""
			while True:
				tmp = f.read(READ_BLOCK_SIZE)
				if not tmp: break
				data += tmp
			f.close()
			print isGzipped
			if isGzipped:
				data = cStringIO.StringIO(data)
				data = gzip.GzipFile(fileobj=data).read()
			return data 
		except urllib2.URLError:
			print "open " + self._url + " error"
	def parse(self, data):
		parser = self._parser
		return parser.parse(data)


if __name__ == "__main__":
	parser = CULParser()
	crawler = PaperCrawler("http://www.citeulike.org/home", parser)
	page = crawler.crawl()
	article_ids = crawler.parse(page)
	for id in article_ids:
		url = "http://www.citeulike.org/bibtex/user/ricardcasas/article/"
		url += id
		url += "?do_username_prefix=0&key_type=0&incl_amazon=1&clean_urls=1&smart_wrap=1&q="
		print url
		page = crawler.crawl(url)
		print page
		file = open(id + ".txt", "w")
		file.write(page)
		file.close()
