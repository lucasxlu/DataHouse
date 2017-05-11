import logging

import numpy as np
import pandas as pd
from sklearn import linear_model

RESOURCE_DIR = '/home/lucasx/PycharmProjects/DataHouse/DataSet/'
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s \t', level=logging.INFO, filemode='a',
                    filename='loginfo.log')


def train_and_predict(filepath):
    df = pd.read_excel(filepath, 'HouseInfo')

    def _preprocessing(dataframe):
        dataframe['buildYear'] = dataframe['buildYear'].fillna(np.median(dataframe['buildYear'].dropna()))
        label_and_value = {
            "武昌": 1,
            "江岸": 2,
            "江汉": 3,
            "硚口": 4,
            "洪山": 5,
            "青山": 6,
            "汉阳": 7,
            "东西湖": 8,
            "沌口开发区": 9,
            "江夏": 10,
            "黄陂": 11,
            "其他": 12,
            "蔡甸": 13,
            "汉南": 14,
            "新洲": 15
        }
        dataframe['areaCode'] = [label_and_value[i] for i in dataframe['area']]

        return dataframe

    df = _preprocessing(dataframe=df).loc[:, ['areaCode', 'buildYear', 'saleNum', 'midPrice']]
    df.to_excel(RESOURCE_DIR + 'data.xlsx', sheet_name='Sheet1')

    X_digits = df.loc[:, ['areaCode', 'buildYear', 'saleNum']]
    y_digits = df.loc[:, ['midPrice']]
    regression = linear_model.Lasso(alpha=0.1)

    # do cross-validation
    X_folds = np.array_split(X_digits, 10)
    y_folds = np.array_split(y_digits, 10)
    scores = list()
    for k in range(10):
        X_train = list(X_folds)
        X_test = X_train.pop(k)
        X_train = np.concatenate(X_train)
        y_train = list(y_folds)
        y_test = y_train.pop(k)
        y_train = np.concatenate(y_train)
        scores.append(regression.fit(X_train, y_train).score(X_test, y_test))
    logging.info(scores)

    from sklearn.externals import joblib
    joblib.dump(regression, RESOURCE_DIR + 'reg_model.pkl')

    print(
        'The max inference accuracy is {:%}'.format(np.array(scores).max()))


def inference(areaCode, buildYear, saleNum):
    from sklearn.externals import joblib
    regression = joblib.load(RESOURCE_DIR + 'reg_model.pkl')
    predict_price = regression.predict(np.array([areaCode, buildYear, saleNum]).reshape(1, 3))

    return predict_price


if __name__ == '__main__':
    # train_and_predict(RESOURCE_DIR + 'anjuke.xlsx')
    price = inference(1, 2015, 1611)
    print('Your house worths %d RMB.' % price)
