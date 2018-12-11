# -*- coding: utf-8 -*-
import scrapy

from newsspider.extras import entry_config as config

from newsspider.extras import newsspider_database as database

from newsspider.extras import news_queue as queue
from newsspider.extras import utils
import json


class QqentrySpider(scrapy.Spider):
    name = 'qqentry'
    allowed_domains = ['http://health.qq.com']
    start_urls = ['http://http://health.qq.com/']

    def start_requests(self):
        database.init_database(config.db)
        config.queue['prefix'] = 'news_entry_qq'

        for job in utils.fetch_jobs(database, queue, config):
            url = job['url']
            meta = job
            meta['config'] = config
            meta['database'] = database
            meta['parse'] = self.parse_page
            if utils.check_domain(url, QqentrySpider.allowed_domains):
                yield scrapy.Request(url, callback=utils.parse, dont_filter=True, meta=meta)

    def parse_page(self, driver, url):
        productdict = {}
        products = []
        disabled = None
        i=0

        while True:
            i += 1
            print("i:", i)
            if i > 50:
                print("break")
                break;
            try:
                elements = utils.find_elements_by_css_selector(driver, '#listZone > div.sBox > div.bd > h2 > a')

                for element in elements:
                    print(element.get_attribute('href').strip())
                    products.append(element.get_attribute('href').strip())

                next_item_list = utils.find_elements_by_css_selector(driver, '#pageZone > span ')
                utils.sleep(2)

                for item in next_item_list:
                    if "转到下一页" == item.get_attribute('title'):
                        next_item = utils.find_element_by_css_selector(item, '#pageZone > span >a')
                        next_item.click()
                        disabled = utils.find_element_by_css_selector(item, '#pageZone > span.Disabled')
                    if '下一页' == item.get_attribute('title'):
                        break;

                if disabled:
                    break;
            except:
                continue


        productdict['products'] = ';'.join(products)

        if 'jbkp' in url:
            productdict['class'] = '疾病'
        elif 'shbj' in url:
            productdict['class'] = '养生'
        else:
            productdict['class'] = ''

        return json.dumps(productdict), None
