# -*- coding: utf-8 -*-
import scrapy
from ZhiL import items

class ZhilianSpider(scrapy.Spider):
    name = 'ZhiLian'
    allowed_domains = ['jobs.zhaopin.com']
    start_urls = ['http://jobs.zhaopin.com/']

    def parse(self, response):
        job_urls = response.xpath("//div[@class='listcon']/a/@href").extract()
        for job_url in job_urls:
            job_url = response.urljoin(job_url)
            yield scrapy.Request(url=job_url, callback=self.second_parse)

    def second_parse(self, response):
        is404 = response.xpath("//p[@class='error-content__text']/text()").extract_first()
        if '对不起，您要访问的页面暂时没有找到' == is404:
            return None
        else:
            next_page = response.xpath("//span[@class='search_page_next']/a/@href").extract_first()
            next_page_url =response.urljoin(next_page)
            job_name = response.xpath("//span[@class='post']/a/text()").extract()
            company_name = response.xpath("//span[@class='company_name']/a/text()").extract()
            salary = response.xpath("//span[@class='salary']/text()").extract()
            address = response.xpath("//span[@class='address']/a/text()").extract()
            publish_time = response.xpath("//span[@class='release_time']/text()").extract()
            num = len(job_name)
            item = items.ZhilItem()
            for i in range(num):
                item["job_name"] = job_name[i].strip('')
                item["company_name"] = company_name[i].strip('')
                item["salary"] = salary[i].strip('')
                item["address"] = address[i].strip('')
                item["time"] = publish_time[i].strip('')
                yield item
            yield scrapy.Request(url=next_page_url, callback=self.second_parse)





