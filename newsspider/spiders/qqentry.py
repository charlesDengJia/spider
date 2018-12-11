# -*- coding: utf-8 -*-
import scrapy


class QqentrySpider(scrapy.Spider):
    name = 'qqentry'
    allowed_domains = ['http://health.qq.com']
    start_urls = ['http://http://health.qq.com/']

    def parse(self, response):
        pass
