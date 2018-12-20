# -*- coding: utf-8 -*-
import scrapy

from newsspider.extras import product_config as config

from newsspider.extras import newsspider_database as database

from newsspider.extras import news_queue as queue
from newsspider.extras import utils
import json


class GuangmingproductSpider(scrapy.Spider):
    name = 'guangmingproduct'
    allowed_domains = ['gmw.cn']
    start_urls = ['http://gmw.cn/']
    class_type = ''
    web = 'gmw'

    def start_requests(self):
        database.init_database(config.db)
        config.queue['prefix'] = 'news_product_gmw'

        for job in utils.fetch_jobs(database, queue, config):
            url = job['url']
            url = json.loads(url)
            meta = job
            meta['config'] = config
            meta['database'] = database
            meta['parse'] = self.parse_page
            self.class_type = url['class']
            if utils.check_domain(url['url'], GuangmingproductSpider.allowed_domains):
                yield scrapy.Request(url['url'], callback=utils.parse, dont_filter=True, meta=meta)

    def parse_page(self, driver, url):
        url_dict = json.loads(url)
        product = {'url': url_dict['url'],
                   'web': GuangmingproductSpider.web,
                   'tag': '',
                   'release_time': 0,
                   'images': '',
                   'text': ''}
        # check 404
        element = utils.find_element_by_css_selector(driver, 'div.nofound')
        if element:
            raise Exception('404 page not found')
        # title
        element = utils.find_element_by_css_selector(driver,
                                                     'body > div.g-main > div.m-title-box > h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found for %s' % driver.current_url)

        # realse_time
        element = utils.find_element_by_css_selector(driver,
                                                     'body > div.g-main > div.m-title-box > div > span.m-con-time')
        product['release_time'] = element.text

        # article text
        textlist = []
        texts = utils.find_elements_by_css_selector(driver, '#article_inbox > div.u-mainText > p')
        if not texts:
            texts = utils.find_elements_by_css_selector(driver, '#contentMain > p')

        for item in texts:
            textlist.append(item.text.strip())
        print("text:" + "\n".join(textlist))
        product['text'] = "\n".join(textlist)

        product['class'] = self.class_type

        # html  标签文本
        element = utils.find_element_by_css_selector(driver, 'body > div.g-main')
        htmlvalue = None
        if element:
            htmlvalue = element.get_attribute('innerHTML').strip()
        return json.dumps(product), htmlvalue
