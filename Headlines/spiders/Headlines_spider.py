#!/usr/bin/env python
#-*-coding:utf8-*-
#import scrapy
#from scrapy.spider import Spider
import datetime
import calendar


date = datetime.datetime.now()

print date

from scrapy.spiders import CrawlSpider

from scrapy.selector import Selector

from Headlines.items import HeadlinesItem

from scrapy.http import Request

import hashlib

import requests

from scrapy import log

from bs4 import BeautifulSoup
import chardet
import time


class HeadlinesSpider(CrawlSpider):
    name = "Headlines"
    allowed_domains = ["top.baidu"]
    start_urls = ["http://top.baidu.com/buzz?b=1&c=513"]
    # 获取详情页的url的列表

    def parse(self, response):

        sel = Selector(response)
        sites = sel.xpath('//tr/td[@class="keyword"]')
        # print len(sites)

        list = []

        for site in sites:
            table = site.xpath(
                'a[@class="icon-search icon-xiang-imp"]/@href').extract()

            #print("Table type:%s" % type(table[i]))
            # print table
            # for i in range(0, len(url)):
            # print(url[i])

            aurl = str("http://top.baidu.com") + table[0][1:]
            list.append(aurl)

            print("=" * 15)
            print(aurl)
        # print list
        print len(list)

        # 获取每个详情页的源码并解析内容
        for i in range(len(list)):

            # 获取新闻详情页的源码并记录时间
            print("=" * 40)
            print("This is the %dth searching" % (i + 1))
            get_start = time.time()
            item = HeadlinesItem()
            item['detailsUrl'] = list[i]
            print("deailsUrl: %s" % list[i])
            resp = requests.get(list[i])

            # 对获取的源码进行转码
            html = resp.text.encode(resp.encoding)

            # 解析html的内容
            soup = BeautifulSoup(html)
            # print(soup.prettify()) 格式化呈现html
            # print soup.original_encoding

            # 解析新闻产生的时间并判断是否存在
            Time = soup.find("span", class_="date")
            if not Time:
                print("date not found")
            else:
                print("time:      %s" % Time.string)
                item['time'] = Time.string  # 时间

            # 解析新闻的摘要内容并判断是否存在
            Summary = soup.find("p", class_="text")
            if not Summary:
                print("text not found")
            else:
                print("summary:   %s" % Summary.string)
                item['summary'] = Summary.string  # 摘要

            # 解析新闻的标题和来源链接并判断是否存在
            # print soup.find("h4",class_="title")
            Title = soup.find("h4", class_="title")
            if not Title:
                print("title not found")
            else:
                print("title:     %s" % Title.string)
                item['title'] = Title.string  # 标题
                print("url        %s" % Title.contents[0]["href"])
                item['url'] = Title.contents[0]["href"]  # 新闻来源链接

                # 生成新闻来源链接的MD5值
                src = Title.contents[0]["href"]
                m2 = hashlib.md5()
                m2.update(src)
                item['urlMd5'] = m2.hexdigest()  # MD5值
                print("urlMd5:    %s" % m2.hexdigest())

            # 解析图片链接并判断是否存在
            # print soup.find("a",class_="related-news-img")
            ImageUrl = soup.find("a", class_="related-news-img")
            if not ImageUrl:
                print('related news img not found')
            else:
                print("imageUrl:  %s" % ImageUrl.contents[0]["src"])  # 图片链接
                item['imageUrl'] = ImageUrl.contents[0]["src"]
            get_end = time.time()
            time_cost = get_end - get_start
            print("The %dth searching cost time:%s" % ((i + 1), time_cost))
            yield item
