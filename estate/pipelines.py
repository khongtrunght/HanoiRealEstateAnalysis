# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from estate.items import EstateItem


class EstatePipeline:
    def process_item(self, item, spider):
        """

        :param item: input item
        :param spider: current spider
        :return: item after process
        :type item: EstateItem
        """
        estate = ItemAdapter(item)
        if estate.get('price'):
            if isinstance(estate['price'], str):
                # unit trieu/ m2
                if ('triệu /\xa0m' in estate['price']) or ('triệu/m²' in estate['price']):
                    if estate.get('area'):
                        estate['price'] = estate['area'] * \
                            price_process(estate['price']) * 10**-3
                    else:
                        raise DropItem(
                            f"Missing area when price in trieu/m2 in {item}")
                elif 'triệu' in estate['price']:
                    estate['price'] = price_process(estate['price']) * 10**-3
                elif 'tỷ' in estate['price']:
                    estate['price'] = price_process(estate['price'])
            else:  # unit ty dong
                pass
        return item


def price_process(string: str):
    return float(string.split()[0].replace(",", "."))
