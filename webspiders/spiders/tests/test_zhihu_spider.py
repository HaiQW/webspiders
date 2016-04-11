#-*- coding:utf-8 -*-
__requires__ = 'Scrapy==0.24.4'
import sys
import unittest
from pkg_resources import load_entry_point


# class TestZhihuSpider(unittest.TestCase):
#     """ Zhihu爬虫测试类. ZhihuSpider test class"""
#     def test_init(self):
#         zhihu_argv = ["scrapy", "crawl", "zhihu_spider", "-a", "name=wenghaiqin@qq.com", "-a", "password=87092046", "-a", "uid=3856926178"]
#         load_entry_point('Scrapy==0.24.4', 'console_scripts', 'scrapy')(zhihu_argv)
#         t_zhuhu_spider = ZhihuSpider(user='wenghaiqin', password='15557106533')


if __name__ == '__main__':
    import sys
    sys.path.append('/home/haiqw/Documents/my_projects/spider/')
    print sys.path
    from web_spiders.zhihu_spider import ZhihuSpider
    # unittest.main()
    print sys.path
    # zhihu_argv = ["scrapy", "crawl", "zhihu_spider", "-a", "name=wenghaiqin@qq.com", "-a", "password=87092046", "-a", "uid=3856926178"]
    # load_entry_point('Scrapy==0.24.4', 'console_scripts', 'scrapy')(zhihu_argv)

    # zhihu_argv = ["scrapy", "crawl", "zhihu_spider", "-a", "name=wenghaiqin@qq.com", "-a", "password=87092046", "-a", "uid=3856926178"]
    t_zhihu = ZhihuSpider('wenghaiqin', '15557106533', '112456')
