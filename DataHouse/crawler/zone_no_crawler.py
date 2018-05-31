"""
not finish yet
"""

import requests
from bs4 import BeautifulSoup


def crawl():
    url = 'http://quhao.tianqi.com/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'quhao.tianqi.com',
        'Referer': 'https://www.baidu.com/link?url=dt9Ft7DGXOxzDe8CX8pIybsRFMUsEzSbE3udUXkowquCMcMgXumd-ruQM4nr4uBD&wd=&eqid=a75b74b50001af66000000035b082294',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')
        for li in soup.find('div', class_="box").find_all('li'):
            print(li.text)


def crawl_detail(place):
    url = 'http://quhao.tianqi.com/%s' % place
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'quhao.tianqi.com',
        'Referer': 'http://quhao.tianqi.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')


if __name__ == '__main__':
    crawl()
