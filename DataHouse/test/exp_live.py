from pymongo import MongoClient
import pandas as pd

if __name__ == '__main__':
    client = MongoClient()
    db = client.zhihu.live
    lives = db.find({})
    result = []

    for live in lives:
        subject = live['subject']
        url = "https://www.zhihu.com/lives/%s" % live['id']
        result.append([subject, url])

    df = pd.DataFrame(result)
    df.to_excel('D:/live.xlsx', sheet_name='Live')
