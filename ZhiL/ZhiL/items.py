# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = scrapy.Field()
    address = scrapy.Field()
    company_name = scrapy.Field()
    salary = scrapy.Field()
    time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                          insert into job(job_name, address, company, salary, publish)
                          VALUES (%s,%s,%s,%s,%s)
 
                    """
        params = (
                    self['job_name'], self['address'], self['company_name'], self['salary'],
                    self['time']
                )
        return insert_sql, params

