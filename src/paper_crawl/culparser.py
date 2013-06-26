#! /usr/bin/env python

from parser import Parser
import re

class CULParser(Parser):
	def parse(self, page):
		tmp = re.findall(r'article_id:\d+', page)
		article_ids = []
		for s in tmp:
			id = s.split(':')[1]
			article_ids.append(id)
		print  repr(article_ids)
		return article_ids

