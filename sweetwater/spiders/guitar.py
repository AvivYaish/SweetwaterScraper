# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from sweetwater.items import SweetwaterItem


class GuitarSpider(scrapy.Spider):
    name = "guitar"
    base_url = 'sweetwater.com'
    allowed_domains = [base_url]
    schemed_base_url = 'http://' + base_url
    start_urls = [schemed_base_url + '/c590--Solidbody_Guitars/']
    item_limit = 50             # the limit for number of items to crawl
    crawled_items_count = 0     # counter for the items crawled so far

    def parse(self, response):
        """
        Parses an item list page.
        """
        if response is None:
            return None

        if self.crawled_items_count > self.item_limit:
            return

        soup = BeautifulSoup(response.body, 'html.parser')

        # first, yield a request for the next item list page (for better parallalization)
        next_page_link = soup.find('a', {'class' : 'next'})
        if next_page_link:
            next_page_url = self.schemed_base_url + next_page_link.get('href')
            yield scrapy.Request(url=next_page_url, callback=self.parse)

        # yield requests for the item pages
        for product_html in soup.find_all('div', {'class' : 'product-card'}):
            if self.crawled_items_count > self.item_limit:
                return

            if (product_html is None) or (product_html.a is None):
                continue

            self.crawled_items_count += 1
            item_link = self.schemed_base_url + product_html.a.get('href')
            yield scrapy.Request(item_link, callback=self.parse_item)

    def parse_item(self, response):
        """
        Parses a single item.
        """
        soup = BeautifulSoup(response.body, 'html.parser')

        item = SweetwaterItem()
        item['product_url'] = response.url
        item['item_id'] = soup.find('span', {'itemprop' : 'productID'}).text
        item['name'] = ' '.join(soup.find('h1', {'class' : 'product__name'}).text.split())
        item['price'] = soup.find('price').text
        item['description'] = ' '.join(soup.find('div', {'class' : 'product__desc'}).text.split())
        item['reviews'] = []

        # if there is a link to a reviews page, follow it and add the reviews to the item
        reviews_link =  soup.find('a', {'class' : 'product-meta__rating'})
        if reviews_link:
            reviews_url = self.schemed_base_url + reviews_link.get('href')
            request = scrapy.Request(reviews_url, callback=self.parse_reviews)
            request.meta['item'] = item
            return request
        else:
            return item

    @staticmethod
    def parse_reviews(response):
        """
        Parses the reviews of an item.
        """
        item = response.meta['item']

        soup = BeautifulSoup(response.body, 'html.parser')
        for review in soup.find_all('p', {'itemprop' : 'description'}):
            if review is None:
                continue
            item['reviews'].append(review.text)

        return item
