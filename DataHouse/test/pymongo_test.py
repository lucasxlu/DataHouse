from pymongo import MongoClient


def insert_item(item):
    client = MongoClient()
    db = client.douban.movie
    result = db.insert_one(item)


def query_document():
    client = MongoClient()
    db = client.douban.movie
    cursor = db.find()
    for document in cursor:
        print(document)


def delete_item():
    client = MongoClient()
    db = client.douban.movie
    db.delete_many({})


if __name__ == '__main__':
    query_document()
    delete_item()
    query_document()
