from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from scrapy.loader import ItemLoader

from .alonhadatLoader import AlonhadatLoader, take_first_string, int_process
from ..items import EstateItem, AdditionalInfo


class BatdongsanLoader(AlonhadatLoader):
    """ Loader for batdongsan.com.vn website
        Inherit from AlonhadatLoader"""
    # default_item_class = EstateItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()

    # use take_first_string and then convert to int
    bedroom_in = MapCompose(take_first_string, int_process)
    
    # use take_first_string and then convert to int 
    bathroom_in = MapCompose(take_first_string, int_process)
