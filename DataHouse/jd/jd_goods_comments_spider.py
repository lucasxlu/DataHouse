import json
import os
import sys
import time
import random

import requests

sys.path.append('../')
from DataHouse.jd.db_utils import insert_item


def crawl_comments_by_good_id(good_id):
    """
    crawl goods comments by good_id
    :param good_id:
    :return:
    """
    headers = {
        'DNT': '1',
        'Referer': 'https://item.jd.com/%d.html' % good_id,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }

    page = 0
    while True:
        print('crawling page %d' % page)
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1739&productId={0}' \
              '&score=0&sortType=5&page={1}&pageSize=10&isShadowSku=0&fold=1'.format(good_id, page)

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                js = json.loads(response.text.replace('fetchJSON_comment98vv1739', '')[1: -2], encoding='utf-8')
                print(js)
                insert_item(js)
            else:
                print('Error!!! {0}'.format(response.status_code))

            time.sleep(random.randint(2, 5))

            page += 1
        except:
            print('wrong HTTP request...')


if __name__ == '__main__':
    crawl_comments_by_good_id(10138091829)
