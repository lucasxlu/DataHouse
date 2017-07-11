"""
crawl douban book data from douban's RESTful API
"""
import requests
import time

import sys
from pymongo import MongoClient

SLEEP_TIME = 2


def crawl(start_num):
    base_url = 'https://book.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=%d' % start_num
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Referer': 'https://movie.douban.com/tag/',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/'
                      '9.0 Mobile/13B143 Safari/601.1',
    }

    response = requests.get(base_url, headers=headers, timeout=10)
    if response.status_code == 200:
        response_json = response.json()
        if len(response_json['data']) > 0:
            result = insert_many_items(response_json['data'])
            if result:
                print('Bulk Insert Successfully...')
            else:
                print('Bulk Insert Fails...')
        else:
            print('All data has been crawled down...')
            sys.exit(0)
    else:
        print('ERROR!!%d' % response.status_code)


def insert_item(item):
    client = MongoClient()
    db = client.douban.movie
    return db.insert_one(item)


def insert_many_items(items):
    client = MongoClient()
    db = client.douban.book
    return db.insert_many(items)


def query_document():
    client = MongoClient()
    db = client.douban.movie
    cursor = db.find()
    for document in cursor:
        print(document)


if __name__ == '__main__':
    for i in range(0, 10000, 20):
        crawl(i)
        time.sleep(SLEEP_TIME)
