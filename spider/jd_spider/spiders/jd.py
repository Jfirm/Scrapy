# -*- coding: utf-8 -*-
import scrapy
from ..items import JdSpiderItem
from scrapy import Request
from scrapy_splash import SplashRequest


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    # start_urls = ['http://jd.com/']

    def start_requests(self):
        script = '''
                    function main(splash)
                        splash:set_viewport_size(1028, 10000)
                        splash:go(splash.args.url)
                        local scroll_to = splash:jsfunc("window.scrollTo")
                        scroll_to(0, 8000)
                        splash:wait(3)

                        return { 
                            html = splash:html() 
                        }
                    end
                  '''

        for i in range(1, 101):
            url = 'https://search.jd.com/Search?keyword=水果&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=水果&cid1=12218&stock=1&page=' + str(i * 2 - 1)
            yield SplashRequest(url, callback=self.start_parse, meta={
                'dont_redirect': True,
                'splash': {
                    'args': {
                        'lua_source': script, 'images': 0
                    },
                    'endpoint': 'execute',
                }
            })

    def start_parse(self, response):
        hrefs = response.xpath('//div[@class="p-name p-name-type-2"]/a/@href').extract()
        print(len(hrefs))
        for hf in hrefs:
            if 'http' not in hf:
                hf = 'https:' + hf
            print(hf)
            yield Request(hf, callback=self.parse)

    def parse(self, response):
        # data = response.body
        # b = BeautifulSoup(data, 'html.parser')
        # b.find()
        item = JdSpiderItem()
        brand = response.xpath('//ul[@id="parameter-brand"]/li/@title').extract()[0]
        flower = response.xpath('//ul[@class="parameter2 p-parameter-list"]//text()').extract()
        brand_name = "其他"
        # flower_num = "其他"
        flower_main = "其他"
        # text = etree.HTML(html)
        # flower = text.xpath('//ul[@class="parameter2 p-parameter-list"]//text()')
        for fl in flower:
            txt = fl.split('：')
            if len(txt) >= 2:
                # print(txt)
                if '商品名称' == txt[0]:
                    brand_name = txt[1]
                    continue

                # if '鲜花朵数' == txt[0]:
                #     flower_num = txt[1]
                #     continue

                if '分类' == txt[0]:
                    flower_main = txt[1]
                    continue
        # 品牌 商品名称 主花材 鲜花朵数
        temp = brand + ';' + brand_name + ';' + flower_main

        item['name'] = temp
        yield item


