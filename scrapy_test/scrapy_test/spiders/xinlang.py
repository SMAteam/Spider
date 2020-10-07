import scrapy
import os
import json
import re
import random
import copy
import datetime
from urllib import parse
class XinlangSpider(scrapy.Spider):
    name = 'xinlang'
    def __init__(self,keyword,range,date_time_begin,date_time_end,task_id):
        # self.allowed_domains = ['search.sina.com.cn']
        self.start_urls = ['https://search.sina.com.cn/']
        self.keyword = parse.quote(keyword)
        self.range = range
        self.task_id = task_id
        with open(os.path.join(os.path.dirname(os.getcwd()), "scrapy_monitor", "cookie.json"), 'r') as f:
            self.cookies_list = json.load(f)
            print(self.cookies_list)
        self.date_time_begin = datetime.datetime.strptime(date_time_begin, '%Y-%m-%d-%H')
        self.date_time_end = datetime.datetime.strptime(date_time_end, '%Y-%m-%d-%H')
        self.days = (self.date_time_end - self.date_time_begin).days
        self.seconds = (self.date_time_end - self.date_time_begin).seconds
        self.time_sub = None
        if self.seconds % 3600 != 0:
            self.time_sub = self.seconds / 3600 + 1 + self.days * 24
        else:
            self.time_sub = self.seconds / 3600 + self.days * 24
        self.url = 'http://search.sina.com.cn/?q='+self.keyword+'&size=20&num=20&col=1_3&c=news&range='+self.range
    def start_requests(self):
        # 数据爬取，按小时爬取
        for hour in range(int(self.time_sub)):
            url = self.url
            begin_time = self.date_time_begin + datetime.timedelta(hours=hour)
            end_time = begin_time + datetime.timedelta(hours=1)
            begin_time_1 = begin_time.strftime('%Y-%m-%d')
            begin_time_2 = begin_time.strftime('%H:00:00')
            end_time_1 = end_time.strftime('%Y-%m-%d')
            end_time_2 = end_time.strftime('%H:00:00')
            # 要爬的微博时间段
            weibo_time = '&stime='+begin_time_1+'%20'+begin_time_2+'&etime='+end_time_1+'%20'+end_time_2
            url = url + weibo_time
            print("下一小时的帖子：",url)
            lenth = len(self.cookies_list) - 1
            i = random.randint(0, lenth)
            cookies = self.cookies_list[i]
            print(cookies)
            yield scrapy.Request(url=url,callback=self.parse_page,cookies=cookies,meta={'url':copy.deepcopy(url),'cookies':copy.deepcopy(cookies)})
    def parse(self, response):
        item = {}
        Li_list = response.xpath('//div[@class="box-result clearfix"]')
        for li in Li_list:
            item['task_id']=self.task_id
            #标题
            li_title = li.xpath('.//h2/a')
            post_url = li.xpath('.//h2/a/@href').extract_first()
            item['post_id'] = re.findall('sina.com.cn/article_([\w]+).html',post_url)
            if(item['post_id']==[]):
                item['post_id'] = re.findall('/([\w-]+).shtml',post_url)
            if(item['post_id']==[]):
                item['post_id'].append(post_url)
            item['post_id'] = item['post_id'][0]
            print('这是转发的id',item['post_id'])
            item['title'] = li_title.xpath('string(.)').extract_first()
            #作者和日期
            tmp = li.xpath('.//h2/span/text()').extract_first().strip()
            li_tmp=tmp.split(' ',1)
            item['author'] = li_tmp[0]
            item['date'] = li_tmp[1]
            #简单介绍
            li_brief = li.xpath('.//p[@class="content"]')
            item['brief'] = li_brief.xpath('string(.)').extract_first().strip()
            # item['brief'] = item['brief'].replace(" ",",")
            item['brief'] = re.sub(' {1,}',',',item['brief'])
            #详细内容链接
            detail_link =li.xpath('.//h2/a/@href').extract_first()
            item["detail_link"] = detail_link
            # print("作者:",item['author'])
            # print("发布时间:",item['date'])
            # print("标题:",item['title'])
            # print("简介：",item['brief'])
            # print(detail_link)
            # print(item)
            yield scrapy.Request(url=detail_link,callback=self.parse_detail,meta={'item':copy.deepcopy(item)})
        pass
    def parse_page(self,response):
        url = response.meta['url']
        if(response.xpath('//div[@class="pagebox"]/b/span/text()').extract_first()==None):
            print("所有的页都找到了，翻页结束")
        else:
            page = int(response.xpath('//div[@class="pagebox"]/b/span/text()').extract_first())
            next_page = str(page+1)
            next_list=response.xpath('//div[@class="pagebox"]/a/text()').extract()
            if(len(next_list)>1 and next_list[-1]=='下一页'):
                next_url =url+'&page='+next_page
                print("下一页"+next_url)
                yield scrapy.Request(url=next_url,callback=self.parse_page,meta={'url':copy.deepcopy(url)},dont_filter=True)
                print(next_list[-1])
            cur_url = url+'&page='+str(page)
            print('第',page,'页：',cur_url)
            yield scrapy.Request(url=cur_url,callback=self.parse)

    def parse_detail(self,response):
        item = response.meta['item']
        item['content'] = []
        Li_List = response.xpath('//div[@id="article"]/p')
        if(Li_List==[]):
            Li_List = response.xpath('//div[@class="article"]/p')
        if (Li_List == []):
            Li_List = response.xpath('//div[@class="article-body main-body"]/p')
        if (Li_List == []):
            Li_List = response.xpath('//div[@class="mainBody"]/p')
        for li in Li_List:
            content = li.xpath('string(.)').extract_first().strip()
            if (content!=''):
                item['content'].append(content)
        yield item


