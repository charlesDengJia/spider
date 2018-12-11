# -*- coding: utf-8 -*-
import scrapy
from newsspider.extras import entry_config as config
from newsspider.extras import newsspider_database as database
from newsspider.extras import news_queue as queue
from newsspider.extras import utils
import json


class WangyientrySpider(scrapy.Spider):
    name = 'wangyientry'
    allowed_domains = ['163.com']
    start_urls = ['http://163.com/']

    def start_requests(self):
        database.init_database(config.db)
        config.queue['prefix'] = 'news_entry_wangyi'

        for job in utils.fetch_jobs(database, queue, config):
            url = job['url']
            meta = job
            meta['config'] = config
            meta['database'] = database
            meta['parse'] = self.parse_page
            if utils.check_domain(url, WangyientrySpider.allowed_domains):
                yield scrapy.Request(url, callback=utils.parse, dont_filter=True, meta=meta)

    def parse_page(self, driver, url):
        products = []
        next = True
        productdict = {}

        while next != None:

            elements = utils.find_elements_by_css_selector(driver,
                                                           '#newidx_news_container > div.news_list_container.clearfix > div > div.news_main_info > h2 > a')

            for element in elements:
                products.append(element.get_attribute('href').strip())

            next = utils.find_element_by_css_selector(driver,
                                                      '#newidx_news_container > div.bizidx_pages.bizidx_news_pages > a.next_page')
            if next:
                next.click()
            productdict['products'] = ';'.join(products)

        if url[-1:] == '1':
            productdict['class'] = '养生'
        elif url[-1:] == '2':
            productdict['class'] = '饮食'
        elif url[-1:] == '3':
            productdict['class'] = '医美'
        elif url[-1:] == '4':
            productdict['class'] = '基因'
        elif url[-1:] == '5':
            productdict['class'] = '专家'
        else:
            productdict['class'] = None

        return json.dumps(productdict), None
