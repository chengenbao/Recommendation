#! /usr/bin/env python

from CULCrawler import CULCrawler
from ThreadPool import *
from Config import config
import urllib
from Daemon import *

if __name__ == "__main__":
	#createDaemon()
	crawler = CULCrawler()
	threadNum = 5
	pool = ThreadPool(threadNum)
	crawl_page_num = int(config.get_config('crawl_pages'))
	for i in xrange(crawl_page_num):
		url = 'http://www.citeulike.org/home/page/' + str(i + 1)
		pool.queueTask(crawler.crawl, url)
	# keywords search
	f = open("keywords", "r")
	for keyword in f.readlines():
		keyword = keyword.strip()
		query = urllib.urlencode({'q' : keyword})
		url_prefix = 'http://www.citeulike.org/search/all/page/'
		for i in xrange(crawl_page_num):
			url = url_prefix + str(i + 1) + '?' + query
			#print url
			pool.queueTask(crawler.crawl, url)
	f.close()
	pool.joinAll()

