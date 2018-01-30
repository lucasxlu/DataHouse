import requests
from bs4 import BeautifulSoup
import time
import re
import datetime
import xlsxwriter

starttime = datetime.datetime.now()
last = 0
name = ['职位名称', '公司名称', '薪资', '学历要求', '工作地点', '要求', '福利', '发布时间', '围观', '点赞', '评论']
tag = ['jobname', 'company', 'salary', 'education', 'place', 'tip', 'weal', 'date', 'show-look', 'show-praise',
       'show-review']


def getHtmlCode(url):
    headers = {
        "Host": "www.rongyp.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Referer": "https://www.rongyp.com/index.php?m=Home&c=Job&a=jobSearch",
    }
    r = requests.get(url, headers=headers)
    r.encoding = 'UTF-8'
    page = r.text
    return page


def __parseHtml(page):
    soup = BeautifulSoup(page, 'html.parser')
    data = [];
    for li in soup.select('.ryp-search-list'):
        jobname = li.select('.jobname')[0].text
        company = li.select('.company')[0].text
        salary = li.select('.salary')[0].text
        education = li.select('.education')[0].text
        place = li.select('.place')[0].text
        tip = ''
        if (li.select('.tip') != []):
            tip = li.select('.tip')[0].text.replace('\n', '').strip()
        arr = []
        for h in li.select('.weal'):
            arr.append(h.text)
        weal = ','.join(arr)
        date = li.select('.date')[0].text
        look = re.findall(r'[^()]+', li.select('span.right a')[0].text)[1]
        praise = re.findall(r'[^()]+', li.select('span.right a')[1].text)[1]
        review = re.findall(r'[^()]+', li.select('span.right a')[2].text)[1]
        data.append([jobname, company, salary, education, place, tip, weal, date, look, praise, review])
    return data


def save_excel(fin_result, name, file_name):  # 将抓取到的招聘信息存储到excel当中
    book = xlsxwriter.Workbook(r'C:\Users\Administrator\Desktop\%s.xlsx' % file_name)  # 默认存储在桌面上
    tmp = book.add_worksheet()
    row_num = len(fin_result)
    for i in range(1, row_num):
        if i == 1:
            tag_pos = 'A%s' % i
            tmp.write_row(tag_pos, name)
        else:
            con_pos = 'A%s' % i
            content = fin_result[i - 1]  # -1是因为被表格的表头所占
            tmp.write_row(con_pos, content)
    book.close()


if __name__ == '__main__':
    fin_result = []
    for page_num in range(1, 1000):
        if (last == 1):
            break
        else:
            url = 'https://www.rongyp.com/index.php?m=Home&c=Job&a=jobSearch'
            # time.sleep(3)
            print('******************************正在下载第%s页内容*********************************' % page_num)
            if (page_num > 1):
                url = '%s%s%s' % (url, '&p=', page_num)
            page = getHtmlCode(url)
            page_result = __parseHtml(page)
            if (len(page_result) == 0):
                last = 1
            fin_result.extend(page_result)
    # file_name = input('抓取完成，输入文件名保存：')
    file_name = 'ryp_job'
    save_excel(fin_result, name, file_name)
    endtime = datetime.datetime.now()
    time = (endtime - starttime).seconds
    print('总共用时：%s s' % time)
