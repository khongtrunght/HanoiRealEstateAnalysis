# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass, field
from typing import Optional
@dataclass
class EstateItem(scrapy.Item):
    Area = scrapy.Field()
    Price = scrapy.Field()
    address = scrapy.Field()
    numFloor = scrapy.Field()
    numBed = scrapy.Field()
    numBath = scrapy.Field()
    direction = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
