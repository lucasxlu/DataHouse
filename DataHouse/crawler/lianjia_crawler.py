"""
    A web crawler for lianjia.com
"""
import time

import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s  \t', level=logging.INFO)


class LianJiaHouse(object):
    pass


def get_xiaoqu_info():
    urls = ['https://m.lianjia.com/wh/xiaoqu/pg%d/' % i for i in
            range(1, 2000, 1)]
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) '
                      'Version/8.0 Mobile/12A4345d Safari/600.1.4'
    }
    lianjia_house_list = []
    for url in urls:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            logging.info(response.url)
            soup = BeautifulSoup(response.text, 'html5lib')
            li_soups = soup.find_all('li', class_='pictext')
            for each_li in li_soups:
                lianjia_house = LianJiaHouse()
                lianjia_house.idNo = each_li.a['href'].split('/')[-1].strip()
                out_div = each_li.a.select('.item_list')[0]
                lianjia_house.name = out_div.find_all('div')[0].get_text()
                lianjia_house.feature = out_div.find_all('div', class_='item_other text_cut')[0].get_text()
                lianjia_house.price = out_div.find_all('em')[0].get_text()
            print('Page %s has been written successfully~' % url[-2])
        elif response.status_code == 304:
            logging.ERROR('304 forbidden!!')
        time.sleep(2)

    return lianjia_house_list


if __name__ == '__main__':
    get_xiaoqu_info()
