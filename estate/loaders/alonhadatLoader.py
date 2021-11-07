from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from scrapy.loader import ItemLoader
from ..items import EstateItem, AdditionalInfo


def take_first_string(string):
    if isinstance(string, str):
        return string.split()[0]
    else:
        return string


def check_none(string):
    if string in (',m', '_', "---", ''):
        return None
    else:
        return string


def float_process(string):
    try:
        return float(string.replace(",", "."))
    except ValueError:
        return string


def int_process(string):
    try:
        return int(string)
    except ValueError:
        return string


def direction_process(string):
    if string == '_':
        return None
    else:
        return string


def facade_process(string):
    if string == "---":
        return None
    else:
        return string[:-1]


def bedroom_process(string):
    if string == "---":
        return None
    else:
        return string

def street_process(string):
    if string == '---':
        return None
    else:
        return float_process(string[:-1])



class AlonhadatLoader(ItemLoader):
    default_item_class = EstateItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()

    facade_in = MapCompose(check_none, facade_process, float_process)

    direction_in = MapCompose(check_none, direction_process)

    price_in = Identity()  # MapCompose(price_process)
    price_out = TakeFirst()

    floors_in = MapCompose(take_first_string, int_process)

    area_in = MapCompose(take_first_string, float_process)

    bedroom_in = MapCompose(check_none, bedroom_process, int_process)

    additional_info_in = Identity()

    address_out = Join()

    street_size_in = MapCompose(street_process)




class AdditionalLoader(ItemLoader):
    default_item_class = AdditionalInfo

    street_size_in = MapCompose(street_process)
