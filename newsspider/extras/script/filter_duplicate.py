# -*- coding: utf-8 -*-

import simhash as sh
import argparse

import newsspider_database as database
import news_queue as queue
import importlib
import json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config',
                        default='product_config')
    parser.add_argument('-d',
                        '--domain')
    parser.add_argument('-r',
                        '--redis')
    return parser.parse_args()


def insertSimhash(queue_, data):
    for i in range(0, 4):
        queue_.put(data[i * 16:(i + 1) * 16], data)
        print("simhash插入", data)


def checkTheSimhashExcited(queue_, data):
    try:
        for i in range(0, 4):
            result_list = queue_.get(data[i * 16:(i + 1) * 16])
            for result_item in result_list:
                if sh.isDuplicated(str(result_item)[2:-1], data, 3):
                    print("simhash距离小有3", data)
                    return True
        insertSimhash(queue_, data)
    except Exception as e:
        print(e)
    return False


if __name__ == '__main__':
    args = parse_args()
    config = importlib.import_module(args.config)
    queue_ = queue.QueueL(config.queue)
    database.init_database(config.db)
    data = database.Result.select().where(
        database.Result.content.contains("www.sohu.com") & (
                database.Result.simhash.is_null(False) | database.Result.simhash != ""))
    i = 0
    for item in data:
        i += 1
        try:
            if not item.simhash.strip():
                continue
            ##是不是重复项
            if not checkTheSimhashExcited(queue_, item.simhash):
                article_info = json.loads(item.content)
                filter_item = database.Filter()
                filter_item.source_id = item.source_id
                filter_item.simhash = item.simhash
                filter_item.release_time = article_info['release_time']
                filter_item.text = article_info['text']
                filter_item.title = article_info['title']
                filter_item.images = article_info['images']
                filter_item.tag = article_info['tag']
                filter_item.source_from = article_info['web']
                filter_item.url = article_info['url']
                filter_item.class_type = article_info['class']
                filter_item.save()
        #         else:
        #             print(item.source_id)
        except Exception as e:
            print("save_exception:", item.source_id, e)
