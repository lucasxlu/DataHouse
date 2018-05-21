"""
a web crawler for www.todayonhistory.com
"""
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def crawl(month, day):
    """
    crawl events happened on today
    :param month:
    :param day:
    :return:
    """
    today_events = []

    url = 'http://www.todayonhistory.com/index.php?m=content&c=index&a=json_event&page=1&pagesize=40&month={0}&day={1}'.format(
        month, day)
    page = 1
    flag = True
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Host': 'www.todayonhistory.com',
        'Referer': 'http://www.todayonhistory.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and flag:
        js = response.json()
        if str(js) != '0':
            for itm in js:
                resp = requests.get(itm['url'], headers={
                    'Referer': itm['url'],
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
                })
                resp.encoding = 'utf-8'
                if resp.status_code not in [404, 403]:
                    soup = BeautifulSoup(resp.text, 'html5lib')
                    article = ''.join([p.text for p in soup.find('div', class_="body").find_all('p')]).strip()

                    event = [itm['id'], itm['solaryear'], month, day, itm['title'], itm['description'], article,
                             itm['thumb'], itm['url']]
                    print(event)
                    today_events.append(event)

            page += 1
        else:
            flag = False

    return today_events


if __name__ == '__main__':
    events = []

    months = [i for i in range(1, 13, 1)]

    for month in months:
        if month in [1, 3, 5, 7, 8, 10, 12]:
            for day in range(1, 32, 1):
                print('start crawling {0}-{1}...'.format(month, day))
                events += crawl(month, day)

                col = [
                    'ID',
                    'Year',
                    'Month',
                    'Day',
                    'Title',
                    'Description',
                    'Article',
                    'Thumb',
                    'URL']
                df = pd.DataFrame(events, columns=col)
                df.to_excel('./today_events.xlsx', 'Events', index=False)

                time.sleep(2)
        elif month in [4, 6, 9, 11]:
            for day in range(1, 31, 1):
                print('start crawling {0}-{1}...'.format(month, day))
                events += crawl(month, day)

                col = [
                    'ID',
                    'Year',
                    'Month',
                    'Day',
                    'Title',
                    'Description',
                    'Article',
                    'Thumb',
                    'URL']
                df = pd.DataFrame(events, columns=col)
                df.to_excel('./today_events.xlsx', 'Events', index=False)

                time.sleep(2)
        else:
            for day in range(1, 29, 1):
                print('start crawling {0}-{1}...'.format(month, day))
                events += crawl(month, day)

                col = [
                    'ID',
                    'Year',
                    'Month',
                    'Day',
                    'Title',
                    'Description',
                    'Article',
                    'Thumb',
                    'URL']
                df = pd.DataFrame(events, columns=col)
                df.to_excel('./today_events.xlsx', 'Events', index=False)

                time.sleep(2)

    print('All has been processed done!!')
