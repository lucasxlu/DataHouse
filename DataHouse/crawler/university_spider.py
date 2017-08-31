import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd

from io import StringIO, BytesIO

university_list = []


class University():
    def __init__(self, name='', is_985=False, is_211=False, has_institute=False, location='', orgnization='',
                 education_level='', education_type='', university_type=''):
        self.name = name
        self.is_985 = is_985
        self.is_211 = is_211
        self.has_institute = has_institute
        self.location = location
        self.orgnization = orgnization
        self.education_level = education_level
        self.education_type = education_type
        self.university_type = university_type

    def __str__(self):
        return "{ " + str(self.name) + " ;" + str(self.is_985) + " ;" + str(self.is_211) + " ;" + str(
            self.has_institute) + " ;" + self.location + " ;" + self.orgnization + " ;" + self.education_level + " ;" \
               + self.education_type + " ;" + self.university_type + " }"


def crawl(page_url):
    headers = {
        'Host': 'gaokao.chsi.com.cn',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-0.dhtml',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36'
    }
    response = requests.get(page_url, timeout=20, headers=headers)
    if response.status_code == 200:
        html_raw = response.text
        soup = BeautifulSoup(html_raw, 'html5lib')
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html_raw), parser)
        for tr in soup.find_all(bgcolor="#E1E1E1")[0].find_all('tr', attrs={'bgcolor': '#FFFFFF'}):
            try:
                name = tr.td.a.text.strip()  # 大学名称
                detail_url = 'http://gaokao.chsi.com.cn' + tr.td.a['href']  # 详情信息页面
                is_985 = True if tr.td.find(class_='a211985 span985') is not None else False  # 985
                is_211 = True if tr.td.find(class_='a211985 span211') is not None else False  # 211
                has_institute = True if tr.td.find(class_='a211985 spanyan') is not None else False  # 研究生院
                location = tr.find_all('td')[1].get_text().strip()  # 学校地址
                orgnization = tr.find_all('td')[2].get_text().strip()  # 所属机构
                education_level = tr.find_all('td')[3].get_text().strip()  # 学历层次
                education_type = tr.find_all('td')[4].get_text().strip()  # 办学类型
                university_type = tr.find_all('td')[5].get_text().strip()  # 院校类型

                university = University(name, is_985, is_211, has_institute, location, orgnization, education_level,
                                        education_type, university_type)

                print(university)
                university_list.append([name, is_985, is_211, has_institute, location, orgnization, education_level,
                                        education_type, university_type])
            except:
                pass
    else:
        print('Error!!')


def output(some_list, filepath):
    col = [
        u'院校名称',
        u'985',
        u'211',
        u'研究生院',
        u'所在地',
        u'院校隶属',
        u'学历层次',
        u'办学类型',
        u'院校类型']

    df = pd.DataFrame(some_list, columns=col)
    df.to_excel(filepath, '大学', index=False)


if __name__ == '__main__':
    page_urllist = ['http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-%d.dhtml'
                    % _ for _ in range(0, 2660, 20)]

    # crawl('http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-0.dhtml')
    for page_url in page_urllist:
        crawl(page_url)
        output(university_list, './大学.xlsx')
