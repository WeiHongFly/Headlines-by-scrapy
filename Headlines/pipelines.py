# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo
import logging
from scrapy.exceptions import DropItem
from scrapy import log
from items import HeadlinesItem


class HeadlinesSpider(object):

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['urlMd5'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['urlMd5'])
            return item
        NewsInfo = dict(item)
        logging.info('insert title:' + item['title'])
        self.post.insert(NewsInfo)
        return item
