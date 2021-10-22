from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader


class AlonhadatLoader(ItemLoader):
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()

    address_out = Join()
