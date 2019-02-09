import os

import requests
from bs4 import BeautifulSoup

DOWNLOAD_DIR = 'E:/Papers/ICCV2017/'


def download_paper():
    if not os.path.isdir(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    print('start downloading all ICCV2017 papers, wait for a moment please......')
    iccv_paperlist_url = "http://openaccess.thecvf.com/ICCV2017.py"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'openaccess.thecvf.com',
        'Referer': 'http://weibo.com/fly51fly?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }
    response = requests.get(iccv_paperlist_url, headers=headers, timeout=20)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')

        for _ in soup.find_all('a'):
            if _.get_text().strip() == 'pdf':
                paper_pdf_url = "http://openaccess.thecvf.com/" + _['href']
                print('downloading %s ~~~' % paper_pdf_url)
                resp = requests.get(paper_pdf_url, timeout=30)
                if resp.status_code not in [403, 404]:
                    with open(os.path.join(DOWNLOAD_DIR, _['href'].split('/')[-1].strip()), mode='wb') as f:
                        f.write(resp.content)
                        f.flush()
                        f.close()
    else:
        print('ERROR!')


if __name__ == '__main__':
    download_paper()
