#! /usr/bin/env python

from CULCrawler import CULCrawler
from ThreadPool import *
from Config import config

if __name__ == "__main__":
    crawler = CULCrawler()
    threadNum = 5
    pool = ThreadPool(threadNum)
    crawl_page_num = int(config.get_config('crawl_pages'))
    for i in xrange(crawl_page_num):
        url = 'http://www.citeulike.org/home/page/' + str(i + 1)
        print url
        pool.queueTask(crawler.crawl, url)
    pool.joinAll()

