# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html


import random
import base64
from .settings import USER_AGENTS
from .settings import PROXIES

class RandomUserAgent(object):
    def process_request(self, request, spider):
        userAgent = random.choice(USER_AGENTS)
        # print(userAgent)
        request.headers.setdefault("User-Agent", userAgent)

class RandomProxy(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        # print(proxy)
        if proxy['user_password'] is None:
            # 没有代理账户验证的代理使用方式
            request.meta['proxy'] = "http://" + proxy['ip_port']
        else:
            # python3默认unicode编码，b64encode函数的参数byte类型，所以必须转码
            base64_userpasswd = base64.b64encode(proxy['user_password'].encode('utf-8'))
            # 将字节对象转为字符串 b'bXJfbWFvX2hhY2tlcjpzZmZxcnk5cg=='
            # print(str(base64_userpasswd, 'utf-8'))
            # 对应到代理服务器的信令格式里
            request.headers['Proxy-Authorization'] = 'Basic' + str(base64_userpasswd, 'utf-8')
            request.meta['proxy'] = "http://" + proxy['ip_port']
