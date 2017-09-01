"""
a web crawler for hospital information
"""
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


def insert_item(item):
    """
    insert an object into mongodb
    :param item:
    :return:
    """
    client = MongoClient()
    db = client.living.hospital
    result = db.insert_one(item)


def crawl(province_id, province_name):
    url = 'https://www.hqms.org.cn/usp/roster/rosterInfo.jsp?provinceId=%s&htype=&hgrade=&hclass=&hname=' \
          '&_=1504241036511' % str(province_id)
    response = requests.get(url, timeout=20)
    if response.status_code == 200:
        json = response.json()
        for _ in json:
            _['province'] = province_name
            insert_item(_)
        print('Insert %s done~' % province_name)
    else:
        print('Error!')


def get_province_id():
    province = {}
    response = requests.get('https://www.hqms.org.cn/usp/roster/index.jsp', timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')
        options = soup.find_all('select', class_='province_select')[0].find_all('option')
        for i in range(1, len(options), 1):
            province_id = options[i]['value'].strip()
            province_name = options[i].text.strip()
            province[province_name] = province_id
    else:
        print('Error!')

    return province


if __name__ == '__main__':
    province = get_province_id()
    for k, v in province.items():
        try:
            crawl(v, k)
        except:
            pass
