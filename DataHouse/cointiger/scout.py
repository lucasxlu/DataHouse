import time
import requests

from cointiger_sdk import cointiger
from cointiger_sdk import const


class Scout:
    def __init__(self, api, secret):
        self.api = api
        self.secret = secret
        self.Trading_Macro_v2 = "https://api.cointiger.com/exchange/trading/api/v2"

    def show_public_info(self):
        # 时间戳
        print(cointiger.timestamp())
        # 支持币种
        print(cointiger.currencys())

        # 24小时行情
        print(cointiger.ticker('btcusdt'))
        # 深度
        print(cointiger.depth('btcusdt'))
        # k线
        print(cointiger.kline('btcusdt', '1min'))
        # 成交历史
        print(cointiger.trade('btcusdt'))
        # 24小时行情列表
        print(cointiger.tickers())

    def show_private_info(self):
        cointiger.set_key_and_secret(self.api, self.secret)

        order_data = {
            'api_key': self.api,
            'symbol': 'btcusdt',
            'price': '0.01',
            'volume': '1',
            'side': const.SideType.BUY.value,
            'type': const.OrderType.LimitOrder.value,
            'time': int(time.time())
        }
        # 签名
        print(cointiger.get_sign(order_data))
        # 创建订单
        print(cointiger.order(dict(order_data, **{'sign': cointiger.get_sign(order_data)})))

        # 撤销订单
        cancel_data = {
            'api_key': self.api,
            'orderIdList': '{"btcusdt":["1","2"],"ethusdt":["11","22"]}',
            'time': int(time.time()),
        }
        print(cointiger.batch_cancel(dict(cancel_data, **{'sign': cointiger.get_sign(cancel_data)})))

        # 查询委托
        print(cointiger.orders('btcusdt', 'canceled', int(time.time()), types='buy-market'))

        # 查询成交
        print(cointiger.match_results('btcusdt', '2018-07-18', '2018-07-19', int(time.time())))

        # 查询成交明细
        print(cointiger.make_detail('btcusdt', '123', int(time.time())))

        # 查询订单详情
        print(cointiger.details('btcusdt', '123', int(time.time())))


if __name__ == '__main__':
    scout = Scout(api="",
                  secret="")

    response = requests.get("https://api.cointiger.com/exchange/trading/api/v2/currencys",
                            headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
                                "Host": "api.cointiger.com",
                                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                            }, timeout=50)

    print(response.json())
