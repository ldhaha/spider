# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors


class ZhilPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbpool = adbapi.ConnectionPool("pymysql", host=settings["MYSQL_HOST"], db=settings["MYSQL_DBNAME"],
                                       user=settings["MYSQL_USER"], password=settings["MYSQL_PASSWORD"], charset="utf8",
                                       cursorclass=pymysql.cursors.DictCursor,
                                        use_unicode = True)
        return cls(dbpool)

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.do_insert, item)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

