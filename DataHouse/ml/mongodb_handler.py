import configparser

import pandas as pd
from pymongo import MongoClient


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def read_mongo(db, collection, query={}, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('/home/lucasx/PycharmProjects/DataHouse/DataSet/mongodb_config.ini')
    db = _connect_mongo(config['douban']['host'], int(config['douban']['port']), None, None, config['douban']['db'])
    df = read_mongo(db, 'movie', query={}, no_id=True)
    print(df)
