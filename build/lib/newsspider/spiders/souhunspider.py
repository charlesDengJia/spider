# -*- coding: utf-8 -*-
import scrapy
from newsspider.extras import utils
import time
from newsspider.extras import entry_sohu_config as config
from newsspider.extras import newsspider_database as database


class SouhunspiderSpider(scrapy.Spider):
    name = 'souhunspider'
    allowed_domains = ['health.sohu.com']
    start_urls = ['http://health.sohu.com/']

    def start_requests(self):
        start_urls = ['http://health.sohu.com/']
        database.init_database(config.db)

        for url in start_urls:
            meta = {}
            meta['url'] = url
            meta['config'] = config
            meta['database'] = database
            meta['parse'] = self.parse_page
            yield scrapy.Request(url, callback=utils.parse, meta=meta)

    def parse_page(self, driver, url):
        elements = utils.find_elements_by_css_selector(driver, '#main-news > div > div.news-wrapper > div > h4 > a')
        contentlist = []
        for element in elements:
            article = {}
            ## 标题
            print(element.text)
            element.click()
            driver.implicitly_wait(30)
            h = driver.window_handles
            driver.switch_to_window(h[1])
            tags = utils.find_elements_by_css_selector(driver,
                                                       '#article-container > div.left.main > div.text > div.text-title > div.article-info > span.tag > a')
            ##获取当前网页地址
            currenturl = driver.current_url
            print("current:" + currenturl)
            article['current_url'] = currenturl
            ##标签获取
            taglist=[]
            for tag in tags:
                print(tag.text)
                taglist.append(tag.text)
            article['tag'] = ";".join(taglist)
            ##日期获取
            datetime = utils.find_element_by_css_selector(driver, 'span#news-time')
            article['release_time'] = datetime.text
            print("datetime:" + datetime.text)
            ##内容获取
            contents = utils.find_elements_by_css_selector(driver, 'article#mp-editor > p')
            for content in contents:
                contentlist.append(content.text)
            print("contents:" + "\n".join(contentlist))
            article['content'] = "\n".join(contentlist)
            time.sleep(1)
            driver.close()
            driver.switch_to_window(h[0])
            return article
        driver.quit()
