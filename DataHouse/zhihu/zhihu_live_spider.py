"""
a web spider for Zhihu Live
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
                    filename='zhihu_live.log',
                    filemode='w')


def crawl(pagenum):
    """
    crawl Zhihu live's info belongs to one page
    :param pagenum:
    :return:
    :Version:1.0
    """
    url_pattern = 'https://api.zhihu.com/lives?limit=10&offset=%d&includes=live' % pagenum
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
    recursively crawl all Zhihu live data
    :return:
    "Version:1.0
    """
    offset = 10
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
            logging.error('https://api.zhihu.com/lives?limit=10&offset=%d&includes=live' % offset)


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


def output_fields_from_mongo():
    """
    extract simpler info zhihu live's info from mongodb and output to XLSX file
    :return:
    :Version:1.0
    """
    client = MongoClient()
    db = client.zhihu.live
    lives = db.find({"status": "ended"})

    live_info = []

    for live in lives:
        subject = live['subject']  # Live名称
        name = live['speaker']['member']['name']  # 主讲人
        attachment_count = live['attachment_count']  # 文件数量
        speaker_audio_message_count = live['speaker_audio_message_count']
        duration = live['duration'] / 60
        original_price = live['fee']['original_price']  # Live单价
        in_promotion = live['in_promotion']  # 是否促销
        has_authenticated = 1 if live['has_authenticated'] == "true" else 0  # 主讲人是否实名认证
        user_type = live['speaker']['member']['user_type']  # 用户类型
        headline = live['speaker']['member']['headline']  # 主讲人个性签名
        gender = live['speaker']['member']['gender']  # 主讲人性别
        speaker_message_count = live['speaker_message_count']
        tags = '|'.join([tag['name'] for tag in live['tags']])
        tag_id = '|'.join([str(tag['id']) for tag in live['tags']])
        liked_num = live['liked_num']
        review_count = live['review']['count']  # Live评价数量
        review_score = live['review']['score']  # Live 评分
        reply_message_count = live['reply_message_count']  # 问答数量
        seats_taken = live['seats']['taken']  # 参与人数
        seats_max = live['seats']['max']  # 最多人数

        cols = ['subject', 'name', 'attachment_count', 'speaker_audio_message_count', 'duration',
                'original_price', 'in_promotion', 'has_authenticated', 'user_type', 'headline', 'gender',
                'speaker_message_count', 'tags', 'tag_id', 'liked_num', 'review_count', 'review_score',
                'reply_message_count', 'seats_taken', 'seats_max']

        live_info.append([subject, name, attachment_count, speaker_audio_message_count, duration,
                          original_price, in_promotion, has_authenticated, user_type, headline, gender,
                          speaker_message_count, tags, tag_id, liked_num, review_count, review_score,
                          reply_message_count, seats_taken, seats_max])

    df = pd.DataFrame(live_info, columns=cols)
    df.to_excel(excel_writer='D:/ZhihuLive.xlsx', sheet_name='ZhihuLive', index=False)
    logging.info('Excel file has been generated...')


if __name__ == '__main__':
    recursive_crawl()
    # output_fields_from_mongo()
