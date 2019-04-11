# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Diany.items import DianyItem
import pymongo
import json
from scrapy.conf import settings

class DianyPipeline(object):
    def __init__(self):
        # self.f = open('dianying.json', 'w')
        # 初始化
        MONGO_DB = settings.get('MONGO_DB')
        MONGO_URL = settings.get('MONGO_URL')
        # MONGO_NAME = settings.get('MONGGO_NAME')
        #创建数据库链接
        client = pymongo.MongoClient(MONGO_URL)
        # 创建数据库
        my_db = client[MONGO_DB]
        # 创建表
        self.post = my_db["dianying"]

    def process_item(self, item, spider):
        # content = json.dumps(dict(item), ensure_ascii=False)
        # self.f.write(content)
        self.post.insert(dict(item))
        return item

    def close_spider(self, spider):
        # self.f.close()
        self.post.close()
