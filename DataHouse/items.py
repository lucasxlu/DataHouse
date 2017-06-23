# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Anjuke(scrapy.Item):
    # DataHouse object of Anjuke
    address = scrapy.Field()
    area = scrapy.Field()
    block = scrapy.Field()
    build_year = scrapy.Field()
    image = scrapy.Field()
    mid_price = scrapy.Field()
    name = scrapy.Field()
    sale_num = scrapy.Field()
    url = scrapy.Field()


class DoubanBook(scrapy.Item):
    # Douban book object
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    score = scrapy.Field()
    scorerNum = scrapy.Field()
    price = scrapy.Field()
    publishDate = scrapy.Field()


class DoubanMovie(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    score = scrapy.Field()
    scorerNum = scrapy.Field()
    date = scrapy.Field()

    def __iter__(self):
        yield 'title', self.title
        yield 'url', self.url
        yield 'image', self.image
        yield 'category', self.category
        yield 'score', self.score
        yield 'scorerNum', self.scorerNum
        yield 'date', self.date


class LiePin(scrapy.Item):
    jobid = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    education = scrapy.Field()
    experience = scrapy.Field()
    company = scrapy.Field()
    industryField = scrapy.Field()
    tags = scrapy.Field()
    publishTime = scrapy.Field()
    feedback = scrapy.Field()
    isVerified = scrapy.Field()
