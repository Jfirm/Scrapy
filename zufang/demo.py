#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : demo.py
@Author: HJ
@Date  : 2018/9/5 10:41
'''
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',

    }
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()  # 如果状态码不是200，将引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'

def get_brand(html):
    text = etree.HTML(html)
    info = text.xpath('//div[@class="zu-info"]/h3/a/@href')
    # print(brands)
    return info
if __name__ == "__main__":
    url = 'https://sz.zu.anjuke.com/fangyuan/p10/'
    html = get_html(url)
    # print(html)
    info = get_brand(html)
    print(info)
