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
                file = open(id + ".bib", "w")
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

