from html.parser import HTMLParser
import re

import scrapy
import os
import json
from urllib import parse
class CeshiSpider(scrapy.Spider):
    name = 'ceshi'
    # allowed_domains = ['baidu.com']
    # start_urls = ['https://www.baidu.com']
    def start_requests(self):
        with open(os.path.join(os.path.dirname(os.getcwd()), "scrapy_monitor", "cookie.json"), 'r') as f:
            cookies = json.load(f)
        # surl = "https://weibo.com/laoluoyonghao?refer_flag=0000015010_&from=feed&loc=nickname&is_all=1"
        # surl = 'https://weibo.com/u/1839236994?refer_flag=1001030103_&is_hot=1'
        surl = 'https://weibo.com/p/1005056510600179/home?from=page_100505&mod=TAB&is_hot=1&sudaref=s.weibo.com&display=0&retcode=6102'
        # surl ='https://weibo.com/p/1005051839236994/home?from=page_100505&mod=TAB&is_hot=1#place'
        yield scrapy.Request(url=surl,callback=self.parse,cookies=cookies)

    def parse(self, response):
        print("到达这个网页")
        # html = response.body.decode('utf-8')
        html = response.body.decode(response.encoding)
        html= str(html)
        html = html.replace('\\t','').replace('\\n','').replace('\\r','').replace(' ','').replace('','')
        print(html)
        location = re.findall(r'<spanclass=\\"item_icoW_fl\\"><emclass=\\"W_ficonficon_cd_placeS_ficon\\">2<\\/em><\\/span><spanclass=\\"item_textW_fl\\">([\u4e00-\u9fff]+)<',html)[0]
        # interest = re.findall(r'<strongclass=\\"W_f18\\">(\d+)<\\/strong><spanclass=\\"S_txt2\\">关注<\\/span>',html)[0]
        interest = re.findall(r'的关注\((\d+)\)',html)[0]
        # fans = re.findall(r'<strongclass=\\"W_f18\\">(\d+)<\\/strong><spanclass=\\"S_txt2\\">粉丝<\\/span>',html)[0]
        fans = re.findall(r'的粉丝\((\d+)\)',html)[0]
        weibo_num = re.findall(r'>(\d+)<\\/strong><spanclass=\\"S_txt2\\">微博<\\/span>',html)[0]
        # weibo_num = re.findall(r'的微博\((\d+)\)',html)[0]
        interest = int(interest)
        fans = int(fans)
        weibo_num =int(weibo_num)
        lenth = len(location)
        print(type(lenth))
        if(len(location)>2):
            if('内蒙古'in location or '黑龙江' in location):
                province = location[0:2]
                city = location[2:lenth]
                print('省:'+province+'市:'+city)
            else:
                province = location[0:2]
                city = location[2:lenth]
                print('省:'+province+'市:'+city)
        else:
            if('内蒙古'in location or '黑龙江' in location):
                province = location[0:2]
                print('省:'+province)

            else:
                province = location[0:2]
                print('省:'+province)
        print("关注数:",fans)
        print("关注数:",interest)
        print("微博数：",weibo_num)
        # body = response.body
        # print(ur)
        pass
