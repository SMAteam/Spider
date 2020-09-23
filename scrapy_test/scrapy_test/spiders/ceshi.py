import scrapy
import os
import json
from urllib import parse
class CeshiSpider(scrapy.Spider):
    name = 'ceshi'
    # allowed_domains = ['baidu.com']
    start_urls = ['https://www.baidu.com']
    def start_requests(self):
        with open(os.path.join(os.path.dirname(os.getcwd()), "scrapy_monitor", "cookie.json"), 'r') as f:
            cookies = json.load(f)
        # surl = "https://weibo.com/laoluoyonghao?refer_flag=0000015010_&from=feed&loc=nickname&is_all=1"
        surl = 'https://weibo.com/1977459170/info?sudaref=s.weibo.com&display=0&retcode=6102'
        yield scrapy.Request(url=surl,callback=self.parse,cookies=cookies)

    def parse(self, response):
        print("到达这个网页")
        ur = response.xpath('.//title/text()').extract()
        print(ur)
        pass
