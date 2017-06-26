"""
a spider for ifeng news
"""
import os

import requests
from bs4 import BeautifulSoup

import re


def crawl(keyword):
    page = 1
    index = 1

    while page <= 565:
        url = 'http://search.ifeng.com/sofeng/search.action?q=' + keyword + '&c=1&chel=&p=' + str(page)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Host': 'search.ifeng.com',
            'Referer': 'http://search.ifeng.com/sofeng/search.action?q=%E5%86%9C%E5%A4%AB%E5%B1%B1%E6%B3%89&c=1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }

        cookies = dict(
            cookies_are='vjuids=d7918423.1524ac04f39.0.cd4c4319; userid=1452953066397_xk9qy88570; vjlast=1452953063.1452953063.30; prov=cn027; city=027; weather_city=hb_wh; region_ip=119.96.76.x; region_ver=1.2')

        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for each_div in soup.find_all('div', class_='searchResults'):
                href = each_div.a['href'].strip()
                title = each_div.a.text.strip()
                datetime_and_media = each_div.find_all(color="#1a7b2e")[0].text.strip().replace('\r', '')
                article = each_div.find_all('p')[1].text
                # article = get_article(href)
                print(datetime_and_media + '   ' + href + '    ' + title + '    ' + article)

                content = '' + datetime_and_media + '\r\n文章链接：' + href + '\r\n文章标题：' + title + '\r\n文章摘要：' + article

                write_txt(content, '/tmp/%s/' % keyword, str(index))
                index += 1
                print('-----------------------')
        page += 1


def get_article(article_url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Cache-Control': 'max-age=0',
        'Host': 'finance.ifeng.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    resp = requests.get(article_url, headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content.decode('utf-8'), 'html.parser')
        if article_url.startswith('http://news.ifeng.com') or article_url.startswith('http://finance.ifeng.com'):
            try:
                main_content = soup.find_all(id='main_content')[0]
                article = main_content.text
                matchObj = re.match(r'^\w\t\d[4]-\d[2]-\d[2]')
                print(len(matchObj) + ' ======== ')
                return article
            except:
                return ''

        else:
            return ''


def write_txt(content, filedir, filename):
    if not os.path.exists(filedir) or not os.path.isdir(filedir):
        os.mkdir(filedir)

    with open(filedir + filename + '.txt', mode='w', encoding='utf-8') as f:
        f.write(content)
        f.flush()
        print(filedir + filename + ' writes out successfully!')


if __name__ == '__main__':
    crawl('蒙牛')
