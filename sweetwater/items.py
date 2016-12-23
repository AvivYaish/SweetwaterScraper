# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SweetwaterItem(scrapy.Item):
    item_id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    product_url = scrapy.Field()
    description = scrapy.Field()
    reviews = scrapy.Field()
