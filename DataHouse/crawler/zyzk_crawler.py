# 中医智库爬虫
import os
import requests
from bs4 import BeautifulSoup
import json

COOKIES = dict(
    cookies_are="pgv_pvi=3986451456; pgv_si=s5456275456; NTKF_T2D_CLIENTID=guest332ACA66-DEC9-0830-369C-6E3A9A70B045; zkudts=1543870524; Hm_lvt_ace6d17be8a406bb09626456ab9d447a=1548081851; Hm_lpvt_ace6d17be8a406bb09626456ab9d447a=1548081851; svrid=5aff15db8fb99d9bd967d5b9eeccc5d1; checkCookieTime=1548130021681; nTalk_CACHE_DATA={uid:kf_9050_ISME9754_guest332ACA66-DEC9-08,tid:1548126339190410}; csrftoken=2YEP69r9axN5MzTMmzz1zBXZ61TuyFMe; sessionid=qcbqusvemwfs5l3222bwagkow648rbzj; authenticated=9754369; shfskey=20190122T040701.602552770267")


def get_all_categories():
    """
    get all disease categories
    :return:
    """
    headers = {
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.zk120.com/an/?nav=ys',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get("https://www.zk120.com/an/ks/%E5%86%85%E7%A7%91?nav=ys", headers=headers,
                            cookies=COOKIES)

    disease_link_map = {}

    if response.status_code not in [403, 404, 500]:
        bs = BeautifulSoup(response.text, "lxml")
        for li in bs.find_all("section", class_="ice_bg space_pr space_pl")[0].find_all("li"):
            disease_link_map[li.a.text] = "https://www.zk120.com/" + li.a['href']

    with open('./disease_cat.json', mode='wt', encoding='utf-8') as f:
        json.dump(disease_link_map, f)

    return disease_link_map


def get_disease_all_sub_pages(disease_name):
    headers = {
        'dnt': '1',
        'referer': 'https://www.zk120.com/an/search?qe=%E5%B0%8F%E5%84%BF%E8%82%BA%E7%82%8E&nav=ys',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    disease_url = 'https://www.zk120.com/an/search?qe={0}&nav=ys'.format(disease_name)
    payload = {
        'qe': disease_name,
        'nav': 'ys',
        's': 0,
        'e': 10
    }
    response = requests.get(disease_url, headers=headers, cookies=COOKIES)

    disease_and_id = {}

    if response.status_code not in [403, 404, 500]:
        js = response.json()
        disease_id = []
        for _ in js['first_cluster']['medicases']:
            disease_id.append(_['url'].split('/')[-1].split('.')[0])

    disease_and_id[disease_name] = disease_id

    return disease_and_id


def write_html_content(disease_name, disease_id):
    headers = {
        'dnt': '1',
        'shtech-cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    s_url = 'https://www.zk120.com/an/get_detail_data/{0}'.format(disease_id)
    response = requests.get(s_url, headers=headers, cookies=COOKIES)

    if response.status_code not in [403, 404, 500]:
        js = response.json()
        print(js)
        title = js['title'].strip()

        content = ""

        if 'followups' in json.loads(js['medicase'].replace("'", "")).keys():
            followups = json.loads(js['medicase'].replace("'", ""))['followups']

            print(followups)
            # medicase = js['medicase'].encode('unicode').decode('utf-8')

            mkdirs_if_not_exist('D:/ChineseMedicine/%s' % disease_name)

            for followup in followups:
                for item in followup:
                    values = list(item.values())
                    content += '{0}: {1}'.format(values[0], values[1][0])
                    content += '\r'

                content += '\r\n'

        else:
            first = json.loads(js['medicase'].replace("'", ""))['first']
            print(first)
            for item in first:
                for v in item.values():
                    content += ' '.join(v)
                    content += '\r\n'

        with open('D:/ChineseMedicine/{0}/{1}.txt'.format(disease_name, title), mode='wt', encoding='utf-8') as f:
            f.write(content)
            f.flush()
            f.close()


def mkdirs_if_not_exist(dir_name):
    """
    make directory if not exist
    :param dir_name:
    :return:
    """
    if not os.path.isdir(dir_name) or not os.path.exists(dir_name):
        os.makedirs(dir_name)


if __name__ == '__main__':
    with open('./disease_cat.json', mode='rt', encoding='utf-8') as f:
        js = json.load(f)

    for k in js.keys():
        print('process %s ...' % k)

        try:
            disease_and_id = get_disease_all_sub_pages(k)
            disease_ids = disease_and_id[k]

            for disease_id in disease_ids:
                write_html_content(k, disease_id)
        except:
            pass
