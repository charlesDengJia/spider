# -*- coding: utf-8 -*-

import argparse
import datetime as dt
import importlib
import inspect
import sys
import traceback
from peewee import BooleanField  # peewee相关模块
from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import Model
from peewee import MySQLDatabase
from peewee import TextField


class Task(Model):
    status = CharField()
    jobs = IntegerField(default=0)
    finished = IntegerField(default=0)
    unfinished = IntegerField(default=0)
    failed = IntegerField(default=0)
    created_at = DateTimeField(default=dt.datetime.now)
    updated_at = DateTimeField(default=dt.datetime.now)

    class Meta:
        database = None


class Job(Model):
    task_id = IntegerField()
    source_id = IntegerField()
    status = CharField()
    message = TextField(default='')
    created_at = DateTimeField(default=dt.datetime.now)
    updated_at = DateTimeField(default=dt.datetime.now)

    class Meta:
        database = None


class Source(Model):
    url = TextField()
    enabled = BooleanField(default=True)
    created_at = DateTimeField(default=dt.datetime.now)
    updated_at = DateTimeField(default=dt.datetime.now)

    class Meta:
        database = None


class Result(Model):
    content = TextField()
    html = TextField()
    simhash = TextField()
    source_id = IntegerField()
    created_at = DateTimeField(default=dt.datetime.now)
    updated_at = DateTimeField(default=dt.datetime.now)

    class Meta:
        database = None


def init_database(config):
    db = MySQLDatabase(host=config['host'],
                       user=config['user'],
                       passwd=config['passwd'],
                       database=config['database'],
                       charset=config['charset'])
    for var in dir(sys.modules[__name__]):
        if var != 'Model':
            obj = eval(var)
            if inspect.isclass(obj) and issubclass(obj, Model):
                obj._meta.database = db

    return db


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config')
    args = parser.parse_args()
    if args.config.endswith('.py'):
        args.config = args.config[:-3]
    return args


if __name__ == '__main__':
    database = None
    args = parse_args()
    try:
        config = importlib.import_module(args.config)
        database = init_database(config.db)
        tables = []
        for var in dir(sys.modules[__name__]):
            if var != 'Model':
                obj = eval(var)
                if inspect.isclass(obj) and issubclass(obj, Model):
                    tables.append(obj)
        database.connect()
        database.create_tables(Task, safe=True)
    except Exception as e:
        print('%s\n%s' % (e, traceback.print_exc()))
    finally:
        if database:
            database.close()
