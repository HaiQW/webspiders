# -*- coding: utf-8 -*-
import urllib
import urllib2
import base64
import re
import json
import binascii
import cookielib

import requests
import rsa

class weibo:
    WBCLIENT = 'ssologin.js(v1.4.5)'
    user_agent = (
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
        'Chrome/20.0.1132.57 Safari/536.11'
    )
    session = requests.session()
    session.headers['User-Agent'] = user_agent

    def __init__(self):
        # Get a Cookie object
        self.cookie_obj = cookielib.LWPCookieJar()
        # Bind Cookie object to HttpRequest Object
        self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie_obj)
        # Init an opener
        self.opener = urllib2.build_opener(self.cookie_support, urllib2.HTTPHandler)
        # Install the opener object
        urllib2.install_opener(self.opener)

    def _get_pwd(self, pwd, pubkey, servertime, nonce):
        key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)
        pwd = rsa.encrypt(message.encode('utf-8'), key)
        return binascii.b2a_hex(pwd)

    def _get_user(self, username):
        username_ = urllib.quote(username)
        username = base64.encodestring(username_)[:-1]
        return username

    def login(self, username, pwd):
        resp = self.session.get(
            'http://login.sina.com.cn/sso/prelogin.php?'
            'entry=sso&callback=sinaSSOController.preloginCallBack&'
            'su=%s&rsakt=mod&client=%s' %
            (base64.b64encode(username.encode('utf-8')), self.WBCLIENT)
        )
        pre_login_str = re.match(r'[^{]+({.+?})', resp.text).group(1)
        pre_login = json.loads(pre_login_str)
        post_data = {
            'entry': 'weibo',
            'gateway': 1,
            'from': '',
            'savestate': 7,
            'userticket': 1,
            'ssosimplelogin': 1,
            'su': base64.b64encode(requests.utils.quote(username).encode('utf-8'),self.WBCLIENT),
            'service': 'miniblog',
            'servertime': pre_login['servertime'],
            'nonce': pre_login['nonce'],
            'vsnf': 1,
            'vsnval': '',
            'pwencode': 'rsa2',
            'sp': self._get_pwd(pwd, pre_login['pubkey'], pre_login['servertime'], pre_login['nonce']),
            'rsakv': pre_login['rsakv'],
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
                   'naSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        resp = self.session.post(
            'http://login.sina.com.cn/sso/login.php?client=%s' % self.WBCLIENT,
            data=post_data,
            # header=self.user_agent
        )
        # print res.text
        login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']', resp.text).group(1)
        self.session.get(login_url)
        response = self.session.get("http://weibo.com")
        return self.session

if __name__ == '__main__':
    pass

