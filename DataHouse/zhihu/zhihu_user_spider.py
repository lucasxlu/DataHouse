"""
a web spider for Zhihu user's information
"""
import json

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
        zhihu_user['educations'] = person_obj['educations']  # 教育经历
        zhihu_user['employments'] = person_obj['employments']  # 工作经历
        zhihu_user['locations'] = person_obj['locations']  # 地址
        zhihu_user['userType'] = person_obj['userType']  # 用户类型
        zhihu_user['followingCount'] = person_obj['followingCount']  # 关注人数
        zhihu_user['followingTopicCount'] = person_obj['followingTopicCount']  # 关注话题数量
        zhihu_user['business'] = person_obj['business']  # 行业
        zhihu_user['hostedLiveCount'] = person_obj['hostedLiveCount']  # 举办Live数量
        zhihu_user['followerCount'] = person_obj['followerCount']  # 粉丝数量
        zhihu_user['favoritedCount'] = person_obj['favoritedCount']  # 答案被收藏数量
        zhihu_user['voteupCount'] = person_obj['voteupCount']  # 答案被点赞数量
        zhihu_user['answerCount'] = person_obj['answerCount']  # 回答数量
        zhihu_user['questionCount'] = person_obj['questionCount']  # 提问数量
        zhihu_user['thankedCount'] = person_obj['thankedCount']  # 感谢数量
        zhihu_user['articlesCount'] = person_obj['articlesCount']  # 发表文章数量
        zhihu_user['columnsCount'] = person_obj['columnsCount']  # 专栏数量
        zhihu_user['favoriteCount'] = person_obj['favoriteCount']  # 收藏数量
        zhihu_user['markedAnswersCount'] = person_obj['markedAnswersCount']  # 编辑收录答案数量
        zhihu_user['gender'] = person_obj['gender']  # 性别
        zhihu_user['badge'] = person_obj['badge']  # 话题优秀回答者
        zhihu_user['name'] = person_obj['name']  # 话题优秀回答者

        print(zhihu_user)
        insert_item(zhihu_user)

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
    db = client.zhihu.user

    result = db.insert_one(item)


if __name__ == '__main__':
    crawl_zhihu_user()
