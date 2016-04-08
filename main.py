#-*- coding:utf-8 -*-
__requires__ = 'Scrapy==0.24.4'
from pkg_resources import load_entry_point

if __name__ == '__main__':
    print "run."
    argv = ["scrapy", "crawl", "weibo", "-a", "name=15557106533", "-a", "password=87092046", "-a", "uid=3856926178"]
    load_entry_point('Scrapy==0.24.4', 'console_scripts', 'scrapy')(argv)
