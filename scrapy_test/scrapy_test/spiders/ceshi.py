from html.parser import HTMLParser
import re
from django.db import connection
import scrapy
import os
import json
import copy
from ..items import UserItem
from urllib import parse
class CeshiSpider(scrapy.Spider):
    name = 'ceshi'
    # allowed_domains = ['baidu.com']
    # start_urls = ['https://www.baidu.com']
    def start_requests(self):
        with open(os.path.join(os.path.dirname(os.getcwd()), "scrapy_monitor", "cookie.json"), 'r') as f:
            cookies = json.load(f)
        # cursor = connection.cursor()
        # sql = 'select distinct(user_id) from weibo_post  where post_time >= "2020-01-01" and post_time <= "2020-02-01" limit 1000;'
        # cursor.execute(sql)
        # id_list = cursor.fetchall()
        # for id in id_list:
        #     user_id = id[0]
        #     # print(user_id)
        #     surl = 'https://weibo.com/p/100505'+user_id+'/home?from=page_100505&mod=TAB&is_hot=1#place'
        #     yield scrapy.Request(url=surl, callback=self.parse, cookies=cookies,meta={'user_id': copy.deepcopy(user_id)})

        # connection
        # surl = 'https://weibo.com/p/1005056510600179/home?from=page_100505&mod=TAB&is_hot=1&sudaref=s.weibo.com&display=0&retcode=6102'
        # surl = 'https://weibo.com/p/1005051839236994/home?from=page_100505&mod=TAB&is_hot=1#place'
        # surl = 'https://weibo.com/p/1005051770380370/home?from=page_100505&mod=TAB&is_hot=1#place'
        # surl = 'https://weibo.com/p/1005051665002772/home?from=page_100505&mod=TAB&is_hot=1#place'  #达人
        # surl = 'https://weibo.com/p/1005051665002772/home?from=page_100505&mod=TAB&is_hot=1#place'  #认证
        # surl = 'https://weibo.com/p/1005056938710690/home?from=page_100505&mod=TAB&is_hot=1#place'  #个人
        # surl = 'https://weibo.com/p/1005051469679623/home?from=page_100505&mod=TAB&is_hot=1#place'  #会员
        surl = 'https://weibo.com/p/1005051657882362/home?from=page_100505&mod=TAB&is_hot=1#place'  #其他
        user_id = 3
        yield scrapy.Request(url=surl, callback=self.parse, cookies=cookies, meta={'user_id': copy.deepcopy(user_id)})

    def parse(self, response):
        # print("到达这个网页")
        user_id = response.meta['user_id']
        # html = response.body.decode('utf-8')
        html = response.body.decode(response.encoding)
        # html= str(html)
        # print(html)
        html = html.replace('\\t', '').replace('\\n', '').replace('\\r', '').replace(' ', '').replace('', '')
        try:
            user_name = re.findall(r'class=\\"username\\">([a-zA-Z0-9\u4e00-\u9fff_·-]+)<',html)[0]
        except:
            user_name = '-100'
        if(re.findall("W_icon_co3icon_verify_co_v", html)!=[]):
            authentication = '1'
            # print("这个微博机构认证")
        elif(re.findall("W_iconicon_verify_v",html)!=[]):
            authentication = '2'
            # print("这个微博个人认证")
        elif(re.findall("daren",html)!=[]):
            authentication = '3'
            # print("这个是微博达人")
        elif(re.findall("W_iconicon_member",html)!=[]):
            authentication = '4'
            # print("会员")
        else:
            authentication = '5'
            # print("个人")
        try:
            location = re.findall(r'<spanclass=\\"item_icoW_fl\\"><emclass=\\"W_ficonficon_cd_placeS_ficon\\">2<\\/em><\\/span><spanclass=\\"item_textW_fl\\">([\u4e00-\u9fff]+)<',html)[0]
            if authentication == '1':
                province = '-100'
                city = '-100'
            else:
                lenth = len(location)
                if (len(location) > 3):
                    if ('内蒙古' in location or '黑龙江' in location):
                        province = location[0:3]
                        city = location[3:lenth]
                        print('省:' + province + '市:' + city)
                    else:
                        province = location[0:2]
                        city = location[2:lenth]
                        print('省:' + province + '市:' + city)
                else:
                    if ('内蒙古' in location or '黑龙江' in location):
                        province = location[0:3]
                        city = '-100'
                        print('省:' + province)
                    else:
                        province = location[0:2]
                        print('省:' + province)
                        city = '-100'
        except:
            province = '-100'
            city = '-100'
        try:
            interest = re.findall(r'>(\d+)<\\/strong><spanclass=\\"S_txt2\\">关注<\\/span>', html)
            if interest == []:
                interest = re.findall(r'的关注\((\d+)\)', html)[0]
            else:
                interest = interest[0]
            if interest == []:
                interest =-100
            interest = int(interest)
        except:
            interest = -100
        try:
            fans = re.findall(r'>(\d+)<\\/strong><spanclass=\\"S_txt2\\">粉丝<\\/span>', html)
            if fans == []:
                fans = re.findall(r'的粉丝\((\d+)\)', html)[0]
            else:
                fans = fans[0]
            if fans == []:
                fans = -100
            fans = int(fans)
        except:
            fans = -100
        try:
            weibo_num =re.findall(r'>(\d+)<\\/strong><spanclass=\\"S_txt2\\">微博<\\/span>', html)[0]
            weibo_num = int(weibo_num)
        except:
            weibo_num = -100
        # item = UserItem()
        # item['user_id'] = user_id
        # item['user_name'] = user_name
        # item['province'] = province
        # item['city'] = city
        # item['authentication'] = authentication
        # item['fans'] = fans
        # item['interest'] =interest
        # item['weibo_num'] = weibo_num
        # try:
        #     item.save()
        # except:
        #     pass
        print(user_name,user_id,authentication,province,city,interest,weibo_num,fans)
        return
