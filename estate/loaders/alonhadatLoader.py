from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from scrapy.loader import ItemLoader
from ..items import EstateItem, AdditionalInfo


def take_first_string(string):
    """
    Get the first word in string

    :param string: input string
    :return: first word in string
    """
    if isinstance(string, str):
        return string.split()[0]
    else:
        return string


def check_none(string):
    """
    Check if the input string is None in some diffirent format

    :param string: input string
    :return: return string if not None else None
    """
    if string in (',m', '_', "---", ''):
        return None
    else:
        return string


def float_process(string):
    """
    Convert input string to float if possible

    :param string: input string of type abc.xyz
    :return: float number
    :except: return original string
    """
    try:
        return float(string.replace(",", "."))
    except ValueError:
        return string


def int_process(string):
    """
        Convert input string to integer if possible

        :param string: input string of type abc.xyz
        :return: integer number
        :except: return original string
        """
    try:
        return int(string)
    except ValueError:
        return string


def direction_process(string):
    """
    Preprocess for direction attribute

    :param string: input string
    :return: well-formated string
    """
    if string == '_':
        return None
    else:
        return string


def facade_process(string):
    """
        Preprocess for facade attribute

        :param string: input string
        :return: well-formated string
    """
    if string == "---":
        return None
    else:
        return string[:-1]


def bedroom_process(string):
    """
        Preprocess for bedroom attribute

        :param string: input string
        :return: well-formated string
    """
    if string == "---":
        return None
    else:
        return string


def street_process(string):
    """
        Preprocess for street attribute

        :param string: input string
        :return: well-formated string
    """
    if string == '---':
        return None
    else:
        return float_process(string[:-1])


class AlonhadatLoader(ItemLoader):
    """Define the default process for Alonhadat

    """
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
