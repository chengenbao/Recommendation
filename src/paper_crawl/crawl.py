#!/usr/bin/env python

__author__ = "chengenbao"
__version__ = 1.0
__email__ = "genbao.chen@gmail.com"

'''
A easy python crawler for paper
'''

import urllib2
import cookielib
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
			referer = url
			headers = []
			headers.append(('Accept', 'text/html, application/xhtml+xml, */*'))
			headers.append(('Referer', referer))
			headers.append(('Accept-Language', 'en-US'))
			headers.append(('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'))
			headers.append(('Accept-Encoding', 'gzip, deflate'))
			headers.append(('Host', host))
			headers.append(('Connection', 'Keep-Alive'))

			#cookies = cookielib.CookieJar()
			#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
			opener = urllib2.build_opener()
			opener.addheaders = headers
			f = opener.open(url)
			isGzipped = f.headers.get('content-encoding', '').find('gzip') >= 0
			data = ""
			#print cookies
			while True:
				tmp = f.read(READ_BLOCK_SIZE)
				if not tmp: break
				data += tmp
			f.close()
			if isGzipped:
				data = cStringIO.StringIO(data)
				data = gzip.GzipFile(fileobj=data).read()
			article_ids = self.parse(data)
			for id in article_ids:
				url = "http://www.citeulike.org/bibtex/user/ricardcasas/article/"
				url += id
				url += "?do_username_prefix=0&key_type=0&incl_amazon=1&clean_urls=1&smart_wrap=1&q="
				print url
				f = urllib2.urlopen(url)
				page = f.read()
				print page
				file = open(id + ".txt", "w")
				file.write(page)
				file.close()
		except urllib2.URLError:
			print "open " + self._url + " error"
	def parse(self, data):
		parser = self._parser
		return parser.parse(data)


if __name__ == "__main__":
	parser = CULParser()
	crawler = PaperCrawler("http://www.citeulike.org/home/page/1", parser)
	page = crawler.crawl()
	
