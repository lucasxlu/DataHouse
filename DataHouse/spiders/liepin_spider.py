import datetime
import os
import urllib.parse

import pandas as pd
import scrapy
from bs4 import BeautifulSoup

from DataHouse.items import LiePin

liepin_job_list = []
LIEPIN_JOB_DATA_DIR = '../DataSet/liepin/'
JOB_LIST = ['python', '']


class LiePinSpider(scrapy.Spider):
    name = "liepin"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Host': 'www.liepin.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/'
                      '58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36'
    }

    def start_requests(self):
        if os.path.exists(LIEPIN_JOB_DATA_DIR):
            os.removedirs(LIEPIN_JOB_DATA_DIR)
        os.makedirs(LIEPIN_JOB_DATA_DIR)
        urls = ['https://www.liepin.com/zhaopin/?fromSearchBtn=2&degradeFlag=0&init=-1&key=python&curPage=%s' % str(i)
                for i in range(10)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html5lib')
        joblist_ul = soup.find_all(class_='sojob-list')[0]
        for li in joblist_ul.find_all('li'):
            isVerified = True if li.i.b is not None else False
            title = li.div.div.h3.a.get_text().strip()
            jobid = li.div.div.h3.a['href'].strip().split('/')[-1].replace('.shtml', '')
            salary = li.div.div.p['title'].split('_')[0].strip()
            location = li.div.div.p['title'].split('_')[1].strip()
            education = li.div.div.p['title'].split('_')[2].strip()
            experience = li.div.div.p['title'].split('_')[2].strip()

            publishTime = li.find(class_="time-info clearfix").time.get_text().strip()
            feedback = li.find(class_="time-info clearfix").span.get_text().strip()

            company = li.find(class_="company-info nohover").find_all('p')[0].a.get_text().strip()
            industryField = li.find(class_="company-info nohover").find_all('p')[1].span.a.get_text().strip()
            tags = [_.get_text().strip() for _ in
                    li.find(class_="company-info nohover").find_all('p')[2].find_all('span')]

            liepin = LiePin(jobid=jobid, title=title, salary=salary, location=location, education=education,
                            experience=experience, company=company, industryField=industryField, tags=tags,
                            publishTime=publishTime, feedback=feedback, isVerified=isVerified)

            def parse_detail_page(job_id):
                """
                get job detailed description
                :param job_id:
                :return:
                """
                desciption = ''
                import requests
                response = requests.get('https://www.liepin.com/job/%s.shtml' % str(job_id), headers=self.headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html5lib')
                    for _ in soup.find_all(class_="job-item main-message"):
                        desciption += _.get_text().strip()
                else:
                    print('ERROR!!!')
                return desciption

            print(parse_detail_page(jobid))

    def close(spider, reason):
        df = pd.DataFrame(liepin_job_list)
        # df.to_excel('./DataSet/liepin.xlsx', sheet_name='JobInfo')
