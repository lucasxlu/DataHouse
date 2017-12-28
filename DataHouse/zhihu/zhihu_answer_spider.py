import logging
import configparser

import smtplib
import email.mime.multipart
import email.mime.text

import requests
from pymongo import MongoClient

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='zhihu_answer.log',
                    filemode='w')


def crawl_answers(question_id, offset):
    """
    crawl zhihu answers in one page
    :param question_id:
    :param offset:
    :return:
    """
    question_url = 'https://www.zhihu.com/api/v4/questions/%s/answers' % str(question_id)
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/question/%s' % str(question_id),
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.'
                      '84 Chrome/63.0.3239.84 Safari/537.36',
        'X-UDID': 'AJCCPZ1u7wqPTlgJlMSqVqpruvn5gL4Ftsw=',
        'Connection': 'keep-alive'
    }
    payload = {
        'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,'
                   'collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,'
                   'voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,'
                   'question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,'
                   'upvoted_followees;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics',
        'offset': offset,
        'limit': 20,
        'sort_by': 'default'
    }
    cookies = dict(
        cookies_are='')

    response = requests.get(url=question_url, headers=headers, cookies=cookies, params=payload)

    if response.status_code == 200:
        resp_json = response.json()

        return resp_json
    else:
        logging.error(response.status_code)

        return None


def recursive_crawl_answers(question_id):
    """
    recursively crawl all Zhihu answers data
    :param question_id:
    :return:
    """
    offset = 0
    while True:
        try:
            obj = crawl_answers(question_id, offset)
            if obj['paging']['is_end'] == 'false':
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
    db = client.zhihu.answer

    result = db.insert_one(item)


def send_email(content, subject="Zhihu Answers", from_="m13207145966@qq.com", to_=""):
    """
    send email
    :param content:
    :param subject:
    :param from_:
    :param to_:
    :return:
    """
    config = configparser.ConfigParser()
    config.read('./163mail.ini')
    msg = email.mime.multipart.MIMEMultipart()
    msg['from'] = from_
    msg['to'] = to_
    msg['subject'] = subject
    txt = email.mime.text.MIMEText(content)
    msg.attach(txt)

    smtp = smtplib.SMTP()
    smtp.connect(config['163Mail']['host'], config['163Mail']['port'])
    smtp.login(config['163Mail']['username'], config['163Mail']['password'])
    smtp.sendmail(from_, to_, str(msg))
    smtp.quit()

    logging.info('send email successfully~')


if __name__ == '__main__':
    recursive_crawl_answers(60293871)
