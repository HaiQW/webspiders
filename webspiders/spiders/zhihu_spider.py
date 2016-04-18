# -*- coding: utf-8 -*-
import re
import urllib
import time
import requests
import logging
import logging.config

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.http import TextResponse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webspiders.utils.zhihu_login import ZhihuLogin
# from webspiders.items import WeiboItem, ParamItem

# 加载loging配置
logging.config.fileConfig("/home/haiqw/Documents/my_projects/webspiders/logging.cfg")
logger_name = 'zhihu'
logger = logging.getLogger(logger_name)


class ZhihuSpider(Spider):
    """知乎爬虫"""
    name = 'zhihu_spider'

    def __init__(self, name, password, uid, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.uid = uid
        self.start_urls = ['http://m.zhihu.com']
        self.allowed_domains = ['zhihu.com']
        self.zhihu = ZhihuLogin(name, password)
        # self.session = self.zhihu.login()  # zhihu模拟登陆
        #cookiejar = requests.utils.dict_from_cookiejar(self.session.cookies)
        #self.cookies = {'q_c1': cookiejar['q_c1'],
        #                'z_c0': cookiejar['z_c0'],
        #                'cap_id': cookiejar['cap_id'],
        #                '_xsrf': cookiejar['_xsrf'],
        #                'unlock_ticket': cookiejar['unlock_ticket'],
        #                'l_cap_id': cookiejar['l_cap_id'],
        #                'login': cookiejar['login'],
        #                'n_c': cookiejar['n_c']}
        #self.cookies2 = {'name': 'q_c1', 'value': cookiejar['q_c1'],
        #                 'name': 'z_c0', 'value': cookiejar['z_c0'],
        #                 'name': 'cap_id', 'value': cookiejar['cap_id'],
        #                 'name': '_xsrf', 'value': cookiejar['_xsrf'],
        #                 'name': 'unlock_ticket', 'value': cookiejar['unlock_ticket'],
        #                 'name': 'l_cap_id', 'value': cookiejar['l_cap_id'],
        #                 'name': 'login', 'value': cookiejar['login'],
        #                 'name': 'n_c', 'value': cookiejar['n_c']}
        #self.headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                        #              'AppleWebKit/537.36(KHTML, like Gecko)'
                        #              'Chrome/44.0.2403.155 Safari/537.36',
                        #'Origin': 'Origin: https://m.zhihu.com',
                        #'Content-Type': 'application/x-protobuf'}
        self.driver = webdriver.Firefox()
        self._login()
        # self.driver.add_cookie(self.cookies)

    def start_requests(self):
        """Parse zhihu homepage"""
        home_url = 'http://m.zhihu.com/'
        questions_url = 'https://m.zhihu.com/log/questions'
        # print self.driver.get_cookies()
        # self.driver.get(home_url)
        # self.driver.add_cookie(self.cookies2)
        # print self.driver.get_cookies()
        # self.driver.close()
        yield Request(url=home_url, cookies=self.cookies, headers=self.headers,
                      callback=self._parse_homepage)
        yield Request(url=questions_url, cookies=self.cookies,
                      headers=self.headers, callback=self._parse_questions)

    def _parse_homepage(self, response):
        """解析知乎的主页home page"""
        # print response.meta
        # print response.body
        logger.info('获取zhihu的主页homepage信息.')

    def _parse_questions(self, response):
        """获取zhihu的所有问题"""
        logger.info("获取zhihu的所有问题.")
        # print response.body

    def _login(self):
        """知乎爬虫的登陆模块(此处用selenium模拟登陆)"""
        r = 1
        while r != 0:
            # try:
                self.driver.set_page_load_timeout(20)  # 防止页面加载不完
                self.driver.get('https://www.zhihu.com/#signin')
                time.sleep(10)  # sleep 20 秒等待用户输入账号信息
                response = TextResponse(u'https://www.zhihu.com/#signin', self.driver.page_source, encoding='utf-8')
                response.xpath('//script')
            #except:
            #    pass
            # email = self.driver.find_element_by_xpath("//input[@name='email']")
            # email.clear()
            # email.send_keys(self.user)
            # password = self.driver.find_element_by_xpath("//input[@name='password']")
            # password.clear()
            # password.send_keys(self.pwd)
            # form = self.driver.find_element_by_xpath("//form[@class='zu-side-login-box']")
            # form.submit()
            # somedom = WebDriverWait(self.driver, 60).until(lambda brow: brow.find_elements_by_class_name("zu-main-feed-con"))[0]
            # html = somedom.find_element_by_xpath("//*").get_attribute("outerHTML")
            # print html
            # self.driver.quit()
