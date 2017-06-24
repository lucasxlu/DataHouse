import os
import time
import json

import requests
from lxml import etree
from openpyxl import Workbook

JOBCN_DATA_DIR = '../../DataSet/jobcn/'
base_url = 'http://www.jobcn.com/search/listalljob_servlet.ujson'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.7 Safari/537.36'


class JobCn(object):
    pass


def crawl(jobFunction, pagenum):
    payload = {'p.keyword': '', 'p.keyword2': '', 'p.keywordType': '', 'p.pageNo': pagenum, 'p.pageSize': 40,
               'p.sortBy': 'postdate', 'p.statistics': 'false', 'p.totalRow': '', 'p.cachePageNo': 1,
               'p.cachePosIds': '', 'p.cachePosUpddates': '', 'p.jobFunction': jobFunction}

    headers = {'user-agent': user_agent, 'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Encoding': 'gzip, deflate', 'Host': 'www.jobcn.com', 'Origin': 'http://www.jobcn.com',
               'Referer': 'http://www.jobcn.com/search/listalljob.xhtml'}

    r = requests.post(base_url, data=payload, headers=headers)
    if r.status_code == 200:
        print(r.json())

        return r.json()
    elif r.status_code == 403:
        print('Access Denied!')
        return None


def get_max_page(jobFunction):
    base_url = 'http://www.jobcn.com/search/listalljob_servlet.ujson'

    payload = {'p.keyword': '', 'p.keyword2': '', 'p.keywordType': '', 'p.pageNo': 1, 'p.pageSize': 40,
               'p.sortBy': 'postdate', 'p.statistics': 'false', 'p.totalRow': '', 'p.cachePageNo': 1,
               'p.cachePosIds': '', 'p.cachePosUpddates': '', 'p.jobFunction': jobFunction}

    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Encoding': 'gzip, deflate', 'Host': 'www.jobcn.com', 'Origin': 'http://www.jobcn.com',
               'Referer': 'http://www.jobcn.com/search/listalljob.xhtml'}

    r = requests.post(base_url, data=payload, headers=headers)
    max_page = r.json()['pageCount']
    return max_page


def get_xml_joblist(job_xml_path):
    """
    read job params from job.xml
    :param job_xml_path:
    :return:
    """
    tree = etree.parse(job_xml_path)
    job_info = {}
    for each_job_node in tree.findall('//job'):
        jobFunction = each_job_node.attrib['jobFunction']
        jobname = each_job_node.text

        job_info[jobFunction] = jobname

    return job_info


"""
def json_file_to_list(each_job_json_dir):
    joblist = []
    for each_job_json in os.listdir(each_job_json_dir):
        with open(each_job_json_dir + os.sep + each_job_json, mode='r', encoding='utf-8') as f:
            for each_line in f.readlines():
                try:
                    json_obj = json.loads(each_line, encoding='utf-8')
                    joblist.append(json_obj)
                except:
                    pass
    return joblist
"""


def write_excel(lists, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = "职位信息"
    ws.cell(row=1, column=1).value = '职位ID'
    ws.cell(row=1, column=2).value = '职位名称'
    ws.cell(row=1, column=3).value = '所属部门'
    ws.cell(row=1, column=4).value = '公司名称'
    ws.cell(row=1, column=5).value = '薪资待遇'
    ws.cell(row=1, column=6).value = '学历要求'
    ws.cell(row=1, column=7).value = '公司福利'
    ws.cell(row=1, column=8).value = '年龄要求'
    ws.cell(row=1, column=9).value = '工作经验'
    ws.cell(row=1, column=10).value = '招聘数量'
    ws.cell(row=1, column=11).value = '工作地点'
    ws.cell(row=1, column=12).value = '联系邮箱'
    ws.cell(row=1, column=13).value = '联系电话'
    ws.cell(row=1, column=14).value = '公司ID'

    rownum = 2

    for _ in lists:
        ws.cell(row=rownum, column=1).value = _.posId
        ws.cell(row=rownum, column=2).value = _.posName
        ws.cell(row=rownum, column=3).value = _.deptName
        ws.cell(row=rownum, column=4).value = _.comName
        ws.cell(row=rownum, column=5).value = _.salaryDesc
        ws.cell(row=rownum, column=6).value = _.reqDegree
        ws.cell(row=rownum, column=7).value = _.benefitTags
        ws.cell(row=rownum, column=8).value = _.ageDesc
        ws.cell(row=rownum, column=9).value = _.workYearDesc
        ws.cell(row=rownum, column=10).value = _.candidatesNum
        ws.cell(row=rownum, column=11).value = _.jobLocation
        ws.cell(row=rownum, column=12).value = _.email
        ws.cell(row=rownum, column=13).value = _.contactTel
        ws.cell(row=rownum, column=14).value = _.comId
    wb.save(os.path.join(JOBCN_DATA_DIR, '%s.xlsx' % filename))
    print('Excel generates successfully......')


def start():
    job_info = get_xml_joblist('job.xml')
    for key, value in job_info.items():
        joblist = []
        '''get the max page number via jobFunction value'''
        max_page = get_max_page(key)
        print('is crawling %s data......' % value)
        index = 1
        while index <= max_page:
            json_obj = crawl(key, index)
            if json_obj is not None:
                for _ in json_obj['rows']:
                    jobcn = JobCn()
                    jobcn.posId = _['posId']
                    jobcn.posName = _['posName']
                    jobcn.deptName = _['deptName']
                    jobcn.comName = _['comName']
                    jobcn.salaryDesc = _['salaryDesc']
                    jobcn.reqDegree = _['reqDegree']
                    jobcn.benefitTags = _['benefitTags']
                    jobcn.ageDesc = _['ageDesc']
                    jobcn.workYearDesc = _['workYearDesc']
                    jobcn.candidatesNum = _['candidatesNum']
                    jobcn.jobLocation = _['jobLocation']
                    jobcn.email = _['email']
                    jobcn.contactTel = _['contactTel']
                    jobcn.comId = _['comId']
                    joblist.append(jobcn)
                index += 1

        print('%s\'s data is finished......' % value)
        time.sleep(2)
        write_excel(joblist, value)


if __name__ == '__main__':
    start()
