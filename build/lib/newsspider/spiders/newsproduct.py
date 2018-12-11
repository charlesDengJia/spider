# -*- coding: utf-8 -*-
import scrapy
from newsspider.extras import product_sohu_config as config
from newsspider.extras import newsspider_database as database
from newsspider.extras import news_queue as queue
from newsspider.extras import utils
import json


class NewsproductSpider(scrapy.Spider):
    name = 'newsproduct'
    allowed_domains = ['sohu.com']
    web = 'souhu'
    start_urls = ['http://sohu.com/']
    class_type = ''

    def start_requests(self):
        database.init_database(config.db)
        for job in utils.fetch_jobs(database, queue, config):
            url = job['url']
            url = json.loads(url)
            meta = job
            meta['config'] = config
            meta['database'] = database
            meta['parse'] = self.parse_page
            self.class_type = url['class']
            if utils.check_domain(url['url'], NewsproductSpider.allowed_domains):
                yield scrapy.Request(url['url'], callback=utils.parse, dont_filter=True, meta=meta)

    def parse_page(self, driver, url):
        url_dict = json.loads(url)
        product = {'url': url_dict['url'],
                   'web': NewsproductSpider.web,
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
                                                     '#article-container > div.left.main > div.text > div.text-title > h1')
        if element:
            product['title'] = element.text.strip()
        else:
            raise Exception('Title not found for %s' % driver.current_url)

        ##tag
        tags = utils.find_elements_by_css_selector(driver,
                                                   '#article-container > div.left.main > div.text > div.text-title > div.article-info > span.tag > a')
        taglist = []
        for tag in tags:
            print(tag.text)
            taglist.append(tag.text)
        product['tag'] = ";".join(taglist)

        # realse_time
        element = utils.find_element_by_css_selector(driver, 'span#news-time')
        product['release_time'] = element.text

        # article text
        textlist = []
        texts = utils.find_elements_by_css_selector(driver, 'article#mp-editor > p')
        for item in texts:
            textlist.append(item.text.strip())
        print("text:" + "\n".join(textlist))
        product['text'] = "\n".join(textlist)

        # images
        imagelist = []
        images = utils.find_elements_by_css_selector(driver, '#mp-editor > p > img')
        for image in images:
            imagelist.append(image.get_attribute('src'))
        product['images'] = ";".join(imagelist)

        product['class'] = self.class_type

        # html  标签文本
        element = utils.find_element_by_css_selector(driver, '#article-container > div.left.main')
        htmlvalue = None
        if element:
            htmlvalue = element.get_attribute('innerHTML').strip()
        return json.dumps(product), htmlvalue
