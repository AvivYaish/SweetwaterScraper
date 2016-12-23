# -*- coding: utf-8 -*-
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SweetwaterPipeline(object):
    items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        """
        Write results to a formatted JSON file.
        This isn't really necessary, as outputting to a not-pretty-formatted JSON file is built in into scrapy.
        """
        with open('./items.json', 'w') as items_file:
            json.dump(self.items, items_file, indent=4, sort_keys=True, separators=(',', ': '))
