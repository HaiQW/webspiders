# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class WeiboItem(Item):
    # define the fields for your item here like:
    uid = Field()
    # uname = Field()
    # url = Field()
    content = Field()
    goods = Field()
    replies = Field()
    retweets = Field()
    timestamp = Field()

class ParamItem(Item):
    name = Field()
    weibo_num = Field()
    fellowing_num = Field()
    fellower_num = Field()

