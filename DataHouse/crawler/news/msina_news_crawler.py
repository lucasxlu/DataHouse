"""
a spider for sina news of mobile H5 version
"""
import json
import os
import time
import urllib.parse

import chardet
import requests
from bs4 import BeautifulSoup


class MSina:
    def __init__(self, date, source, title, article):
        self.date = date
        self.source = source
        self.title = title
        self.article = article

    def __str__(self):
        return '{date = ' + self.date + '; source = ' + self.source + '; title = ' + self.title + '; article = ' + self.article + '}';

    def __repr__(self):
        return self.__str__()


def crawl(keyword):
    pagenum = 1

    while pagenum <= 1035:
        request_url = 'http://site.proc.sina.cn/search/search_list.php?search_kind=news&search_keyword=' + urllib.parse.quote(
            keyword) + '&page=' + str(
            pagenum) + '&range=title&channel=&zt_name=&sort=time&jsoncallback=loadSuccess&callback=jsonp1'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
            'Referer': 'http://site.proc.sina.cn/search/query.php?kind=%E6%90%9C%E6%A0%87%E9%A2%98&key=%E8%82%AF%E5%BE%B7%E5%9F%BA&vt=4',
            'Host': 'site.proc.sina.cn',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
        }

        response = requests.get(request_url, headers=headers)
        if response.status_code == 200:
            json_obj = json.loads(
                response.text.replace('loadSuccess(', '').replace(')', '').replace("'", '"').replace('undefined',
                                                                                                     'null'))
            if json_obj['code'] == 0:
                for i in range(1, 11):

                    try:
                        json_item = json_obj['item'][str(i)]
                        date = json_item['date']
                        url = json_item['url']
                        title = BeautifulSoup(json_item['title'], 'html.parser').text
                        source = json_item['source']
                        article = get_article(url)

                        print("Article is " + article)
                        msina = MSina(date, source, title=title, article=article)

                        write_txt(msina, '/tmp/%s/' % keyword, title, char_encoding='UTF-8')
                    except:
                        pass

        time.sleep(2)
        pagenum += 1


def get_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }
    resp = requests.get(url, headers=headers)
    print('This article\'s URL is ' + url)
    # resp.encoding = 'utf-8'
    article_text = ''
    if resp.status_code == 200:
        page_encoding = chardet.detect(resp.content)['encoding']
        soup = BeautifulSoup(resp.content.decode(page_encoding), 'html.parser')
        article_soups = soup.find_all(class_='art_t')

        if len(article_soups) > 0:
            for each_p in article_soups:
                article_text += each_p.text.strip()
            return str(article_text)

        article_soups = soup.find_all('p')
        if len(article_soups) > 0:
            for each_p in article_soups:
                article_text += each_p.text.strip()
            return str(article_text)

    elif resp.status_code == 403:
        print('Your requests are denied!')
    else:
        print('ERROR!!!' + str(resp.status_code))


def write_txt(msina, filedir, filename, char_encoding):
    if not os.path.isdir(filedir):
        os.mkdir(filedir)

    filepath = filedir + filename + '.txt'
    txt_content = "时间：" + msina.date + "\r\n来源：" + msina.source + "\r\n题目：" + msina.title + "\r\n正文：\r\n" + msina.article

    if msina.article.strip() is not "" and msina.article.strip() is not None:
        try:
            f = open(filepath, mode='w', encoding=char_encoding)
            f.write(txt_content)
            f.flush()
            f.close()
        except:
            pass
        finally:
            print('File ' + filepath + ' writes successfully!')


if __name__ == '__main__':
    crawl('农夫山泉')
