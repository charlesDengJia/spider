# -*- coding: utf-8 -*-
import scrapy


class QqproductSpider(scrapy.Spider):
    name = 'qqproduct'
    allowed_domains = ['http://health.qq.com']
    start_urls = ['http://http://health.qq.com/']

    def parse(self, response):
        pass
