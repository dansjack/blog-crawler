# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv, json, pymongo
from scrapy.exceptions import DropItem


class MongoPipeline(object):
    coll_name = 'blogs'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.count = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DATABASE',
                                                 'gh_blog'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        print('Added {} posts to collection'.format(self.count))
        self.client.close()

    def process_item(self, item, spider):
        # if title doesn't exist in collection, add to collection
        if self.db[self.coll_name].find_one({"url": item["url"]}) is None:
            self.count += 1
            self.db[self.coll_name].insert_one(dict(item))
            return item
        else:
            print('Duplicate title found: "{}"'.format(item["title"]))


class DuplicatePipeExample(object):
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['url'])
            return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.links_seen = self.get_current_blog_links(f_type='csv')

    def process_item(self, item, spider):
        if item['url'] in self.links_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.links_seen.add(item['url'])
            return item

    @staticmethod
    def get_current_blog_links(f_type='json'):
        if f_type is 'csv':
            with open('b.csv', newline='', encoding='utf-8-sig') as f:
                return {row['url'] for row in csv.DictReader(f)}
        else:
            with open('b.json') as f:
                return {item['url'] for item in json.load(f)}

