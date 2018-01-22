"""
a web spider for Zhihu Live
"""
import logging
import random
import time
import time

import jieba
import jieba.analyse
import pandas as pd
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
    url_pattern = 'https://api.zhihu.com/lives?limit=10&offset=%d&includes=live' % pagenum
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'api.zhihu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    }
    cookies = dict(
        cookies_are='')

    response = requests.get(url=url_pattern, headers=headers, cookies=cookies, timeout=20)
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
    # lives = db.find({"status": "ended", "review.count": {"$gt": 50}})

    live_info = []

    for live in lives:
        id = live['id']
        created_at = str(live['created_at'])
        starts_at = str(live['starts_at'])
        speaker_name = live['speaker']['member']['name']
        speaker_url = live['speaker']['member']['url_token']
        live_subject = live['subject']
        live_id = live['id']
        in_promotion = int(live['in_promotion'])
        duration = live['duration']
        reply_message_count = live['reply_message_count']
        source = 1 if live['source'] == 'admin' else 0
        purchasable = int(live['purchasable'])
        is_refundable = int(live['is_refundable'])
        has_authenticated = int(live['has_authenticated'])
        user_type = 0 if live['speaker']['member']['user_type'] == 'organization' else 1
        gender = live['speaker']['member']['gender']
        badge = len(live['speaker']['member']['badge'])
        tags = live['tags']
        tag_id = tags[0]['id'] if len(tags) > 0 else None
        tag_name = tags[0]['name'] if len(tags) > 0 else ''
        speaker_audio_message_count = live['speaker_audio_message_count']
        attachment_count = live['attachment_count']
        liked_num = live['liked_num']
        is_commercial = int(live['is_commercial'])
        audition_message_count = live['audition_message_count']
        is_audition_open = int(live['is_audition_open'])
        seats_taken = live['seats']['taken']
        seats_max = live['seats']['max']
        speaker_message_count = live['speaker_message_count']
        amount = live['fee']['amount']
        original_price = live['fee']['original_price'] / 100
        buyable = int(live['buyable'])
        has_audition = int(live['has_audition'])
        has_feedback = int(live['has_feedback'])
        is_public = live['is_public']
        review_count = live['review']['count']
        review_score = live['review']['score']

        live_info.append(
            [id, created_at, starts_at, speaker_name, speaker_url, live_subject, live_id, in_promotion, duration,
             reply_message_count, source, purchasable, is_refundable, has_authenticated,
             user_type, gender, badge, tag_id, tag_name, speaker_audio_message_count, attachment_count, liked_num,
             is_commercial, audition_message_count, is_audition_open, seats_taken, seats_max, speaker_message_count,
             amount, original_price, buyable, has_audition, has_feedback, is_public, review_count, review_score])

    cols = ['id', 'created_at', 'starts_at', 'speaker_name', 'speaker_url', 'live_subject', 'live_id', 'in_promotion',
            'duration', 'reply_message_count', 'source', 'purchasable',
            'is_refundable', 'has_authenticated', 'user_type', 'gender', 'badge', 'tag_id', 'tag_name',
            'speaker_audio_message_count', 'attachment_count', 'liked_num', 'is_commercial',
            'audition_message_count', 'is_audition_open', 'seats_taken', 'seats_max', 'speaker_message_count', 'amount',
            'original_price', 'buyable', 'has_audition', 'has_feedback', 'is_public', 'review_count', 'review_score']

    df = pd.DataFrame(live_info, columns=cols)
    df.to_excel(excel_writer='./ZhihuLiveDB.xlsx', sheet_name='ZhihuLive', index=False)
    logging.info('Excel file has been generated...')


def text_analysis(high_quality=True, score_margin=4):
    """
    text analysis with jieba
    :param high_quality:
    :return:
    """
    client = MongoClient()
    db = client.zhihu.live
    if high_quality:
        lives = db.find({"status": "ended", "review.score": {"$gt": score_margin}}, {"description": 1, "_id": 0})
    else:
        lives = db.find({"status": "ended", "review.score": {"$lt": score_margin}}, {"description": 1, "_id": 0})

    text = ''.join([live['description'] for live in lives])

    jieba.analyse.set_stop_words('./stopwords.txt')
    jieba.load_userdict('./userdict.txt')
    word_list = jieba.analyse.extract_tags(text, topK=30, withWeight=True, allowPOS=())
    for _ in word_list:
        print(_[0] + ', ' + str(_[1]))


if __name__ == '__main__':
    # recursive_crawl()
    output_fields_from_mongo()
    # text_analysis(True, 4.2)
