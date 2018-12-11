import argparse
import importlib
import sys
import traceback

sys.path.append('../')
import newsspider_database as database
import json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config',
                        default='entry_config')
    parser.add_argument('-f',
                        '--file')
    parser.add_argument('-tid',
                        '--task_id',
                        type=int,
                        default=-1)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    config = importlib.import_module(args.config)
    database.init_database(config.db)
    jobs = database.Job.select(). \
        where(database.Job.task_id == args.task_id)
    source_ids = []
    for job in jobs:
        source_ids.append(job.source_id)
    products = []
    for source_id in source_ids:
        result = database.Result.select(). \
            where(database.Result.source_id == source_id)

        if result:
            result = result.get()
            result_content = json.loads(result.content)
            productlist = result_content['products']
            if 'class' in result_content.keys():
                typeclass = result_content['class']
            for item in productlist.split(';'):
                productitem = {}
                productitem['url'] = item
                productitem['class'] = typeclass
                products.append(json.dumps(productitem))
    products = set(products)
    with open(args.file, 'w+') as f:
        for product in products:
            f.write(product + '\n')
