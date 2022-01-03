import scrapy
from estate.items import EstateItem
from datetime import datetime
import re
from scrapy_selenium import SeleniumRequest





def room_process(string):
    if string is not None:
        if 'phòng' in string:
            if 'hơn' in string:
                return string
            else:
                return int(string[:-5].replace(',','.'))
        else:
            return string
    else:
        return string

def area_process(string):

    if string is not None:
        return float(string[:-3].replace(',','.'))
    else:
        return string

def price_process(string):
    if string is not None:
        if 'triệu' in string:
            return round(float(string[:-6].replace(',','.'))*0.001,5)
        elif 'tỷ' in string:
            return float(string[:-3].replace(',','.'))
    else:
        return string

def price_m2_process(string):
    if string is not None:
        if "triệu/m²" in string:
            return round(float(string[:-8].replace(',','.'))*0.001,5)

        else:
            return string

    else:
        return string

class test(scrapy.Spider):

    custom_settings = {
        "ITEM_PIPELINES": {
            'estate.pipelines.EstatePipeline': 300
        },
        "SELENIUM_DRIVER_NAME": 'chrome',
        "SELENIUM_DRIVER_EXECUTABLE_PATH": 'C:/Users/pn021/Desktop/HanoiRealEstateAnalysis/chromedriver.exe',
        "SELENIUM_DRIVER_ARGUMENTS": [],  # ['--headless']

        "DOWNLOADER_MIDDLEWARES": {
            'scrapy_selenium.SeleniumMiddleware': 800
        },
    }


    name = "chotot"
    start_urls = [f'https://nha.chotot.com/ha-noi/mua-ban-nha-dat?page={i}' for i in range(1, 870)]
    # start_urls = [f'https://nha.chotot.com/ha-noi/mua-ban-can-ho-chung-cu?page={i}' for i in range(1, 311)]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)
    def parse(self, response):
        estates = response.xpath("//li[contains(@class, 'AdItem_wrapperAdItem__1hEwM  AdItem_big__2Sqod')]//a/@href")
        for href in estates:
            print(href)
            print(href.extract())
            url = "https://nha.chotot.com/" + (href.extract()).split('/')[-1]

            yield SeleniumRequest(url=url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = EstateItem()
        area = response.xpath("//span[@itemprop = 'size']/text()").extract_first()
        item['area'] = area_process(area)
        price = response.xpath("//span[contains(@itemprop, 'price')]/text()").extract_first()
        item['price'] = price_process(price)

        # priceperarea = response.xpath("//span[contains(@itemprop, 'price_m2')]/text()").extract_first()
        # item['price_m2'] = price_m2_process(priceperarea)

        item['address'] = response.xpath("//span[@class = 'fz13']/text()").extract_first()

        numFloor = response.xpath("//span[@itemprop = 'floors']/text()").extract_first()
        if numFloor is not None:
            item['numFloor'] = int(numFloor)
        else:
            item['numFloor'] = None

        numBed = response.xpath("//span[@itemprop = 'rooms']/text()").extract_first()
        item['numBed'] = room_process(numBed)
        numBath = response.xpath("//span[@itemprop = 'toilets']/text()").extract_first()
        item['numBath'] = room_process(numBath)
        item['direction'] = response.xpath("//span[@itemprop = 'direction']/text()").extract_first()
        # item['type'] = "Căn hộ/Chung cư"
        item['type'] = "Nhà ở"
        item['type_detail'] = response.xpath("//span[@itemprop = 'house_type']/text()").extract_first()
        # item['type_detail'] = response.xpath("//span[@itemprop = 'apartment_type']/text()").extract_first()
        # item['property_road'] = response.xpath("//span[@itemprop = 'property_road_condition']/text()").extract_first()
        # item['property_back'] = response.xpath("//span[@itemprop = 'property_back_condition']/text()").extract_first()
        # item['floornumber'] = response.xpath("//span[@itemprop = 'floornumber']/text()").extract_first()
        item['furniture'] = response.xpath("//span[@itemprop = 'furnishing_sell']/text()").extract_first()
        item['url'] = response.xpath("//link[@rel = 'canonical']//@href").extract_first()
        yield item

