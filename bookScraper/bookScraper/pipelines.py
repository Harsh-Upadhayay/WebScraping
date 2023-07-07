# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from bookScraper.items import BookItem

class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        ratingString = adapter.get('rating').split(' ')[1].lower()

        if ratingString == 'zero':
            adapter['rating'] = 0
        elif ratingString == 'one':
            adapter['rating'] = 1
        elif ratingString == 'two':
            adapter['rating'] = 2
        elif ratingString == 'three':
            adapter['rating'] = 3
        elif ratingString == 'four':
            adapter['rating'] = 4
        elif ratingString == 'five':
            adapter['rating'] = 5

        return item


class SaveToMongoDbPipeline:

    def __init__(self):
        CONNECTION_STRING = "mongodb://127.0.0.1:27017/"
        DB_NAME = 'BlueStar'
        COLLECTION = 'books'
 
        self.dbHandle = MongoClient(CONNECTION_STRING)
        self.collHandle = self.dbHandle[DB_NAME][COLLECTION]

    def process_item(self, item, spider):
        data = dict(BookItem(item))
        self.collHandle.insert_one(data)
        return item
    
    def close_spider(self, spider):
        self.dbHandle.close()