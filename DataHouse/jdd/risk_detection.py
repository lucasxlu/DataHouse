import os
import sys

import pandas as pd
import numpy as np

DATA_BASE_DIR = 'E:/Dataset/JDD/RiskDetection/Risk_Detection_Qualification'


def load_data():
    t_login = pd.read_csv(os.path.join(DATA_BASE_DIR, 't_login.csv'))
    t_trade = pd.read_csv(os.path.join(DATA_BASE_DIR, 't_trade.csv'))

    t_login_test = pd.read_csv(os.path.join(DATA_BASE_DIR, 't_login_test.csv'))
    t_trade_test = pd.read_csv(os.path.join(DATA_BASE_DIR, 't_trade_test.csv'))

    print(t_login)


if __name__ == '__main__':
    load_data()
