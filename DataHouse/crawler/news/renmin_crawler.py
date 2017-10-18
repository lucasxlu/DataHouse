"""
a spider for renmin news
"""
import os
import time

import requests


def crawl(keyword):
    url = 'http://search.people.com.cn/rmw/GB/rmwsearch/gj_searchht.jsp'
    curpage = 1

    while curpage <= 320:
        payload = {
            'basenames': 'rmwsite',
            'where': '(CONTENT = (' + keyword + ') or TITLE = (' + keyword + ') or AUTHOR = (' + keyword + '))',  # 检索全文
            # 'where': 'TITLE = (肯德基)', #仅检索标题
            'curpage': curpage,
            'pagecount': 20,
            'classvalue': 'ALL',
            'classfield': 'CLASS2',
            'isclass': 1,
            'keyword': keyword,
            'sortfield': 'LIFO',
            'id': 0.7601115698867418,
            '_': ''
        }

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Content-type': 'application/x-www-form-urlencoded',
            'Host': 'search.people.com.cn',
            'Origin': 'http://search.people.com.cn',
            'Referer': 'http://search.people.com.cn/rmw/GB/rmwsearch/gj_search_pd.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
            'X-Prototype-Version': '1.4.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

        cookies = dict(
            cookies_are='')

        response = requests.post(url, data=payload, headers=headers, cookies=cookies, stream=True, timeout=20)
        if response.status_code == 200:
            xml_raw = response.content
            if not os.path.exists('/tmp/' + keyword) or not os.path.isdir('/tmp/' + keyword):
                os.mkdir('/tmp/' + keyword)
            with open('/tmp/' + keyword + os.path.sep + str(curpage) + '.xml', mode='w') as f:
                f.write(xml_raw.decode('utf-8'))
                f.flush()
                curpage += 1
                print('processing page %d done!!' % curpage)
        time.sleep(10)


if __name__ == '__main__':
    crawl('农夫山泉')
