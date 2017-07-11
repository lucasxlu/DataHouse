"""
Douban Movie Web Spider powered by parsing HTML
"""
import datetime
import os
import urllib.parse

import pandas as pd
import scrapy
from pymongo import MongoClient

from DataHouse.items import DoubanMovie

douban_movie_list = []
client = MongoClient()

start_time = datetime.datetime


class DoubanMovieSpider(scrapy.Spider):
    name = "doubanMovie"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/tag',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
                      'Version/9.0 Mobile/13B143 Safari/601.1 '
    }

    def start_requests(self):
        def get_tags_and_num():
            my_dict = {}
            import requests
            from bs4 import BeautifulSoup
            import time
            headers = {
                'Host': 'movie.douban.com',
                'Referer': 'https://movie.douban.com/',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
            response = requests.get('https://movie.douban.com/tag/', headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html5lib')
                for td in soup.find_all('div', class_='article')[0].find_all('td'):
                    my_dict[td.a.get_text().strip()] = get_max_pagenum(td.a.get_text().strip()) * 20
                    time.sleep(3)
            else:
                raise ValueError('Fail to get tags...' + str(response.status_code))

            return my_dict

        tags_and_num = get_tags_and_num()
        # tags_and_num = {'科幻': 6181851}
        print(tags_and_num)
        for tag, num in tags_and_num.items():
            urls = ['https://movie.douban.com/tag/' + urllib.parse.quote(tag) + '?start=%d&type=T' % i for i in
                    range(0, num, 20)]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        import re
        def parse_date(data_string):
            match_result = re.match('\d{4}-*\d{0,2}-\d{0,2}', data_string)
            return match_result.group() if match_result is not None else 0

        def parse_scorerNum(scorer_string):
            match_result = re.match('\d+', scorer_string.replace('(', '').replace(')', ''))
            return match_result.group() if match_result is not None else 0

        for each_movie in response.xpath('//div[@class="article"]/div[2]/table'):
            url = each_movie.xpath('tr/td[1]/a/@href').extract_first()
            title = each_movie.xpath('tr/td[1]/a/@title').extract_first()
            image = each_movie.xpath('tr/td[1]/a/img/@src').extract_first()
            category = urllib.parse.unquote(response.url.split('?')[0].split('/')[-1])
            date = parse_date(
                each_movie.xpath('tr/td[2]/div[@class="pl2"]/p[@class="pl"]/text()').extract_first().strip())
            score_node = each_movie.xpath(
                'tr/td[2]/div[@class="pl2"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')
            score = float(score_node.extract_first().strip()) if score_node is not None else 0
            score_num_node = each_movie.xpath(
                'tr/td[2]/div[@class="pl2"]/div[@class="star clearfix"]/span[@class="pl"]/text()').extract_first()
            scorerNum = int(parse_scorerNum(score_num_node.strip())) if score_num_node is not None else 0

            douban_movie = DoubanMovie(title=title, url=url, image=image, category=category, score=score, date=date,
                                       scorerNum=scorerNum)
            insert_item(dict(douban_movie))

            douban_movie_list.append(douban_movie)

    def close(spider, reason):
        df = pd.DataFrame(douban_movie_list)
        mkdirs_if_not_exists('./DataSet/douban/movie/')
        # df.to_excel('./DataSet/douban/movie/科幻.xlsx', sheet_name='Movies')
        end_time = datetime.datetime

        print('It takes %d seconds in all~~~' % (end_time - start_time))


def mkdirs_if_not_exists(dir_):
    if not os.path.exists(dir_) or not os.path.isdir(dir_):
        os.makedirs(dir_)


def get_max_pagenum(tag):
    import requests
    from bs4 import BeautifulSoup
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/tag/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    response = requests.get('https://movie.douban.com/tag/%s' % tag, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')
        max_pagenum = 1
        try:
            page_div = soup.find_all('div', class_='paginator')[0]
            a_list = page_div.find_all('a')
            max_pagenum = int(a_list[-2].get_text().strip())
        except:
            pass

        print('getting max page num of %s is %d' % (tag, max_pagenum))
        return max_pagenum
    else:
        return 0


def insert_item(item):
    client = MongoClient()
    db = client.douban.movie
    result = db.insert_one(item)


def query_document():
    client = MongoClient()
    db = client.douban.movie
    cursor = db.find()
    for document in cursor:
        print(document)
