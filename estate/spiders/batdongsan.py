import scrapy
from scrapy_selenium import SeleniumRequest

from estate.items import EstateItem


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
        for estate in estates:
            estate_loader = BatdongsanLoader(
                item=EstateItem(), selector=estate)
            url = response.urljoin(estate.css('*::attr(href)').extract_first())
            estate_loader.add_value('url', url)
            yield SeleniumRequest(url, callback=self.parse_detail, meta={'item': estate_loader.load_item()})

    def parse_detail(self, response):
        estate_loader = response.meta['item']
        estate_loader['title'] = response.xpath(
            '//*[@class="re__pr-title pr-title"]/text()').extract_first()

        params = response.xpath('//*[@class="re__list-standard-1line--md"]')
        for param in params:
            if param.xpath("/span[@class='title']/text()").extract_first() == 'Địa chỉ:':
                estate_loader['address'] = param.xpath(
                    "/span[@class='content']/text()").extract_first()
            elif param.xpath("/span[@class='title']/text()").extract_first() == 'Đường vào:':
                estate_loader['street'] = param.xpath(
                    "/span[@class='content']/text()").extract_first()
