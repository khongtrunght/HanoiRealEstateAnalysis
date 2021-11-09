import scrapy
from scrapy.selector.unified import Selector
from scrapy_selenium import SeleniumRequest

from estate.items import EstateItem
from estate.loaders.alonhadatLoader import AdditionalLoader
from estate.loaders.batdongsanLoader import BatdongsanLoader


class BatdongsanSpider(scrapy.Spider):
    name = 'batdongsan'
    allowed_domains = ['batdongsan.com.vn']
    start_urls = [
        f'https://batdongsan.com.vn/nha-dat-ban-ha-noi/p{x}' for x in range(1, 5)]

    custom_settings = {
        "ITEM_PIPELINES": {
            'estate.pipelines.EstatePipeline': 300
        },
        "SELENIUM_DRIVER_NAME": 'chrome',
        "SELENIUM_DRIVER_EXECUTABLE_PATH": '../driver/chromedriver.exe',
        "SELENIUM_DRIVER_ARGUMENTS": [],  # ['--headless']

        "DOWNLOADER_MIDDLEWARES": {
            'scrapy_selenium.SeleniumMiddleware': 800
        },
    }

    name_dict = {

        'Địa chỉ': 'address',
        'Mặt tiền': 'facade',
        'Hướng nhà': 'direction',

        'Số toilet': 'bathroom',
        'Số tầng': 'floors',
        'Loại tin đăng': 'house_type',

        'Đường vào': 'street_size',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        estates = response.xpath(
            '//*[@class="js__product-link-for-product-id"]')
        for estate in estates[:3]:
            estate_loader = BatdongsanLoader(
                item=EstateItem(), selector=estate)
            url = response.urljoin(estate.css('*::attr(href)').extract_first())
            estate_loader.add_value('url', url)
            yield SeleniumRequest(url=url, callback=self.parse_detail, meta={'item': estate_loader.load_item()})

    def parse_detail(self, response):
        estate_loader = estate_loader = BatdongsanLoader(
            item=response.meta['item'], response=response)
        table_xpath = '//*[@class="re__list-standard-1line--md"]'
        param_content_xpath = lambda \
            x: f"/span[@class='title'  and contains(text(),'{x}')]/following-sibling::span[@class='value']/text()"

        for t in self.name_dict.keys():
            estate_loader.add_xpath(
                self.name_dict[t], table_xpath + param_content_xpath(t))

        def get_xpath(string):
            return f"//div[@class='re__pr-short-info-item js__pr-short-info-item']/span[@class='title' and contains(text(),'{string}')]/following-sibling::span[@class='value']/text()"

        estate_loader.add_xpath(
            'price', get_xpath("Mức giá"))
        estate_loader.add_xpath(
            'area', get_xpath("Diện tích"))
        estate_loader.add_xpath(
            'bedroom', get_xpath("Phòng ngủ"))

        yield estate_loader.load_item()

    def get_addition(self, response):
        additional_info = AdditionalLoader(selector=Selector(response))
        additional_info.add_xpath(
            'street_size', "/span[@class='content']/text()")
        return additional_info.load_item()
