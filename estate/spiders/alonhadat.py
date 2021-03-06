import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector.unified import Selector
from estate.loaders.alonhadatLoader import AdditionalLoader, AlonhadatLoader
from estate.items import AdditionalInfo, EstateItem


class AlonhadatSpider(scrapy.Spider):
    """ Spider to scrape alonhadat.com.vn website"""
    name = 'alonhadat'
    allowed_domains = ['alonhadat.com.vn']
    start_urls = [
        'http://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi.html'] + [f"http://alonhadat.com.vn/nha-dat/can-ban/nha-dat/1/ha-noi/trang--{i}.html" for i in range(
            2, 12452)]

    custom_settings = {
        "ITEM_PIPELINES": {
            'estate.pipelines.EstatePipeline': 30
        },
    }


    def parse(self, response):
        """
        Parse the response ( Get all estate in page)
        :param response: the response when follow link in start_urls
        """
        estates = response.css('div.content-item')
        for estate in estates:
            estate_loader = AlonhadatLoader(item=EstateItem(), selector=estate)
            estate_loader.add_css('floors', "span.floors::text")
            url = response.urljoin(estate.css('a::attr(href)').extract_first())
            estate_loader.add_value('url', url)
            yield scrapy.Request(url, callback=self.parse_detail, meta={'item': estate_loader.load_item()})

    def parse_detail(self, response):
        """
        Parse for each sub content in website ( here is an estate )
        :param response: content contains information of estate
        :return: return an item of EstateItem type
        """
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
        estate_loader.add_xpath('street_size', '//tr[2]/td[4]/text()')
        yield estate_loader.load_item()

