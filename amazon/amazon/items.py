# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    vendor_name = scrapy.Field()
    seller_name = scrapy.Field()
    keyword = scrapy.Field()
    category = scrapy.Field()
    quantity = scrapy.Field()
    description = scrapy.Field()
    buy_box = scrapy.Field()
    is_best_link = scrapy.Field()
    is_active = scrapy.Field()
    url = scrapy.Field()
    department = scrapy.Field()
    vendor_url = scrapy.Field()
    brands = scrapy.Field()
    rating = scrapy.Field()