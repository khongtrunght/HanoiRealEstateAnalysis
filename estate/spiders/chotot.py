import scrapy
from estate.items import EstateItem
from datetime import datetime
import re
from scrapy_selenium import SeleniumRequest

class test(scrapy.Spider):
    name = "chotot"
    start_urls = [f'https://nha.chotot.com/ha-noi/mua-ban-nha-dat?page={i}' for i in range(1, 3)]
    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)
    def parse(self, response):
        estates = response.xpath("//div[contains(@class, 'ListAds_ListAds__1z6Pv col-xs-12 no-padding')]//a/@href")
        for href in estates:
            url = "https://nha.chotot.com/" + (href.extract()).split('/')[4]
            yield SeleniumRequest(url=url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = EstateItem()

        # item['Area'] = response.xpath("//span[@itemprop = 'size']").extract()
        # item['Price'] = response.xpath("//span[contains(@itemprop, 'price')]/text()").extract()[0]
        #
        # address = response.xpath("//span[@class = 'fz13']/text()").extract()
        # if len(address) == 0:
        #     item['address'] = None
        # else:
        item['address'] = response.xpath("//span[@class = 'fz13']/text()").extract()
        #
        # item['numFloor'] = response.xpath("//span[@itemprop = 'floors']/text()").extract()[0]
        item['numBed'] = response.xpath("//span[@itemprop = 'rooms']/text()").extract()[0]
        item['numBath'] = response.xpath("//span[@itemprop = 'toilets']/text()").extract()[0]
        # item['direction'] = response.xpath("//span[@itemprop = 'direction']/text()").extract()[0]
        # item['type'] = response.xpath("//span[@itemprop = 'name']/text()").extract()[3]
        # item['url'] = response.xpath("//link[@rel = 'canonical']//@href").extract()[0]

        yield item

