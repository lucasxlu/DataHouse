import time
import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

commments = []


def crawl_comments(type='book', item_id='26708119', pn=2):
    url = 'https://' + type + '.douban.com/subject/' + str(item_id) + '/comments/hot?p=' + str(pn)
    print('crawling page %s ' % url)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Host': '%s.douban.com' % type,
        'Referer': 'https://' + type + '.douban.com/subject/' + str(item_id) + '/comments/hot?p=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')
        for li in soup.find('div', id="comments").find_all('li'):
            cid = li['data-cid']
            comm = li.find('p', class_="comment-content").get_text()

            tmp = li.find('span', class_="comment-info").find_all('span')[0]
            rate = int(tmp['class'][1].replace('allstar', '')) / 10 if tmp.has_attr('class') else ''
            cdate = li.find('span', class_="comment-info").find_all('span')[-1].get_text()
            commments.append([cid, comm, rate, cdate])
    else:
        print(response.status_code)


if __name__ == '__main__':
    for i in range(2, 894):
        crawl_comments(pn=i, item_id='2062200')
        time.sleep(np.random.randint(2, 5))

    col = ['ID', 'Comment', 'Rate', 'Date']
    df = pd.DataFrame(commments, columns=col)
    df.to_excel(excel_writer='./悲伤逆流成河.xlsx', sheet_name='DoubanBook', index=False)
