import json

import scrapy
import pandas as pd

from DataHouse.items import Anjuke

anjuke_list = []


class QuotesSpider(scrapy.Spider):
    name = "anjuke"

    def start_requests(self):
        urls = ['https://m.anjuke.com/wh/community/?from=trendency_rec_more&p=%d' % i for i in range(10)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for each_item in json.loads(response.text)['data']:
            anjuke = Anjuke(address=each_item['address'], area=each_item['area'], block=each_item['block'],
                            build_year=each_item['build_year'], image=each_item['image'],
                            mid_price=each_item['mid_price'], name=each_item['name'],
                            sale_num=each_item['sale_num'], url=each_item['url'])
            anjuke_list.append(anjuke)

    def close(spider, reason):
        df = pd.DataFrame(anjuke_list)
        df.to_excel('./DataSet/anjuke_house.xlsx', sheet_name='Community')
