#! /usr/bin/env python

from Parser import Parser
import re

class CULParser(Parser):
    def parse(self, page):
        tmp = re.findall(r'article_id:\d+', page)
        article_ids = []
        for s in tmp:
            id = s.split(':')[1]
            article_ids.append(id)
        pattern = r'data-link=.*/article/'
        result = {}
        for id in article_ids:
            p = pattern + id
            m = re.search(p, page)
            if m:
                s = m.group(0).split('=')[1]
                s = s[1:]
                result[id] = s

        return result

