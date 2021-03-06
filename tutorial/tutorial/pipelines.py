# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from datetime import datetime
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy.exceptions import DropItem
from twisted.internet.threads import deferToThread

class StripPipeline(object):
    def process_item(self, item, spider):
        for key in item.keys():
            # if type(item[key]==unicode):
            if type(item[key])==unicode:
                item[key] = item[key].strip()
        return item

class HouseDealPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'house':
            item["crawled_time"] = str(datetime.utcnow())
            item["_id"] = item["house_no"]
            # item["spider"] = spider.name
            pass
        return item



class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item



class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__

        # self.db[collection_name].insert(dict(item))
        self.db[collection_name].update({'_id':item["_id"]}, dict(item), True)
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if spider.name == 'house':
            if item['house_no'] in self.ids_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.ids_seen.add(item['house_no'])
                return item

from scrapy_redis import connection

default_serialize = ScrapyJSONEncoder().encode

class ChengJiaoUrlPipeline(object):

    def __init__(self, server,
                 key='%(spider)s:items',
                 serialize_func=default_serialize):
        self.server = server
        self.key = key
        self.serialize = serialize_func

    @classmethod
    def from_settings(cls, settings):
        params = {
            'server': connection.from_settings(settings),
        }
        return cls(**params)
    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        key = "chengjiao_urls"
        # store new url to chengjiao_urls
        data = self.serialize("dasdasdasd")
        self.server.rpush(key, data)
        return item
