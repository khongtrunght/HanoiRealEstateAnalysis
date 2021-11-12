# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass, field
from typing import Optional

class EstateItem(scrapy.Item):
    area = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    numFloor = scrapy.Field()
    numBed = scrapy.Field()
    numBath = scrapy.Field()
    direction = scrapy.Field()
    type = scrapy.Field()
    type_detail = scrapy.Field()
    property_road = scrapy.Field()
    property_back = scrapy.Field()
    furniture = scrapy.Field()
    url = scrapy.Field()
