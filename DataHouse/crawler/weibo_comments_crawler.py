"""
A web crawler for sina weibo comments of a particular weibo
"""
import datetime
import os
import time

import requests
from bs4 import BeautifulSoup

WEIBO_DATA_FILEPATH = '/tmp/wjk/'


class WeiboComment:
    def __init__(self, username, user_href, content, like, date, device):
        self.username = username
        self.user_href = user_href
        self.content = content
        self.like = like
        self.date = date
        self.device = device

    def __str__(self):
        return '{username = ' + self.username + '; user_href = ' + self.user_href + '; content = ' + self.content + '; like = ' + self.like + '; date = ' + self.date + '; device = ' + self.device + '}';

    def __repr__(self):
        return self.__str__()


def get_weibo_comments(weibo_url):
    pagenum = 1
    counter = 1

    while pagenum < 39018:
        # request_url = 'http://weibo.cn/comment/E3bri9IO7?uid=2609400635&rl=0&page=%s' % str(pagenum)
        request_url = weibo_url + '?page=%s' % str(pagenum)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Host': 'weibo.cn',
            'Referer': 'https://weibo.cn/comment/E3bri9IO7',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
        }

        with open('../config/weibo_cookies.txt', mode='rt', encoding='UTF-8') as f:
            cookies_string = ''.join(f.readlines()).strip()
        cookies = dict(cookies_are=cookies_string)
        response = requests.get(request_url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            html_raw = response.text
            soup = BeautifulSoup(html_raw, 'html5lib')

            div_soups = soup.find_all('div', class_='c')

            for i in range(2, len(div_soups) - 1, 1):
                try:
                    username = div_soups[i].a.get_text()
                    user_href = div_soups[i].a['href']
                    div_spans = div_soups[i].find_all('span')

                    content = div_spans[0].get_text()
                    like = div_spans[1].get_text().replace('赞[', '').replace(']', '').strip()
                    date_and_device = div_spans[3].get_text()

                    date_raw = date_and_device.split('来自')[0].strip()

                    date = datetime_handle(date_raw)
                    device = date_and_device.split('来自')[1].strip()

                    weiboComment = WeiboComment(username, user_href, content, like, date, device)
                    content = weiboComment.username + '\r\n' + weiboComment.user_href + '\r\n' + weiboComment.content + '\r\n' + weiboComment.like + '\r\n' + weiboComment.date + '\r\n' + weiboComment.device
                    out_txt(content, WEIBO_DATA_FILEPATH, str(counter))
                    counter += 1

                except:
                    pass

                    # time.sleep(2)
        elif response.status_code == 403:
            print('Access denied! Current page is ' + str(pagenum))
        pagenum += 1


def datetime_handle(date_time):
    if date_time.endswith('分钟前'):
        sub_min = date_time.replace('分钟前', '').strip()
        date = datetime.datetime.now() - datetime.timedelta(minutes=int(sub_min))
        return str(date.month) + '月' + str(date.day) + '日 ' + str(date.hour) + ':' + str(date.minute)
    elif '今天' in date_time:
        today = datetime.datetime.today()
        date = date_time.replace('今天', str(today.month) + '月' + str(today.day) + '日')
        return date
    else:
        return date_time


def out_txt(content, dir, filename):
    if not os.path.exists(dir) or not os.path.isdir(dir):
        os.mkdir(dir)

    filepath = dir + filename + '.txt'
    print(filepath)
    with open(filepath, mode='wt') as f:
        f.write(content)
        f.flush()
        f.close()
        print('file ' + filename + ' has been written successfully!')


if __name__ == '__main__':
    get_weibo_comments('http://weibo.cn/comment/E3bri9IO7')
