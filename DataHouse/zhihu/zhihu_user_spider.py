"""
a web spider for Zhihu user's information
"""
import json
import random
import time

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


def crawl_zhihu_user(user_id='xulu-0620'):
    """
    crawl a Zhihu user's info by user_id
    :param user_id:
    :return:
    :Version:1.0
    """
    zhihu_user = {}
    user_page = 'https://www.zhihu.com/people/%s/activities' % user_id
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'www.zhihu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/'
                      '9.0 Mobile/13B143 Safari/601.1'
    }
    response = requests.get(user_page, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')
        json_obj = json.loads(soup.find(id="data")['data-state'])
        person_obj = json_obj['entities']['users'][user_id]
        zhihu_user['userId'] = user_id  # 用户ID
        zhihu_user['followerCount'] = person_obj['followerCount']  # 粉丝数量
        zhihu_user['userType'] = person_obj['userType']  # 用户类型
        zhihu_user['followingCount'] = person_obj['followingCount']  # 关注人数
        zhihu_user['followingTopicCount'] = person_obj['followingTopicCount']  # 关注话题数量
        zhihu_user['hostedLiveCount'] = person_obj['hostedLiveCount']  # 举办Live数量
        zhihu_user['favoritedCount'] = person_obj['favoritedCount']  # 答案被收藏数量
        zhihu_user['voteupCount'] = person_obj['voteupCount']  # 答案被点赞数量
        zhihu_user['answerCount'] = person_obj['answerCount']  # 回答数量
        zhihu_user['questionCount'] = person_obj['questionCount']  # 提问数量
        zhihu_user['thankedCount'] = person_obj['thankedCount']  # 感谢数量
        zhihu_user['articlesCount'] = person_obj['articlesCount']  # 发表文章数量
        zhihu_user['columnsCount'] = person_obj['columnsCount']  # 专栏数量
        zhihu_user['favoriteCount'] = person_obj['favoriteCount']  # 收藏数量
        zhihu_user['markedAnswersCount'] = person_obj['markedAnswersCount']  # 编辑收录答案数量
        try:
            zhihu_user['educations'] = person_obj['educations']  # 教育经历
            zhihu_user['employments'] = person_obj['employments']  # 工作经历
            zhihu_user['locations'] = person_obj['locations']  # 地址
            zhihu_user['business'] = person_obj['business']  # 行业
            zhihu_user['gender'] = person_obj['gender']  # 性别
            zhihu_user['badge'] = person_obj['badge']  # 话题优秀回答者
            zhihu_user['name'] = person_obj['name']  # 话题优秀回答者

        except:
            pass
        print(zhihu_user)
        insert_item(zhihu_user)
        time.sleep(random.randint(2, 5))  # a range between 2s and 5s

    else:
        print('Error ! error code is %d' % response.status_code)


def crawl_zhihu_user_by_api(user_id='xulu-0620'):
    """
    crawl zhihu user info by zhihu api v4
    :param user_id:
    :return:
    """
    req_url = 'https://www.zhihu.com/api/v4/members/%s' % str(user_id)
    payload = {
        'include': 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,'
                   'following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,'
                   'following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,'
                   'columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,'
                   'included_answers_count,included_articles_count,included_text,message_thread_token,account_status,'
                   'is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,'
                   'sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,'
                   'is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,'
                   'thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,'
                   'industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Host': 'www.zhihu.com',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }

    cookies = dict(
        cookies_are='')

    response = requests.get(url=req_url, headers=headers, cookies=cookies, params=payload)
    print(response.url)
    if response.status_code == 200:
        user_obj = response.json()
        print(user_obj)
        insert_item(user_obj)
    else:
        print('Error: %d' % response.status_code)


def crawl_zhihu_followers(zhihu_user_id='xulu-0620'):
    """
    crawl all followers belong to the particular Zhihu user
    :param zhihu_user_id:
    :return:
    """
    page_no = 1
    totals = 20  # just for temp use

    url = 'https://www.zhihu.com/api/v4/members/%s/followers' % zhihu_user_id
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer Mi4xaTZ0UkFBQUFBQUFBVU1KWlMtYjlDeGNBQUFCaEFsVk5zMUFOV2dBVHk5U2h1S1FVN1R6OUFweVYwV21HWm5Fa1dn|1508230067|a16ee938a86d2a004193803aa5390bb287bfd3e5',
        'Host': 'www.zhihu.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Referer': 'https://www.zhihu.com',
        'x-udid': 'AFDCWUvm_QuPTrodoMiYXMbKPb92g2-ihUs=',
    }

    while page_no * 20 <= totals:
        payload = {
            'include': 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics',
            'offset': str(page_no * 20),
            'limit': '20'
        }

        cookies = dict(
            cookies_are='')

        response = requests.get(url, headers=headers, cookies=cookies, params=payload)
        print('crawling url : ' + response.url)
        if response.status_code == 200:
            json_obj = response.json()
            totals = json_obj['paging']['totals']
            for _ in json_obj['data']:
                _['host'] = zhihu_user_id
                insert_item(_)
                print('insert one item successfully~')
            page_no += 1
        else:
            print('Error ! error code is %d' % response.status_code)


def insert_item(item):
    """
    insert an item into MongoDB
    :param item:
    :return:
    :Version:1.0
    """
    client = MongoClient()
    db = client.zhihu.users

    result = db.insert_one(item)


def query_and_crawl_zhihuer_from_mongo():
    """
    query zhihu users from mongodb and crawl the detailed info of them
    :return:
    :Version:1.0
    """
    client = MongoClient()
    db = client.zhihu.live
    lives = db.find()
    visited_zhihu_user = []
    for live in lives:
        zhihu_user = live['speaker']['member']['url_token']
        if zhihu_user not in visited_zhihu_user:
            print('start crawling %s' % zhihu_user)
            try:
                crawl_zhihu_user_by_api(zhihu_user)
                time.sleep(random.randint(2, 5))  # a range between 2s and 5s
            except:
                pass
            visited_zhihu_user.append(zhihu_user)


if __name__ == '__main__':
    query_and_crawl_zhihuer_from_mongo()
