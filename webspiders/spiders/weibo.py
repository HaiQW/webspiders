# -*- coding: utf-8 -*-
import re
import urllib
import time
import requests

from scrapy.http import Request
from scrapy import log
from scrapy.spider import Spider
from webspiders.utils.weibo import weibo
from webspiders.items import WeiboItem, ParamItem

class Weibo(Spider):
    name = 'weibo'
    def __init__(self, name, password, uid, *args, **kwargs):
        super(Weibo, self).__init__(*args, **kwargs)
        self.uid = uid
        self.start_urls = ["http://weibo.com"]
        self.allowed_domains = ["weibo.com"]
        self.weibo = weibo()
        self.session = self.weibo.login(name, password)
        cookiejar = requests.utils.dict_from_cookiejar(self.session.cookies)
        print cookiejar
        # Set sina weibo cookie
        self.cookie = {'ALF': cookiejar['ALF'],
                       'sso_info': cookiejar['sso_info'],
                       'SUB': cookiejar['SUB'],
                       'SUBP': cookiejar['SUBP'],
                       'SUE': cookiejar['SUE'],
                       'SUHB': cookiejar['SUHB'],
                       'SUP': cookiejar['SUP'],
                       'SUS': cookiejar['SUS']}

    def start_requests(self):
        # Parse weibo homepage
        home_url = "http://weibo.cn/u/%s" % self.uid
        yield Request(url=home_url, cookies=self.cookie, callback=self._parse_homepage, errback=self._parse_fail)

    def _parse_homepage(self, response):
        """
        Parse the home page of user's weibo and get some parameters
        :param response: Http response
        :return: Some parameter
        """
        print ('Parse weibo homepage.')
        user_name = response.xpath('//div[@class="ut"]/text()').extract()
        param = response.xpath('//div[@class="tip2"]/a/text()').extract()
        param = re.findall(u'\d+', "".join(param).encode("utf-8"))
        item = ParamItem(name=user_name[0], weibo_num=param[0], fellowing_num=param[1], fellower_num=param[2])

        print ('Parse weibo content.')
        weibo_num = param[0]
        print (weibo_num)
        for page in range(0, (int(weibo_num))/10 + 1):
            content_url = "http://weibo.cn/%s/profile?page=%s" % (self.uid, page + 1)
            yield Request(url=content_url.encode("utf-8"), meta={'uid': self.uid}, cookies=self.cookie,
                          dont_filter=True, callback=self._parse_weibo_content, errback=self._parse_fail)

    def _parse_weibo_content(self, response):
        """
        Parse the home page html and get some important parameter.
        :param response: http response
        :return: a list of parameters
        """
        print ("parse weibo content.")
        uid = str(response.meta['uid']).encode("utf-8")
        contents = response.xpath('//div[@class="c"]/div/span[@class="ctt"]').extract()
        feeds = response.xpath('//div[@class="c"]/div[last()]').extract()  # last():the last elements

        # parse the weibo content
        contents_array = []
        for content in contents:
            p = re.compile(u'<[^>]+>')  # Filter html tag
            weibo_content = p.sub("", content)
            contents_array.append(weibo_content)

        # Get the number of good, retweet and reply. Get data time.
        feeds_array = []
        for feed in feeds:
            good = re.search(u"赞\[\d+\]", feed.encode("utf-8"))
            retweet = re.search(u"转发\[\d+", feed.encode("utf-8"))
            reply = re.search(u"评论\[\d+", feed.encode("utf-8"))
            data_time = re.search(u"\d+-\d+-\d+ \d+:\d+:\d+|\d+分钟前|\d+月\d+日 \d+:\d+|今天 \d+:\d+", feed.encode("utf-8"))

            # Format data time
            data_type = "".join(re.findall(u"[\u4e00-\u9fa5]+", data_time.group(0)))
            if data_type.encode("utf-8") == u"今天":
                data_time = data_time.group(0).replace(u"今天 ", "")
                cur_time = time.localtime()
                month = str(cur_time.tm_mon/10)+str(cur_time.tm_mon-cur_time.tm_mon/10)
                data_time = "%s-%s-%s %s:%s" % (cur_time.tm_year, month, cur_time.tm_mday, data_time,
                                                cur_time.tm_sec)
            elif data_type.encode("utf-8") == u"分钟前":
                data_time = data_time.group(0).replace(u"分钟前", "")
                data_time = int(data_time)
                data_time = time.localtime(time.time()-int(data_time)*60)
                data_time = time.strftime('%Y-%m-%d %H:%M:%S', data_time)
            elif data_type.encode("utf-8") == u"月日":
                data_time = data_time.group(0).replace(u"月", "-").replace(u"日", "")
                cur_time = time.localtime()
                data_time = "%s-%s:%s" % (cur_time.tm_year, data_time, cur_time.tm_sec)
            else:
                data_time = data_time.group(0)
            print (data_time)

            # Get the number of retweet, good, reply, feed
            if retweet and good and reply:
                p = re.compile(u"\d+")
                retweet_num = p.search(retweet.group(0).encode("utf-8")).group(0)
                good_num = p.search(good.group(0).encode("utf-8")).group(0)
                reply_num = p.search(reply.group(0).encode("utf-8")).group(0)
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
        """
        Parse and download some photos
        :param response: Http response
        :return: None
        """
        photo_url = response.xpath('//a[contains(@href, "album")]/img/@src').extract()
        i = 10
        for photo in photo_url:
            photo = photo.encode('utf-8').replace("square", "large")
            conn = urllib.urlopen(photo)
            f = open("lady_professor/pic_" + str(i) + ".jpg", 'wb')
            i += 1
            f.write(conn.read())
            f.close()
            # print photo

    def _get_weibo_url(self, pid, page):
        """
        Get the weibo url to searcg
        :param pid:
        :param page:
        :return:
        """
        search_url = []
        url = 'http://weibo.cn/%s/profile?page=%s'
        for i in range(0, page):
            search_url.append(url % (pid, i + 1))
        return search_url

    def get_albums_url(self, pid, page):
        albums_url = 'http://photo.weibo.com/%s/talbum/index#!/mode/1/page/%s'
        return albums_url % (pid, page)

    def _parse_fail(self, response):
        log.err("Fail to parse the http response file.")

    # def process_request(self, request):
    #     request = request.replace(**{'cookies': self.cookie})
    #     return request

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
                print (uid, name, url)
        else:
            log.err("error in parse uid.")
