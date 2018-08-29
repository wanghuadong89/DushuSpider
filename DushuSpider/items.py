# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DushuspiderItem(scrapy.Item):
    # 一级页面
    # 书名
    name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 封面
    cover_img = scrapy.Field()
    # 二级页面
    # 出版社
    cbs = scrapy.Field()
    # 内容简介
    content = scrapy.Field()
    # 作者简介
    author_info = scrapy.Field()
    # 定价
    price = scrapy.Field()
    # 目录
    mulu = scrapy.Field()
