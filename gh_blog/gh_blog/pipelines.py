# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv, json, pymongo
from scrapy.exceptions import DropItem


class MongoPipeline(object):
    collection_name = 'blogs'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DATABASE',
                                                 'gh_blog'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # if title doesn't exist in collection, add to collection
        if self.db[self.collection_name].find_one({"link": item["link"]}) is \
                None:
            self.db[self.collection_name].insert_one(dict(item))
            return item
        else:
            print('Duplicate title found: "{}"'.format(item["title"]))


class DuplicatesPipeline(object):

    def __init__(self):
        self.links_seen = self.get_current_blog_links(f_type='csv')

    def process_item(self, item, spider):
        if item['link'] in self.links_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.links_seen.add(item['link'])
            return item

    @staticmethod
    def get_current_blog_links(f_type='json'):
        if f_type is 'csv':
            with open('blogs.csv', newline='', encoding='utf-8-sig') as f:
                return {row['link'] for row in csv.DictReader(f)}
        else:
            with open('blogs.json') as f:
                return {item['link'] for item in json.load(f)}

