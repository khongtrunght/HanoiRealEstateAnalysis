# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join


class EstateItem(scrapy.Item):
    address = scrapy.Field()
    facade = scrapy.Field()
    direction = scrapy.Field()
    age = scrapy.Field()
    area = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    floors = scrapy.Field()
    house_type = scrapy.Field()
    price = scrapy.Field()
