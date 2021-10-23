from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from scrapy.loader import ItemLoader
from ..items import EstateItem, AdditionalInfo


def take_first_string(string):
    if isinstance(string, str):
        return string.split()[0]
    else:
        return string


def float_process(string):
    return float(string.replace(",", "."))


def int_process(string):
    return int(string)


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


class AlonhadatLoader(ItemLoader):
    default_item_class = EstateItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()

    facade_in = MapCompose(facade_process, float_process)

    direction_in = MapCompose(direction_process)

    price_in = MapCompose(take_first_string, float_process)

    floors_in = MapCompose(take_first_string, int_process)

    area_in = MapCompose(take_first_string, float_process)

    additional_info_in = Identity()

    address_out = Join()


def street_process(string):
    return string[:-1]


class AdditionalLoader(ItemLoader):
    default_item_class = AdditionalInfo

    street_size_in = MapCompose(street_process, float_process)
