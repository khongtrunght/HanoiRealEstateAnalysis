import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector.unified import Selector
from estate.loaders.alonhadatLoader import AdditionalLoader, AlonhadatLoader
from estate.items import AdditionalInfo, EstateItem


class AlonhadatSpider(scrapy.Spider):
    name = 'alonhadat'
    allowed_domains = ['alonhadat.com.vn']
    start_urls = [
        'http://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi.html'] + [f"http://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi/trang--{i}.html" for i in range(
            2, 40)]

    def parse(self, response):
        estates = response.css('div.content-item')
        for estate in estates:
            estate_loader = AlonhadatLoader(item=EstateItem(), selector=estate)
            estate_loader.add_css('floors', "span.floors::text")
            url = response.urljoin(estate.css('a::attr(href)').extract_first())
            estate_loader.add_value('url', url)
            yield scrapy.Request(url, callback=self.parse_detail, meta={'item': estate_loader.load_item()})

    def parse_detail(self, response):
        estate_loader = AlonhadatLoader(
            item=response.meta['item'], response=response)
        estate_loader.add_css('address', "div.address>span.value::text")
        estate_loader.add_value(
            'price', response.css("span.price>span.value::text").extract_first())
        estate_loader.add_css('area', "span.square>span.value::text")
        estate_loader.add_xpath('bedroom', '//tr[5]/td[4]/text()')
        estate_loader.add_xpath('facade', '//tr[4]/td[2]/text()')
        estate_loader.add_xpath('direction', '//tr[1]/td[4]/text()')
        estate_loader.add_xpath('house_type', '//tr[3]/td[2]/text()')
        estate_loader.add_value('additional_info', self.get_addition(response))
        yield estate_loader.load_item()

    def get_addition(self, response):
        additional_info = AdditionalLoader(selector=Selector(response))
        additional_info.add_xpath('street_size', '//tr[2]/td[4]/text()')
        return additional_info.load_item()
