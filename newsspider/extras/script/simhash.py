import argparse
import importlib
import sys
import traceback
import jieba
import datetime as dt
import inspect

sys.path.append('../')
import newsspider_database as database
import json
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config',
                        default='product_sohu_config')
    return parser.parse_args()


def string_hash(source):
    if source == "":
        return 0
    else:
        x = ord(source[0]) << 7
        m = 1000003
        mask = 2 ** 128 - 1
        for c in source:
            x = ((x * m) ^ ord(c)) & mask
        x ^= len(source)
        if x == -1:
            x = -2
        x = bin(x).replace('0b', '').zfill(64)[-64:]
        print(source, x)
        return str(x)


def cal_sim_hash(text):
    seg = jieba.cut(text)
    jieba.analyse.set_stop_words('/Users/jiadeng/Downloads/machinelearningown/stopwords.txt')
    keyword = jieba.analyse.extract_tags('|'.join(seg), topK=20, withWeight=True, allowPOS=())
    print(keyword)
    keyList = []
    for feature, weight in keyword:
        weight = int(weight * 100)
        feature = string_hash(feature)
        temp = []
        for i in feature:
            if (i == '1'):
                temp.append(weight)
            else:
                temp.append(-weight)
        #     print(temp)
        keyList.append(temp)
    list_sum = np.sum(np.array(keyList), axis=0)
    # print('list_sum:',list_sum)
    if (keyList == []):
        print('00')
    simhash = ''
    for i in list_sum:
        if i > 0:
            simhash = simhash + '1'
        else:
            simhash = simhash + '0'
    print(simhash)
    return simhash


if __name__ == '__main__':
    args = parse_args()
    config = importlib.import_module(args.config)
    try:
        database.init_database(config.db)
        for url in urls:
            result = database.Source.select(). \
                where(database.Source.url == url)
            if not result:
                database.Source(url=url).save()
    except Exception as e:
        print('%s\n%s' % (e, traceback.print_exc()))
