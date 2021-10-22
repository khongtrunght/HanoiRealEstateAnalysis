import scrapy
from scrapy.loader import ItemLoader
from estate.loaders.alonhadatLoader import AlonhadatLoader
from estate.items import EstateItem


class AlonhadatSpider(scrapy.Spider):
    name = 'alonhadat'
    allowed_domains = ['alonhadat.com.vn']
    start_urls = [
        'http://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi.html'] + [f"http://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi/trang--{i}.html" for i in range(
            2, 3)]

    def parse(self, response):
        estates = response.css('div.content-item')
        for estate in estates:
            estate_loader = AlonhadatLoader(item=EstateItem(), selector=estate)
            estate_loader.add_css('floors', "span.floors::text")
            url = response.urljoin(estate.css('a::attr(href)').extract_first())
            yield scrapy.Request(url, callback=self.parse_detail, meta={'item': estate_loader.load_item()})

    def parse_detail(self, response):
        estate_loader = AlonhadatLoader(
            item=response.meta['item'], response=response)
        estate_loader.add_css('address', "div.address>span.value::text")
        estate_loader.add_css('price', "span.price>span.value::text")
        estate_loader.add_css('area', "span.square>span.value::text")
        yield estate_loader.load_item()
