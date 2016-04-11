# -*- coding: utf-8 -*-
"""
知乎的爬虫登陆模块. The login module of zhihu.
"""
import re
import requests
import logging, logging.config
from PIL import Image

# 加载logging配置
logging.config.fileConfig("/home/haiqw/Documents/my_projects/web_spiders/logging.cfg")
logger_name = "zhihu"
logger = logging.getLogger(logger_name)

class ZhihuLogin:
    """知乎登陆模块"""
    user_agent = (
         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
         '(KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
    )
    session = requests.session()
    session.headers['User-Agent'] = user_agent
    session.headers['Origin'] = 'http://www.zhihu.com/'

    def __init__(self, user, password):
        if user == None or password == None:
            raise ValueError("Value Error, got the None value of user or password.")
        self.user = user
        self.password = password

    def _get_captcha(self):
        """
        Get captcha gif and let the user himself to recognize the captcha.
        获取用户登陆时的验证码，并让用户识别验码.
        """
        # 获取验证码图片的url
        resp = self.session.get('https://www.zhihu.com/#sign')
        captcha_url = re.search('/captcha.gif',resp.text).group(0)
        print captcha_url
        # 获取验证码图片并保存
        captcha_str = None
        captcha = self.session.get('http://www.zhihu.com/captcha.gif')
        captcha_pic = open('captcha.gif', 'wb')
        for line in captcha.iter_content(10):
            captcha_pic.write(line)
        captcha_pic.close()
        # 输入验证码
        print('Please enter the captcha: ')
        captcha_str = raw_input()
        return captcha_str

    def login(self):
        # 获取_xsrf的值.get _xsrf
        resp = self.session.get('http://www.zhihu.com/#signin')  # <input type="hidden" name="_xsrf" value="..."/>
        parse_str = re.search('<input\s+type\s*=\s*"\s*hidden\s*".*', resp.text).group(0)
        _xsrf = re.search('value\s*=\s*"\w+"', parse_str).group(0)
        _xsrf = _xsrf.replace('value=', "").replace('"', '')

        post_data = {
            '_xsrf': _xsrf,
            'email': self.user,
            'password': self.password,
            'remember_me': 'true'
        }

        # 模拟登陆
        r = 1
        while not r == 0:
            # 需要用户输入验证码的情况

            # 登陆
            resp = self.session.post('http://www.zhihu.com/login/email', data=post_data)
            r = re.search('"r"\s*:\s*\w+,', resp.text).group(0)
            r = int(r.replace('"', '').replace(',', '').replace(':', '').replace('r', ''))
            if r == 0:
                print (u"知乎登陆成功.")
                logger.info(u'知乎登陆成功.')
                break
            else:
                logger.info(u'知乎登陆失败，重新登陆.')
                print(u'知乎登陆失败，用户名或者密码错误, 需要重新输入账号信息.')
                print(u'请输入用户名:')
                self.user = raw_input()
                print(u'请输入密码:')
                self.password = raw_input()
                post_data = {
                    '_xsrf': _xsrf,
                    'email': self.user,
                    'password': self.password,
                    'remember_me': 'true'
                }
        return self.session


def main():
    t_zhihu = Zhihu(user='wenghaiqin@qq.com', password='')
    t_zhihu.login()

if __name__ == '__main__':
    main()
