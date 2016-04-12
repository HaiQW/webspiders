# -*- coding:utf-8 -*-
"""ZhihuSpiderc测试模块
HaiQW: 2016-04-14"""
__requires__ = 'Scrapy==0.24.4'
import unittest
from pkg_resources import load_entry_point


# 执行测试ZhihuSpider的类
class TestZhihuSpider(unittest.TestCase):
    """ Zhihu爬虫测试类. ZhihuSpider test class"""
    def test_init(self):
        zhihu_argv = ["scrapy", "crawl", "zhihu_spider", "-a",
                      "name=wenghaiqin@qq.com", "-a", "password=87092046",
                      "-a", "uid=3856926178"]
        load_entry_point(
            'Scrapy==0.24.4',
            'console_scripts',
            'scrapy')(zhihu_argv)
        t_zhuhu_spider = ZhihuSpider(user='wenghaiqin', password='15557106533')


# 构造测试集
def suite():
    """构造测测试集"""
    suite = unittest.TestSuite()
    suite.addTest(TestZhihuSpider("test_init"))
    return suite


# 测试
if __name__ == '__main__':
    import sys
    sys.path.append('/home/haiqw/Documents/my_projects/webspiders/')
    from webspiders.spiders.zhihu_spider import ZhihuSpider
    unittest.main(defaultTest='suite')
