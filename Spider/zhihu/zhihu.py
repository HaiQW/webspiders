# -*- coding: utf-8 -*-
"""
The module that help login in zhihu.
"""

import urllib2
import urllib
import cookielib
import re
import requests
import sys

class Zhihu:
    user_agent = (
         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
    )
    session = requests.session()
    session.headers['User-Agent'] = user_agent
    session.headers['Origin'] = 'http://www.zhihu.com'

    def __init__(self, user, password):
        if user == None or password == None:
            raise ValueError("Value Error, got the None value of user or password.")
        self.user = user
        self.password = password

        # Get a Cookie object
        self.cookie_obj = cookielib.LWPCookieJar()
        # Bind Cookie object to HttpRequest Object
        self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie_obj)
        # Init an opener
        self.opener = urllib2.build_opener(self.cookie_support, urllib2.HTTPHandler)
        # Install the opener object
        urllib2.install_opener(self.opener)

    def login(self):
        # get _xsrf
        resp = self.session.get('http://www.zhihu.com/')
        # <input type="hidden" name="_xsrf" value="d692bea9ca68c27fb92f411942d8e0a4"/>
        parse_str = re.search('<input\s+type\s*=\s*"\s*hidden\s*".*', resp.text).group(0)
        _xsrf = re.search('value\s*=\s*"\w+"', parse_str).group(0)
        _xsrf = _xsrf.replace('value=', "").replace('"', '')
        print _xsrf

        captcha_url = 'http://www.zhihu.com/captcha.gif'
        captcha = self.session.get(captcha_url, stream=True)
        captcha_pic = open('pic.gif', 'w')
        for line in captcha.iter_content(10):
            captcha_pic.write(line)
        captcha_pic.close()

        captcha_str = raw_input()

        post_data = {
            '_xsrf': _xsrf,
            'email': 'wenghaiqin@qq.com',
            'password': 'wenghaiqin',
            'remember_me': 'true',
            'captcha': captcha_str
        }
        resp = self.session.post(
            'http://www.zhihu.com/login/email',
            data = post_data
        )

        # captcha_pic.close()
        # print captcha
        # pic = open(captcha)
        # print resp.text
        # print u"\u9a8c\u8bc1\u7801\u9519\u8bef"
        # login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']', resp.text).group(1)
        print resp.text
        # self.session.get(login_url)
        # response = self.session.get("http://weibo.com")
        # return self.session
        pass


def main():
    t_zhihu = Zhihu(user='wenghaiqin@qq.com', password='1234567978')
    t_zhihu.login()

if __name__ == '__main__':
    main()