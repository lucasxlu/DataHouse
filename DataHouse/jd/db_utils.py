from pymongo import MongoClient


def insert_item(item):
    """
    insert an item into MongoDB
    :param item:
    :return:
    :Version:1.0
    """
    client = MongoClient()
    db = client.jd.goods

    result = db.insert_one(item)