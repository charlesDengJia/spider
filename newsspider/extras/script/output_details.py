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
                        default='product_sohu_config')
    parser.add_argument('-f',
                        '--file')
    parser.add_argument('-b',
                        '--brand')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    web = args.brand
    config = importlib.import_module(args.config)
    database.init_database(config.db)
    results = database.Result.select()
    sources = database.Source.select()
    with open(args.file, 'w+', encoding='utf-8') as f:
        for result in results:
            try:
                source = sources.where(database.Source.id == result.source_id).get()
                data = json.loads(result.content)
                if data['web'] == web:
                    data['url'] = json.loads(source.url)['url']
                    data = str(data).replace("'", '"')
                    f.write(data + '\n')
            except:
                continue
