import itertools
from pprint import pprint

import pymysql
import requests
from bs4 import BeautifulSoup
from lxml import etree

INDUSTRY_XML_PATH = './industry.xml'
PLACE_XML_PATH = './place.xml'


def parse_industry_xml():
    """
    parse config xml info from industry.xml
    :return: dict
    """
    tree = etree.parse(INDUSTRY_XML_PATH)

    industry_name_list = tree.xpath('//industry/text()')
    industry_value_list = tree.xpath('//industry/@value')

    industry = dict(itertools.zip_longest(industry_name_list, industry_value_list[:len(industry_name_list)]))

    return industry


def parse_place_xml():
    """
    parse config xml info from place.xml
    :return: dict
    """
    tree = etree.parse(PLACE_XML_PATH)

    place_name_list = tree.xpath('//place/text()')
    place_value_list = tree.xpath('//place/@value')

    place = dict(itertools.zip_longest(place_name_list, place_value_list[:len(place_name_list)]))

    return place


def db_connect():
    conn = pymysql.connect("localhost", "root", "root", "qcwy", use_unicode=True, charset="utf8")

    return conn


def db_dict_insert(tname, k, v):
    con = db_connect()
    cursor = con.cursor()

    sql = "INSERT INTO dict(tname, key, value) VALUES('%s', '%s', '%s')" % (tname, k, v)
    try:
        cursor.execute(sql)
        con.commit()
    except:
        pass


def db_insert(o):
    con = db_connect()
    cursor = con.cursor()

    sql = "INSERT INTO 51job(cjobname, cocname, coid, hasposted, isexpired, isjump, jobareaname, jobid, jobsalaryname, jumpurl,typeid,placeid)\
        VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (o['cjobname'], o['cocname'], o['coid'], o['hasposted'], o['isexpired'], o['isjump'], o['jobareaname'],
           o['jobid'], o['jobsalaryname'], o['jumpurl'], o['typeid'], o['placeid'])
    try:
        cursor.execute(sql)
        con.commit()
    except:
        pass


def crawl(pageno, jobarea, indtype):
    url1 = 'http://m.51job.com/ajax/search/joblist.ajax.php'
    data = {"jobarea": jobarea, "indtype": indtype, "pageno": pageno}
    headers = {"Accept": "application/json",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "http://m.51job.com/search/joblist.php?jobarea=180200&indtype=32",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
               }
    res1 = requests.post(url1, params=data, headers=headers)
    if len(res1.json()['data']) > 0:
        for o in res1.json()['data']:
            o['placeid'] = jobarea
            o['typeid'] = indtype
            db_insert(o)
        print('page %d data has been crawled done !' % pageno)
        pageno += 1
        crawl(pageno, jobarea, indtype)


if __name__ == '__main__':
    for pls_name, pls_id in parse_place_xml().items():
        for ind_name, ind_id in parse_industry_xml().items():
            crawl(1, pls_id, ind_id)
    # for pls_name, pls_id in parse_place_xml().items():
    #     db_dict_insert("工作区域", pls_name, pls_id)
    print("--END--")
