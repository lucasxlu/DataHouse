"""
a web spider for Zhihu Course
"""
import random
import os
import time
import logging

import requests
from pymongo import MongoClient
import pandas as pd

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='zhihu_course.log',
                    filemode='w')


def crawl(pagenum):
    url_pattern = 'https://api.zhihu.com/lives/special_lists?limit=10&offset=%d&subtype=course' % pagenum
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'api.zhihu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    }
    cookies = dict(
        cookies_are='')

    response = requests.get(url=url_pattern, headers=headers, cookies=cookies)
    if response.status_code == 200:
        live_json = response.json()
        time.sleep(random.randint(2, 5))  # a range between 2s and 5s

        return live_json
    else:
        print('ERROR, code is %d' % response.status_code)

        return None


def recursive_crawl():
    """
    recursively crawl all Zhihu course data
    :return:
    "Version:1.0
    """
    offset = 0
    while True:
        try:
            obj = crawl(offset)
            if obj is not None and len(obj['data']) > 0:
                for _ in obj['data']:
                    insert_item(_)
                    print('insert one item successfully~')
                offset += 10
            else:
                break
        except:
            logging.error('https://api.zhihu.com/lives/special_lists?limit=10&offset=%d&subtype=course' % offset)


def insert_item(item):
    """
    insert an item into MongoDB
    :param item:
    :return:
    :Version:1.0
    """
    client = MongoClient()
    db = client.zhihu.course

    result = db.insert_one(item)


if __name__ == '__main__':
    recursive_crawl()
