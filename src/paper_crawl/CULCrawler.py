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
import requests

from CULParser import CULParser
from Config import *
from Util import *

READ_BLOCK_SIZE = 1024*8

class CULCrawler:
	def __init__(self, url = None):
		self._url = url
		self._parser = CULParser()
	def crawl(self, url = None):
		try:
			if not url:
				url = self._url
			if not url:
				return
			p = urlparse(url)
			host = p.netloc.split(':')[0]
			referer = url
			headers = {}
			headers['Accept'] = 'text/html, application/xhtml+xml, */*'
			headers['Referer'] = referer
			headers['Accept-Language'] = 'en-US'
			headers['User-Agent'] = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'
			headers['Accept-Encoding'] = 'gzip, deflate'
			headers['Host'] = host
			headers['Connection'] = 'Keep-Alive'
			r = requests.get(url, headers = headers)
			data = r.content
			articles = self.parse(data)
			for id, path in articles.items():
				# random sleep
				random_sleep()
				url = "http://www.citeulike.org/bibtex"
				url += path
				payload = {}
				payload['do_username_prefix'] = 0
				payload['key_type'] = 0
				payload['incl_amazon'] = 1
				payload['clean_urls'] = 1
				payload['smart_wrap'] = 1
				payload['q'] = ''
				cookies = {}
				cookies['accept_cookie_terms'] = 'no'
				r = requests.get(url, params = payload, headers = headers, cookies = cookies)
				page = r.content
				filename = config.get_config('data_dir')
				filename += "/" + id + ".bib"
				if len(page) == 0:
					filename += "-"
				file = open(filename, "w")
				file.write(page)
				if len(page) == 0:
					file.write(url)
				file.close()
		except urllib2.URLError:
			print "open " + self._url + " error"
	def parse(self, data):
		parser = self._parser
		return parser.parse(data)


if __name__ == "__main__":
	crawler = CULCrawler("http://www.citeulike.org/home/page/1")
	page = crawler.crawl()

