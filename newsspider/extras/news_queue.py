# -*- coding: utf-8 -*-

import redis


class Queue:
    def __init__(self, name, config):
        self._db = redis.Redis(host=config['host'], port=config['port'])
        self.key = '%s:%s' % (config['prefix'], name)

    def qsize(self):
        return self._db.llen(self.key)

    def empty(self):
        return self.qsize() == 0

    def put(self, item):
        self._db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        if block:  # 阻塞
            item = self._db.blpop(self.key, timeout=timeout)
            if item:
                item = item[1]
        else:  # 非阻塞
            item = self._db.lpop(self.key)
        return item

    # TODO: implement redis 的 保存时间


class QueueS:
    def __init__(self, config):
        self._db = redis.Redis(host=config['host'], port=config['port'], db=1)

    def qsize(self, key):
        return self._db.scard(key)

    def empty(self):
        return self.qsize() == 0

    def put(self, key, item):
        self._db.sadd(key, item)

    def checkValue(self, key, value):
        return self._db.sismember(key, value)


class QueueL:
    def __init__(self, config):
        self._db = redis.Redis(host=config['host'], port=config['port'],db=1)

    def qsize(self,key):
        return self._db.llen(key)

    def empty(self):
        return self.qsize() == 0

    def put(self,key,item):
        return self._db.rpush(key, item)

    def get(self,key):
        return self._db.lrange(key,0,-1)
