"""
a web spider for Zhihu Live
"""
import random
import os
import time
import logging

import requests
from pymongo import MongoClient

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='zhihu_live.log',
                    filemode='w')


def crawl(pagenum):
    """
    crawl Zhihu live's info belongs to one page
    :param pagenum:
    :return:
    :Version:1.0
    """
    url_pattern = 'https://api.zhihu.com/lives/homefeed?limit=10&offset=%d&includes=live' % pagenum
    headers = {
        'accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'api.zhihu.com',
        'Origin': 'https://www.zhihu.com',
        'Referer': 'https://www.zhihu.com/lives/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'X-Api-Version': '3.0.63'
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
    recursively crawl all Zhihu live data
    :return:
    "Version:1.0
    """
    offset = 10
    while True:
        try:
            obj = crawl(offset)
            if obj is not None and obj['paging']['is_end'] == False:
                for _ in obj['data']:
                    insert_item(_)
                    print('insert one item successfully~')
                offset += 10
            else:
                break
        except:
            logging.error('https://api.zhihu.com/lives/homefeed?limit=10&offset=%d&includes=live' % offset)


def insert_item(item):
    """
    insert an item into MongoDB
    :param item:
    :return:
    :Version:1.0
    """
    client = MongoClient()
    db = client.zhihu.live

    result = db.insert_one(item)


if __name__ == '__main__':
    recursive_crawl()
