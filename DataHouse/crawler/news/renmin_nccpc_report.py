"""
a text mining script for The 19th National Congress of CPC Report
"""

import requests
from bs4 import BeautifulSoup
import jieba
import jieba.analyse

STOPWORDS = './stopwords_renmin_nccpc_report.txt'
USERDICT = './userdict_renmin_nccpc_report.txt'

jieba.load_userdict(USERDICT)
jieba.analyse.set_stop_words(STOPWORDS)


class Report(object):
    def __init__(self, timestamp, speaker, content):
        self.timestamp = timestamp
        self.speaker = speaker
        self.content = content

    def __str__(self):
        return '{timestamp = ' + self.timestamp + '; speaker = ' + self.speaker + '; content = ' + self.content + '}';

    def __repr__(self):
        return self.__str__()


def crawl_report():
    """
    crawl report from http://live01.people.com.cn/zhibo/Myapp/Html/Member/html/201710/9_1887_59e5a87edb17f_quan.html
    :return:
    """
    url = 'http://live01.people.com.cn/zhibo/Myapp/Html/Member/html/201710/9_1887_59e5a87edb17f_quan.html'
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=30)

    report_list = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text.encode('latin').decode('utf-8'), 'html5lib')
        for _ in soup.find_all('div', class_='zhibo_box clearfix')[0].dl.contents:
            if _.name in ['dd', 'dt']:
                timestamp = _.h3.text.strip()
                speaker = _.h4.text.strip()
                content = _.p.text.strip()

                report = Report(timestamp, speaker, content)
                report_list.append(report)

    return report_list


def analysis(list_):
    content_list = [_.content for _ in list_]

    hot_words = jieba.analyse.extract_tags(''.join(content_list), topK=100, withWeight=True, allowPOS=())

    for _ in hot_words:
        print(_[0] + '\t' + str(_[1]))


if __name__ == '__main__':
    report_list = crawl_report()
    analysis(report_list)
