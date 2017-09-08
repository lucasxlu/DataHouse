import csv

import requests
from bs4 import BeautifulSoup
from lxml import etree
from io import StringIO, BytesIO
from pymongo import MongoClient
import pandas as pd


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def crawl_comment(shop_id, pageno):
    """
    unfinished!
    :param shop_id:
    :param pageno:
    :return:
    """
    url = 'http://www.dianping.com/shop/%s/review_more?pageno=%d' % (str(shop_id), pageno)
    headers = {
        'Host': 'www.dianping.com',
        'Referer': 'http://www.dianping.com/shop/19266073/review_more',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html5lib')

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(response.text), parser)
    for _ in tree.xpath('//div[@class="comment-list"]/ul/li'):
        print(_)
        # for span in _.xpath('div[@class="content"]/div[@class="user-info"]/span/text()'):
        #     print(span.text)


def read_mongo(db, collection, query={}, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Make a query to the specific DB and Collection
    cursor = list(db[collection].find(query))
    df = pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df


if __name__ == '__main__':
    # crawl_comment(19266073, 23)
    df = read_mongo(_connect_mongo("localhost", 27017, None, None, "dianping"), "food", {"cityName": "兰州"})
    result = {}
    for _ in df['dishtags']:
        if type(_) is str:
            for dish in _.split('|'):
                dish_name = dish.split(',')[0].strip() if ',' in dish else dish
                if '' != dish_name:
                    if dish_name in result.keys():
                        result[dish_name] += 1
                    else:
                        result[dish_name] = 1

    sorted_items = sorted(result.items(), key=lambda d: d[1], reverse=True)
    for _ in sorted_items[0: 800]:
        print(_[0] + '\t' + str(_[1]))
        #
        # index = 0
        # for item in sorted_items:
        #     while index < 30:
        #         print(item)
        #         index += 1
