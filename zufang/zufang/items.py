# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangItem(scrapy.Item):
    # 整租合租
    type = scrapy.Field()
    # 房屋地址
    location = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 格局
    pattern = scrapy.Field()
    # 租金
    rent = scrapy.Field()
    # 装修
    decor = scrapy.Field()
    # 评价
    eva = scrapy.Field()