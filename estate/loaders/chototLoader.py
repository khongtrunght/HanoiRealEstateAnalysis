from scrapy.loader import ItemLoader
from estate.items import EstateItem
from itemloaders.processors import TakeFirst, MapCompose, Join, Identity

def room_process(string):
    if 'phòng' in string:
        return int(string[:-5])
    else:
        return string

def area_process(string):
    if type(string) != 'NoneType':
        return int(string[:-2])
    else:
        return string

def price_process(string):
    if 'triệu' in string:
        return int(string[:-5])*0.001
    elif 'tỷ' in string:
        return string[:-2]
    else:
        return string


class chototLoader(ItemLoader):
    default_item_class = EstateItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()

    area_in = MapCompose(area_process)
    price_in = MapCompose(price_process)
    numBed_in = MapCompose(room_process)
    numBath_in = MapCompose(room_process)

