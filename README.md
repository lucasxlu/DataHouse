# Data Mining Workspace

## Introduction
   This repository is designed for data analysis and data visualization in house price, job interviewing and SNS data mining.
   We collect all the data with [scrapy](https://docs.scrapy.org/en/latest/index.html) and [requests](http://www.python-requests.org/en/master/), data pre-processing and machine learning with [scikit-learn](http://scikit-learn.org/stable/) and [pandas](http://pandas.pydata.org/).
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
   * [Zhihu Live](DataHouse/zhihu)
    
## Prerequisite
   > Python version >= 3.4  
   > requests   
   > scrapy  
   > pandas    
   > scikit-learn   
   > pymongo
   
   
## Installation
    sudo pip3 install -r requirements.txt  


## Report
   The report of house price prediction has been released on [Zhihu](https://zhuanlan.zhihu.com/p/26949876) with my presentation [here](/Presentation/House_ML.pptx). 


## Note
   V1.6.2_ALPHA is released.
   More features are being developed and will be released soon~  