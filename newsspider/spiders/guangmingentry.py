# -*- coding: utf-8 -*-
import scrapy
from newsspider.extras import entry_config as config

from newsspider.extras import newsspider_database as database

from newsspider.extras import news_queue as queue
from newsspider.extras import utils
import json


class GuangmingentrySpider(scrapy.Spider):
    name = 'guangmingentry'
    allowed_domains = ['gmw.cn']
    start_urls = ['http://gmw.cn/']

    def start_requests(self):
        database.init_database(config.db)
        config.queue['prefix'] = 'news_entry_gmw'

        for job in utils.fetch_jobs(database, queue, config):
            url = job['url']
            meta = job
            meta['config'] = config
            meta['database'] = database
            meta['parse'] = self.parse_page
            if utils.check_domain(url, GuangmingentrySpider.allowed_domains):
                yield scrapy.Request(url, callback=utils.parse, dont_filter=True, meta=meta)

    def parse_page(self, driver, url):
        products = []
        productdict = {}
        i = 0

        while i < 12:
            try:
                utils.sleep(2)
                i += 1
                elements = driver.find_elements_by_css_selector(
                    'body > div.channelMain > div.channelLeftPart > div > ul > li > a')

                for element in elements:
                    products.append(element.get_attribute('href').strip())

                button_list = driver.find_elements_by_css_selector('#displaypagenum > center > a')

                for button in button_list:
                    if '下一页' == button.text:
                        button.click()

                utils.sleep(2)

                h = driver.window_handles
                driver.switch_to_window(h[i])

            except:
                break;

        print("products_lens:", len(products))

        productdict['products'] = ';'.join(products)
        if "12212" in url:
            productdict['class'] = '美容美体'
        elif '12207' in url:
            productdict['class'] = '营养保健'
        elif '12206' in url:
            productdict['class'] = '健康常识'
        else:
            productdict['class'] = ''

        return json.dumps(productdict), None
