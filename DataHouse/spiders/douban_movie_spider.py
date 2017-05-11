import os
import urllib.parse
import datetime

import pandas as pd
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

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
                    my_dict[td.a.get_text().strip()] = int(td.b.get_text().replace('(', '').replace(')', ''))
            else:
                raise ValueError('Fail to get tags...' + str(response.status_code))

            return my_dict

        # tags_and_num = get_tags_and_num()
        tags_and_num = {'科幻': 6181851}
        print(tags_and_num)
        for tag, num in tags_and_num.items():
            urls = ['https://movie.douban.com/tag/' + urllib.parse.quote(tag) + '?start=%d&type=T' % i for i in
                    range(0, num, 20)]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for each_movie in response.xpath('//div[@class="article"]/div[2]/table'):
            url = each_movie.xpath('tr/td[1]/a/@href').extract_first()
            title = each_movie.xpath('tr/td[1]/a/@title').extract_first()
            image = each_movie.xpath('tr/td[1]/a/img/@src').extract_first()
            category = urllib.parse.unquote(response.url.split('?')[0].split('/')[-1])
            date = \
                each_movie.xpath('tr/td[2]/div[@class="pl2"]/p[@class="pl"]/text()').extract_first().strip().split('/')[
                    0].split('(')[0]
            score = each_movie.xpath(
                'tr/td[2]/div[@class="pl2"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()').extract_first()
            scorerNum = each_movie.xpath(
                'tr/td[2]/div[@class="pl2"]/div[@class="star clearfix"]/span[@class="pl"]/text()').extract_first().replace(
                '人评价)', '').replace('(', '')

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
