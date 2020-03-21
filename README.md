<p align="left"><img src="logo/horizontal.png" alt="DataHouse" height="120px"></p>

# Data Mining Workspace

## Introduction
   This repository is designed for data scraping, data mining and data visualization in house price, job interviewing and SNS data mining.
   We collect data with [scrapy](https://docs.scrapy.org/en/latest/index.html) and [requests](http://www.python-requests.org/en/master/), data pre-processing and machine learning with [scikit-learn](http://scikit-learn.org/stable/) and [pandas](http://pandas.pydata.org/).
   Data storing with [MongoDB](https://docs.mongodb.com/).
   
   There are several modules belongs to different application.  
   * [JobCn](DataHouse/jobcn)
   * [Douban Book](DataHouse/spiders/douban_book_spider.py)
   * [Douban Movie](DataHouse/spiders/douban_movie_spider.py)
   * [Anjuke](DataHouse/spiders/anjuke_spider.py)
   * [fang.com](DataHouse/crawler/fang_crawler.py)
   * [Lian Jia](DataHouse/crawler/lianjia_crawler.py)
   * [LiePin](DataHouse/spiders/liepin_spider.py)
   * [Music Toolbox](DataHouse/music)
   * [51 Job](DataHouse/51job)
   * [Zhihu](DataHouse/zhihu)
   * [Rongyp](DataHouse/rongyp)
   * [JD](DataHouse/jd)
    
## Prerequisite
   > Python version >= 3.5  
   > requests   
   > scrapy  
   > pandas    
   > scikit-learn   
   > pymongo    
   > TensorFlow >= 1.6  
   > PyTorch >= 0.3.1
   
- Installation

   ```sudo pip3 install -r requirements.txt```  

- Start MongoDB Service

   ```sudo service mongod start```

## Report
   * [House Price Prediction](https://zhuanlan.zhihu.com/p/26949876).
   * [Zhihu Live Analysis](https://zhuanlan.zhihu.com/p/30514792)
   * [City Analysis](https://zhuanlan.zhihu.com/p/28954770)
   * [JobCn](https://www.zhihu.com/question/30080717/answer/234002087)


## Note
   - This repository can be only used for research and non-commercial applications.
