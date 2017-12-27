import json
import time
from pprint import pprint

import pandas as pd


def precess_token_sales(json_str_path):
    result = []
    with open(json_str_path, mode='rt') as f:
        json_obj = json.load(f)

        index = 0
        for _ in json_obj['data']:
            print('*' * 100)
            print(index)
            pprint(_)
            index += 1
            print('*' * 100)
            try:
                result.append([_['_id'], _['name'], _['description'], _['symbol'], _['status'], _['usd_raised'],
                               _['month'],
                               time.ctime(_['start_date']).replace('08:00:00', '') if _['start_date']
                                                                                      not in ['', '#N/A'] else '',
                               time.ctime(_['end_date']).replace('08:00:00', '') if _['end_date']
                                                                                    not in ['', '#N/A'] else '',
                               _['token_sale_price'],
                               _['current_token_price'], _['token_return'], _['whitepaper']])
            except:
                result.append([_['_id'], _['name'], _['description'], '', _['status'], _['usd_raised'],
                               _['month'],
                               time.ctime(_['start_date']).replace('08:00:00', '') if _['start_date']
                                                                                      not in ['', 'N/A'] else '',
                               time.ctime(_['end_date']).replace('08:00:00', '') if _['end_date']
                                                                                    not in ['', 'N/A'] else '',
                               _['token_sale_price'],
                               _['current_token_price'], _['token_return'], _['whitepaper']])

        cols = ['id', 'name', 'description', 'symbol', 'status', 'usd_raised', 'month', 'start_date', 'end_date',
                'token_sale_price', 'current_token_price', 'token_return', 'whitepaper']
        df = pd.DataFrame(result, columns=cols)

        df.to_excel("./TokenData.xlsx", sheet_name='TOKEN SALES', index=False)
        print('processing done!')


if __name__ == '__main__':
    precess_token_sales("./data.json")
