# -*- coding: utf-8 -*-
import scrapy
from newsspider.extras import entry_sohu_config as config

from newsspider.extras import newsspider_database as database

from newsspider.extras import news_queue as queue
from newsspider.extras import utils
import json


class NewsentrySpider(scrapy.Spider):
    name = 'newsentry'
    allowed_domains = ['sohu.com']
    start_urls = ['http://sohu.com/']

    def start_requests(self):
        database.init_database(config.db)

        for job in utils.fetch_jobs(database, queue, config):
            url = job['url']
            meta = job
            meta['config'] = config
            meta['database'] = database
            meta['parse'] = self.parse_page
            if utils.check_domain(url, NewsentrySpider.allowed_domains):
                yield scrapy.Request(url, callback=utils.parse, dont_filter=True, meta=meta)

    def parse_page(self, driver, url):
        products = []
        product_count = 0
        productdict = {}
        while True:
            if 'tag' in url:
                elements = utils.find_elements_by_css_selector(driver,
                                                               '#news-wrapper > div > h4 > a')
            else:
                elements = utils.find_elements_by_css_selector(driver,
                                                               '#main-news > div > div.news-wrapper > div > h4 > a')

            if len(elements) > product_count:
                product_count = len(elements)
                driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
                utils.sleep(2)
            else:
                break

        for element in elements:
            products.append(element.get_attribute('href').strip())

        productdict['products'] = ';'.join(products)
        if url[-2:] == '32':
            productdict['class'] = '营养'
        elif url[-2:] == '23':
            productdict['class'] = '新闻'
        elif url[-2:] == '25':
            productdict['class'] = '内科'
        elif url[-2:] == '27':
            productdict['class'] = '妇产科'
        elif url[-2:] == '30':
            productdict['class'] = '肿瘤'
        elif url[-2:] == '26':
            productdict['class'] = '外科'
        elif url[-2:] == '28':
            productdict['class'] = '儿科'
        else:
            productdict['class'] = ''

        return json.dumps(productdict), None
