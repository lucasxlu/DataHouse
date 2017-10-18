# News and Forum Text Crawler

## Introduction
This module includes web crawler for [ifeng](./ifeng_news_crawler.py), [sina news](msina_news_crawler.py), [renmin](renmin_crawler.py), [Baidu tieba](tieba_crawler.py) and [Renmin_NCCPC](./renmin_nccpc_report.py).


# Prerequisite
1. install 3rd party libraries

       sudo pip3 install -r requirements.txt 

2. download pre-trained model  
   
       polyglot download ner2.zh
       polyglot download embeddings2.zh
