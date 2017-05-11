"""
    A web crawler for anjuke
"""
import requests

from DataHouse.crawler.file_helper import write_excel


class AnjukeHouse(object):
    pass


def get_community_info():
    urls = ['https://m.anjuke.com/wh/community/?from=trendency_rec_more&p=%d' % i for i in
            range(1, 117, 1)]
    headers = {
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) '
                      'Version/8.0 Mobile/12A4345d Safari/600.1.4'
    }
    anjuke_house_list = []
    for url in urls:
        response = requests.get(url, headers=headers)
        response_json = response.json()
        if response_json['code'] == 0 and response_json['msg'] == 'ok' and len(response_json['data']) > 0:
            for row in response_json['data']:
                anjuke_house = AnjukeHouse()
                anjuke_house.address = row['address']
                anjuke_house.area = row['area']
                anjuke_house.block = row['block']
                anjuke_house.buildYear = row['build_year'].replace('年', '').strip()
                anjuke_house.image = row['image']
                anjuke_house.midPrice = row['mid_price']
                anjuke_house.name = row['name']
                anjuke_house.saleNum = row['sale_num']
                anjuke_house.url = row['url']
                anjuke_house_list.append(anjuke_house)

        print('Page %s has been crawled successfully~' % url.split('=')[-1])

    return anjuke_house_list


if __name__ == '__main__':
    anjuke_house_list = get_community_info()
    write_excel(anjuke_house_list, 'anjuke')
