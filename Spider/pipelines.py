# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys

import MySQLdb

import settings


# Write item to mysql
class ScrapyWeiboPipeline(object):
    def __init__(self):
        self.sql = settings.SQL_PATH
        try:
            self.db = MySQLdb.connect(settings.MYSQL_HOST, settings.USER_NAME, settings.PASSWORD, settings.DATABASE,
                                      charset="utf8")
            self.cursor = self.db.cursor()
        except MySQLdb.Error, e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "File \"%s\", line %s. \n MySQL Error:%s" % (exc_traceback.tb_frame.f_code.co_filename,
                                                               exc_traceback.tb_lineno, e)

        # Execute sql file
        for line in open(self.sql, 'r'):
            try:
                self.cursor.execute(line)
            except (AttributeError, MySQLdb.Error), e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print "File \"%s\", line %s.\n MySql Error:%s" % (exc_traceback.tb_frame.f_code.co_filename,
                                                                  exc_traceback.tb_lineno, e)

    def process_item(self, item, spider):
        self._insert(item)
        return item

    def _insert(self, item):
        """
        Insert a WeiboItem into table in database
        :param item: WeiboItem
        :return: None
        """
        content = item['content'].encode("utf-8")
        sql = u"INSERT INTO sina.feed(author_id, content, replies, retweets) VALUES(%s, %s, %s, %s)"
        try:
            self.cursor.execute(sql, (item['uid'], content, item['replies'], item['retweets']))
            self.db.commit()
        except (AttributeError, MySQLdb.Error), e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "File \"%s\", line %s.\n MySql Error:%s" % (exc_traceback.tb_frame.f_code.co_filename,
                                                              exc_traceback.tb_lineno, e)
