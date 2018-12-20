# -*- coding: utf-8 -*-

from datetime import datetime
import json
from newsspider.extras import product_config as configp

from newsspider.extras import newsspider_database as database_product


class NewsspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class NewsPipeline(object):
    def process_item(self, item, spider):
        content = item['content']
        database = item['database']

        if spider.name.endswith('entry'):
            database_product.init_database(configp.db)
            urls = []
            result_content = json.loads(content)
            productlist = result_content['products']
            typeclass = None
            if 'class' in result_content.keys():
                typeclass = result_content['class']
            for item in productlist.split(';'):
                productitem = {}
                productitem['url'] = item
                productitem['class'] = typeclass
                urls.append(json.dumps(productitem))

            urls = set(urls)  # 数据去重复
            for url in urls:
                result = database_product.Source.select(). \
                    where(database_product.Source.url == url)
                if not result:
                    database_product.Source(url=url).save()

        else:

            if content:
                try:
                    html = item['html']
                except:
                    html = None

                result = database.Result.select(). \
                    where(database.Result.source_id == item['source_id'])
                if result:
                    result = result.get()
                    result.updated_at = datetime.now()
                else:
                    result = database.Result()
                    result.source_id = item['source_id']
                result.content = content
                result.html = html
                result.save()

                # todo:
                source = database.Source.select().where(database.Source.id == item['source_id'])
                source = source.get()
                source.updated_at = datetime.now()
                source.enabled = False
                source.save()

                job = database.Job.select(). \
                    where(database.Job.id == item['job_id']).get()
                job.status = item['status']
                job.message = item['message']
                job.updated_at = datetime.now()
                job.save()
