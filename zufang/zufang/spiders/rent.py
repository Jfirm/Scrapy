# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from zufang.items import ZufangItem
import re
class RentSpider(CrawlSpider):
    name = 'anjuke'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://sz.zu.anjuke.com/fangyuan/p1/']
    pageLink = LinkExtractor(allow=(r"p\d+"), restrict_xpaths="//div[@class='multi-page']")
    pageHref = LinkExtractor(allow=(r'//sz.zu.anjuke.com/fangyuan/\d+'))
    rules = [
        Rule(pageLink),
        Rule(pageHref, callback='parse_item', follow=False)
    ]


    # def start_parse(self, response):
    #     hrefs = response.xpath('//div[@class="zu-info"]/h3/a/@href').extract()
    #     print(len(hrefs))
    #     for href in hrefs:
    #         print(href)
    #         yield scrapy.Request(href, callback=self.parse_item)

    def parse_item(self, response):
        print(response.url)
        item = ZufangItem()
        item['type'] = self.get_type(response)
        item['location'] = self.get_location(response)
        item['area'] = self.get_area(response)
        item['pattern'] = self.get_pattern(response)
        item['rent'] = self.get_rent(response)
        item['decor'] = self.get_decor(response)
        item['eva'] = self.get_eva(response)

        yield item
    def get_type(self, response):
        ty = re.compile(r'<li class="title-label-item rent">(.*?)</li>')
        info = ty.findall(response.text)
        if len(info):
            type = info[0]
        else:
            type = "NULL"
        return type

    def get_location(self, response):
        info = response.xpath('//li[@class="house-info-item l-width"]/a/text()').extract()
        if len(info):
            location = info[0]
        else:
            location = "NULL"
        return location

    def get_area(self, response):
        info = response.xpath('//li[@class="house-info-item"]/span/text()').extract()
        if len(info):
            area = info[1]
        else:
            area = "NULL"
        return area

    def get_pattern(self, response):
        info = response.xpath('//li[@class="house-info-item l-width"]/span/text()').extract()
        if len(info):
            pattern = info[1]
        else:
            pattern = "NULL"

        return pattern

    def get_rent(self, response):
        info = response.xpath('//li[@class="full-line cf"]//em/text()').extract()
        if len(info):
            rent = info[0]
        else:
            rent = "NULL"

        return rent

    def get_decor(self, response):
        info = response.xpath('//li[@class="house-info-item"]/span/text()').extract()
        if len(info):
            decor = info[5]
        else:
            decor = "NULL"

        return decor

    def get_eva(self, response):
        p = re.compile('<em class="score-num" style="margin-top: -7px;">(.*?)</em>')
        info = p.findall(response.text)
        if len(info):
            eva = info[0]
        else:
            eva = "NULL"

        return eva