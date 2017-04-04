# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class HeadlinesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hotNews = Field()  # mongoDB collection名字
    detailsUrl = Field()  # 新闻详情链接
    title = Field()  # 标题
    summary = Field()  # 摘要
    imageUrl = Field()  # 图片链接
    url = Field()  # 新闻来源链接
    urlMd5 = Field()  # 新闻来源链接MD5值
    time = Field()  # 插入mongoDB的时间
