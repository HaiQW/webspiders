# -*- coding: utf-8 -*-
import re
import urllib

import scrapy
import requests
from scrapy.http import Request

from Spider.sina.weibo import weibo
from Spider.items import WeiboItem, ParamItem


# from pyquery import PyQuery as pq
# from scrapy.contrib.linkextractors import LinkExtractor

class Weibo(scrapy.Spider):
    name = 'weibo'
    weibo = weibo()
    session = weibo.login('15557106533', 'wenghaiqin')
    allowed_domains = ['weibo.com']
    start_urls = ["http://weibo.com/3856926178/home?wvr=5"]
    cookiejar = requests.utils.dict_from_cookiejar(session.cookies)
    cookie = {'ALF': cookiejar['ALF'],
              'sso_info': cookiejar['sso_info'],
              'SUB': cookiejar['SUB'],
              'SUBP': cookiejar['SUBP'],
              'SUE': cookiejar['SUE'],
              'SUHB': cookiejar['SUHB'],
              'SUP': cookiejar['SUP'],
              'SUS': cookiejar['SUS']}
    param = ParamItem(name='', weibo_num='20', fellowing_num='', fellower_num='')

    def start_requests(self):
        uid = 1246531434
        params = {'page': 1, 'section': 1, 'uid': 1246531434, 'start': '2015-03-15', 'end': '2015-06-15'}
        urls = self._get_weibo_url(1246531434, 23)

        # Parse weibo homepage
        home_url = "http://weibo.cn/u/%s" % uid
        yield Request(url=home_url, cookies=self.cookie, callback=self._parse_homepage, errback=self._parse_fail)

        # Parse weibo content
        weibo_num = self.param['weibo_num']
        for page in range(0, (int(weibo_num)) / 10 + 1):
            content_url = "http://weibo.cn/%s/profile?page=%s" % (uid, page + 1)
            yield Request(url=content_url.encode("utf-8"), meta={'uid': 3856926178}, cookies=self.cookie,
                          callback=self._parse_weibo_content, errback=self._parse_fail)

    def _parse_homepage(self, response):
        """
        Parse the home page of user's weibo and get some parameters
        :param response: Http response
        :return: Some parameter
        """
        print 'Parse weibo homepage.'
        user_name = response.xpath('//div[@class="ut"]/text()').extract()
        param = response.xpath('//div[@class="tip2"]/a/text()').extract()
        param = re.findall(u'\d+', "".join(param).decode("utf-8"))
        self.param = ParamItem(name=user_name[0], weibo_num=param[0], fellowing_num=param[1], fellower_num=param[2])

    def _parse_weibo_content(self, response):
        """
        Parse the home page html and get some important parameter.
        :param response: http response
        :return: a list of parameters
        """
        print "parse weibo content."
        uid = str(response.meta['uid']).decode("utf-8")
        contents = response.xpath('//div[@class="c"]/div/span[@class="ctt"]').extract()
        feeds = response.xpath('//div[@class="c"]/div[last()]').extract()  # last():the last elements

        # parse the weibo content
        contents_array = []
        for content in contents:
            p = re.compile(u'<[^>]+>')  # Filter html tag
            weibo_content = p.sub("", content)
            contents_array.append(weibo_content)

        # Get the number of good, retweet and reply
        feeds_array = []
        for feed in feeds:
            good = re.search(u"赞\[\d+\]", feed.decode("utf-8"))
            retweet = re.search(u"转发\[\d+", feed.decode("utf-8"))
            reply = re.search(u"评论\[\d+", feed.decode("utf-8"))
            if retweet and good and reply:
                p = re.compile(u"\d+")
                retweet_num = p.search(retweet.group(0).decode("utf-8")).group(0)
                good_num = p.search(good.group(0).decode("utf-8")).group(0)
                reply_num = p.search(reply.group(0).decode("utf-8")).group(0)
                feeds_array.append([reply_num, retweet_num, good_num])

        # Pipeline item
        if len(contents_array) == len(feeds_array):
            for i in range(0, len(contents_array)):
                weibo_item = WeiboItem()
                weibo_item['retweets'] = feeds_array[i][1]
                weibo_item['replies'] = feeds_array[i][0]
                weibo_item['goods'] = feeds_array[i][2]
                weibo_item['content'] = contents_array[i]
                weibo_item['uid'] = uid
                yield weibo_item

    # def parse_weibo(self, response):
    #     params = response
    #     sel = Selector(response)
    #     weibo_content = response.selector.xpath('//div[@class="c"]/div/span/text()').extract()
    #     for item in weibo_content:
    #         item = item.encode("utf-8")
    #         try:
    #             cursor = self.db.cursor()
    #             sql = u" INSERT INTO weibo(contant) VALUES(%s)"
    #             temp = item.decode("utf-8")
    #             cursor.execute(sql, item)
    #             chinese = u"[\u4e00-\u9fa5]+"
    #             pattern = re.compile(chinese)
    #             all = pattern.findall(temp)
    #             for i in all:
    #                 print i.encode("utf-8")
    #             self.db.commit()
    #         except:
    #             print "Could not insert an item into mysql."

    def _parse_photo(self, response):
        photo_url = response.xpath('//a[contains(@href, "album")]/img/@src').extract()
        i = 10
        for photo in photo_url:
            photo = photo.encode('utf-8').replace("square", "large")
            conn = urllib.urlopen(photo)
            f = open("lady_professor/pic_" + str(i) + ".jpg", 'wb')
            i = i + 1
            f.write(conn.read())
            # print conn.body
            f.close()

            print photo

    def _get_weibo_url(self, pid, page):
        search_url = []
        url = 'http://weibo.cn/%s/profile?page=%s'
        for i in range(0, page):
            search_url.append(url % (pid, i + 1))
        return search_url

    def get_albums_url(self, pid, page):
        albums_url = 'http://photo.weibo.com/%s/talbum/index#!/mode/1/page/%s'
        return albums_url % (pid, page)

    def _parse_fail(self, response):
        print "fail to crawl from weibo."

    def process_request(self, request):
        request = request.replace(**{'cookies': self.cookie})
        return request

    def _parse_friend_pid(self, response):
        """
        Get friends' pid from the login page
        :param response: http response
        :return: list
        """
        uid_url = response.xpath('//td[contains(@valign, "top")]/a[contains(@href, "del?uid=")]/@href').extract()
        user_name = response.xpath('//td[contains(@valign, "top")]/a[contains(@href, "http://weibo.cn")][1]/text()') \
            .extract()
        if len(uid_url) == len(user_name):
            for i in range(0, len(user_name)):
                uid = re.search("\d+", uid_url[i]).group(0)
                name = user_name[i]
                url = "http://weibo.cn/u/%s" % uid  # Reform the home page url using uid
                # Parse the home page of friends's content
                print uid, name, url
        else:
            print "error in parse uid."
