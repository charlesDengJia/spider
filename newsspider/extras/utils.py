# -*- coding: utf-8 -*-

import scrapy
import time
import traceback
from selenium import webdriver
import json
import random



def sleep(seconds):
    time.sleep(seconds)


def create_chrome_driver():
    agents = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
              'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
              "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
              "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
              "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
              "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
              "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
              "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
              "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
              "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
              "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
              "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
              "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
              "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
              "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
              "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"]

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('user-agent=' + agents[random.randint(0, len(agents) - 1)])

    driver = webdriver.Chrome(chrome_options=options)

    driver.maximize_window()
    return driver


def find_element_by_css_selector(element, selector):
    try:
        return element.find_element_by_css_selector(selector)
    except:
        return None


def find_elements_by_css_selector(element, selector):
    try:
        return element.find_elements_by_css_selector(selector)
    except:
        return []


def check_domain(url, domains):
    for domain in domains:
        if domain in url:
            print('%s, %s is True' % (domain, url))
            return True
    return False


def fetch_jobs(database, queue, config):
    try:
        tasks = database.Task
        for task in tasks.select().where(tasks.status == config.ts_inprogress):
            queue_ = queue.Queue(task.id, config.queue)
            while not queue_.empty():
                job = queue_.get(False)
                if job:
                    yield json.loads(job)
    except Exception as e:
        print('%s\n%s' % (e, traceback.format_exc()))
    return 'Done'


def build_result(meta):
    result = {}
    result['job_id'] = meta['id']
    result['source_id'] = meta['source_id']
    result['content'] = ''
    result['message'] = ''  # 失败原因
    return result


def parse(response):
    driver = response.driver
    meta = response.meta
    config = meta['config']
    database = meta['database']
    url = meta['url']
    result = build_result(meta)
    try:
        result['content'], result['html'] = meta['parse'](driver, url)
        result['status'] = config.js_finished
    except Exception as e:
        result['message'] = '%s\n%s' % (e, traceback.format_exc())
        result['status'] = config.js_failed
    finally:
        if driver:
            driver.quit()
    result['database'] = database
    yield result
