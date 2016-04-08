# -*- coding: utf-8 -*-
"""
知乎的爬虫登陆模块. The login module of zhihu.
"""
import re
import requests
from PIL import Image

class Zhihu:
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
        Let the user himself to recognize the captcha.
        """
        captcha_str = None
        # get the captcha gif picture
        captcha = self.session.get('http://www.zhihu.com/captcha.gif')
        # read and save this gif
        captcha_pic = open('captcha.gif', 'wb')
        for line in captcha.iter_content(10):
            captcha_pic.write(line)
        captcha_pic.close()

        print('Please enter the captcha: ')
        captcha_str = raw_input()

        return captcha_str

    def login(self):
        # get _xsrf
        resp = self.session.get('http://www.zhihu.com/#signin')  # <input type="hidden" name="_xsrf" value="..."/>
        parse_str = re.search('<input\s+type\s*=\s*"\s*hidden\s*".*', resp.text).group(0)
        _xsrf = re.search('value\s*=\s*"\w+"', parse_str).group(0)
        _xsrf = _xsrf.replace('value=', "").replace('"', '')

        # # load captcha.gif
        # captcha_url = 'http://www.zhihu.com/captcha.gif'
        # captcha = self.session.get(captcha_url, stream=True)
        # captcha_pic = open('picture.gif', 'w')
        # for line in captcha.iter_content(10):
        #     captcha_pic.write(line)
        # captcha_pic.close()
        #
        #
        # # Let the user to recognize the captcha string
        # print("Please enter the captcha: ")
        # captcha_str = self._get_captcha()

        # prepare post data to login
        post_data = {
            '_xsrf': _xsrf,
            'email': 'wenghaiqin@qq.com',
            'password': 'wenghaiqin',
            'remember_me': 'true'
        }

        # login
        # resp = self.session.post(
        #     'http://www.zhihu.com/login/email',
        #     data = post_data
        # )

        # print resp.text

        # error_code = re.search('', )
        # set the maximum login times
        r = 1
        while not r == 0:
            print r
            # get the captcha string
            captcha_str = self._get_captcha()
            post_data['captcha'] = captcha_str

            #login
            resp = self.session.post('http://www.zhihu.com/login/email', data=post_data)
            print resp.text
            r = re.search('"r"\s*:\s*\w+,', resp.text).group(0)
            r = int(r.replace('"', '').replace(',', '').replace(':', '').replace('r', ''))
            print r

        # print requests.utils.dict_from_cookiejar(self.session.cookies)
        return self.session


def main():
    t_zhihu = Zhihu(user='wenghaiqin@qq.com', password='1234567978')
    t_zhihu.login()

if __name__ == '__main__':
    main()
