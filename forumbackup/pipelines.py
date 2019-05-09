'''Custom data processing before save'''
# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class DuplicateUsersPipeline():
    '''Skip duplicate users'''
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        '''Check if user_id already exists'''
        if not item['user_id']:
            raise DropItem("user_id not found: %s" % item)
        if item['user_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['user_id'])
            return item
