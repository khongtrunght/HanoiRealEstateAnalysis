# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AdditionalInfo():
    street_size: Optional[float] = field(default=None)


@dataclass
class EstateItem():
    """field for EstateItem
    """
    url: Optional[str] = field(default=None)
    address: Optional[str] = field(default=None)
    facade: Optional[float] = field(default=None)
    direction: Optional[str] = field(default=None)
    age: Optional[int] = field(default=None)
    area: Optional[float] = field(default=None)
    bedroom: Optional[int] = field(default=None)
    bathroom: Optional[int] = field(default=None)
    floors: Optional[int] = field(default=None)
    house_type: Optional[str] = field(default=None)
    price: Optional[float] = field(default=None)
    # additional_info: Optional[AdditionalInfo] = field(default=None)
    street_size: Optional[float] = field(default=None)
    # additional_info = scrapy.Field(serializer=AdditionalInfo)
