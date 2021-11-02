import scrapy
from scrapy.selector.unified import Selector
from scrapy_selenium import SeleniumRequest

from estate.items import EstateItem
from estate.loaders.alonhadatLoader import AdditionalLoader
from estate.loaders.batdongsanLoader import BatdongsanLoader


class BatdongsanSpider(scrapy.Spider):
    name = 'batdongsan'
    allowed_domains = ['batdongsan.com.vn']
    start_urls = ['http://batdongsan.com.vn/nha-dat-ban-ha-noi']

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        estates = response.xpath(
            '//*[@class="js__product-link-for-product-id"]')
        for estate in estates[:2]:
            estate_loader = BatdongsanLoader(
                item=EstateItem(), selector=estate)
            url = response.urljoin(estate.css('*::attr(href)').extract_first())
            estate_loader.add_value('url', url)
            yield SeleniumRequest(url=url, callback=self.parse_detail, meta={'item': estate_loader.load_item()})

    def parse_detail(self, response):
        estate_loader = estate_loader = BatdongsanLoader(
            item=response.meta['item'], response=response)

        params = response.xpath('//*[@class="re__list-standard-1line--md"]')
        for param in params:
            param_name = param.xpath(
                "/span[@class='title']/text()").extract_first()

            param_content_xpath = "/span[@class='content']/text()"
            if param_name == 'Địa chỉ:':
                estate_loader.add_xpath('address',
                                        param_content_xpath).extract_first()
            elif param_name == 'Đường vào:':
                estate_loader.add_value(
                    'additional_info', self.get_addition(param))

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
