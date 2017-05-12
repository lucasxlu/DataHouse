import re


def parse_date(data_string):
    match_result = re.match('\d{4}-*\d{0,2}-\d{0,2}', data_string)
    return match_result.group() if match_result is not None else 0


if __name__ == '__main__':
    result = parse_date('(北京电影节) / (中国大陆) / 金城武 / 周冬雨 / 孙艺洲 / 奚梦瑶 '
                        '/ 杨祐宁 / 张国柱 / 高晓松 / 林志玲 / 中国大陆 / 许宏宇 / 106分钟 / 喜剧 / 爱情 / '
                        '李媛 Yuan Li / 许伊萌 Yimeng Xu / 蓝白色(原著) / 汉语普通话')
    print(result)
