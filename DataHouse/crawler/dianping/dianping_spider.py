"""
a web spider for daz hong dian ping
"""
import time

import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
from pymongo import MongoClient

CITY_FILEPATH = 'city.xml'
CATEGORY_FILEPATH = 'type.xml'
SLEEP_TIME = 2


class City(object):
    def __init__(self, pinyin, id, name):
        self.pinyin = pinyin
        self.id = id
        self.name = name

    def __str__(self):
        return '{pinyin = ' + self.pinyin + '; id = ' + self.id + '; name = ' + self.name + '}';

    def __repr__(self):
        return self.__str__()


class Category(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return '{id = ' + self.id + '; name = ' + self.name + '}';

    def __repr__(self):
        return self.__str__()


def parse_city_xml(city_xml_filepath):
    """
    parse the city_xml_filepath file in res directory, and return job list
    :param city_xml_filepath:
    :return:
    """
    citylist = []
    tree = etree.parse(city_xml_filepath)
    for _ in tree.xpath('//city'):
        city = City(_.get('pinyin').strip(), _.get('id').strip(), _.text.strip())
        citylist.append(city)

    return citylist


def parse_category_xml(type_xml_filepath):
    """
    parse the type_xml_filepath file in res directory, and return job list
    :param type_xml_filepath:
    :return:
    """
    categorylist = []
    tree = etree.parse(type_xml_filepath)
    for _ in tree.xpath('//type'):
        category = Category(_.get('id').strip(), _.text.strip())
        categorylist.append(category)

    return categorylist


def crawl(start_num, city, category):
    headers = {
        'Host': 'mapi.dianping.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    payload = {
        'start': start_num,
        'categoryid': category.id,
        'sortid': 0,
        'maptype': 0,
        'cityid': city.id
    }

    main_url = 'http://mapi.dianping.com/searchshop.json'

    response = requests.get(main_url, params=payload, timeout=20, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error!')
        return None


def insert_item(item):
    """
    insert an object into mongodb
    :param item:
    :return:
    """
    client = MongoClient()
    db = client.dianping.hotel
    result = db.insert_one(item)


if __name__ == '__main__':
    categorylist = parse_category_xml(CATEGORY_FILEPATH)
    citylist = parse_city_xml(CITY_FILEPATH)

    for city in citylist:
        for category in categorylist:
            # data = []
            max_num = 25  # can be assigned to any number
            start_num = 0
            while start_num < max_num:
                try:
                    dat = crawl(start_num, city, category)
                    if dat is not None:
                        max_num = dat['recordCount']
                    start_num += 25
                    print(dat['list'])
                    for _ in dat['list']:
                        _['cityName'] = city.name
                        _['categoryName'] = category.name
                        insert_item(_)
                    # data.append(dat['list'])
                    time.sleep(SLEEP_TIME)
                    # df = pd.DataFrame(data, )
                    # df = pd.DataFrame(data)
                    # df.to_excel('./food.xlsx', 'Food', index=False)
                except:
                    pass
