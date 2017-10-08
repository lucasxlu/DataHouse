import re


def parse_date(data_string):
    match_result = re.match('\d{4}-*\d{0,2}-\d{0,2}', data_string)
    return match_result.group() if match_result is not None else 0


def parse_scorerNum(scorer_string):
    match_result = re.match('\d+', scorer_string.replace('(', '').replace(')', ''))
    return match_result.group() if match_result is not None else 0


def get_max_pagenum(tag):
    import requests
    from bs4 import BeautifulSoup
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/tag/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    response = requests.get('https://movie.douban.com/tag/%s' % tag, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html5lib')
        page_div = soup.find_all('div', class_='paginator')[0]
        a_list = page_div.find_all('a')
        max_pagenum = int(a_list[-2].get_text().strip())

        return max_pagenum


if __name__ == '__main__':
    # get_max_pagenum('爱情')
    avg_salary = []
    with open("C:\\Users\\LucasX\\Desktop\\salary.txt", mode='rt', encoding='utf-8') as f:
        for line in f.readlines():
            if line.strip() == '面议':
                avg_salary.append(None)
            elif '-' in line:
                min = float(line.strip().split('-')[0])
                max = float(line.replace('万', '').strip().split('-')[1])
                avg_salary.append((min + max) / 2)
            else:
                avg_salary.append(line)

    for _ in avg_salary:
        print(_)
