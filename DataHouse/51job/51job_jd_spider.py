import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


def crawl_jd(job_id):
    url = 'http://m.51job.com/search/jobdetail.php?jobid=%s' % str(job_id).strip()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'm.51job.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }

    jd = {}

    response = requests.get(url, headers=headers)
    response.encoding = 'UTF-8'
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')
        article = soup.find('article')
        article_content = article.get_text().strip().replace('\n', '')

        job_tags = [span.get_text().strip() for span in soup.find_all('div', class_='xqq')[0].find_all('span')]
        benefits = [span.get_text().strip() for span in soup.find_all('div', class_='xqq')[1].find_all('span')]

        company_label = {}
        for label in soup.find_all('div', class_='xqd')[0].find_all('label'):
            company_label[label.span.get_text()] = str(list(label.children)[1]).strip()

        jobname = soup.find('p', class_='xtit').get_text().strip()
        company_node = soup.find('a', class_='xqa')

        company_name = company_node.text.strip()
        company_url = company_node['href']

        jd['article_content'] = article_content
        jd['job_tags'] = job_tags
        jd['benefits'] = benefits
        jd['jobname'] = jobname
        jd['company_name'] = company_name
        jd['company_url'] = company_url

    elif response.status_code == 403:
        print('forbidden')
    else:
        print('Error, ' + str(response.status_code))

    return jd


def insert_jd(item):
    """
    insert an item into MongoDB
    :param item:
    :return:
    :Version:1.0
    """
    client = MongoClient()
    db = client.wyjob.jd

    result = db.insert_one(item)


if __name__ == '__main__':
    try:
        jd = crawl_jd('94557976')
        if jd is not None:
            insert_jd(jd)
    except:
        pass
