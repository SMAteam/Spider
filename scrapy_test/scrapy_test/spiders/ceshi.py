from html.parser import HTMLParser
import re
import random
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
            cookies_list = json.load(f)
            lenth = len(cookies_list) - 1
        #     i = random.randint(0, lenth)
        #     print(i)
        #     cookies = cookies_list[i]
        #     print(cookies)
        # cookies = {'_s_tentry': 'passport.weibo.com', 'wb_view_log': '800*6001', 'SINAGLOBAL': '5744165866381.79.1602054057383', 'login_sid_t': 'ba40ef8f4dc5878518d6ad5dcfbf7deb', 'Apache': '5744165866381.79.1602054057383', 'SUB': '_2AkMoIeiRf8PxqwJRmf8dzGvqb4V_ywDEieKefRlKJRMxHRl-yT9jqkogtRB6A6HGfg2pA7NdJaV89WMqcf6Q7BuSBoSm', 'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFRUji25u9IzdLXI8ADiigk', 'WBStorage': '70753a84f86f85ff|undefined', 'ULV': '1602054057394:1:1:1:5744165866381.79.1602054057383:', 'cross_origin_proto': 'SSL'}
        cursor = connection.cursor()
        sql = 'select distinct(user_id) from weibo_post  where post_time >= "2020-01-01" and post_time <= "2020-02-01";'
        cursor.execute(sql)
        id_list = cursor.fetchall()
        for id in id_list:
            user_id = str(id[0])
            # print(user_id)
            i = random.randint(0, lenth)
            print(i)
            cookies = cookies_list[i]
            surl = 'https://weibo.com/p/100505'+user_id+'/home?from=page_100505&mod=TAB&is_hot=1#place'
            yield scrapy.Request(url=surl, callback=self.parse, cookies=cookies,meta={'user_id': copy.deepcopy(user_id)})

        # connection
        # surl = 'https://weibo.com/p/1005055445373111/home?from=page_100505&mod=TAB&is_hot=1&sudaref=s.weibo.com&display=0&retcode=6102'
        # surl = 'https://weibo.com/p/1005051839236994/home?from=page_100505&mod=TAB&is_hot=1#place'
        # surl = 'https://weibo.com/p/1005051770380370/home?from=page_100505&mod=TAB&is_hot=1#place'
        # surl = 'https://weibo.com/p/1005051665002772/home?from=page_100505&mod=TAB&is_hot=1#place'  #??????
        # surl = 'https://weibo.com/p/1005051665002772/home?from=page_100505&mod=TAB&is_hot=1#place'  #??????
        # surl = 'https://weibo.com/p/1005056938710690/home?from=page_100505&mod=TAB&is_hot=1#place'  #??????
        # surl = 'https://weibo.com/p/1005051469679623/home?from=page_100505&mod=TAB&is_hot=1#place'  #??????
        #surl = 'https://weibo.com/p/1005051657882362/home?from=page_100505&mod=TAB&is_hot=1#place'  #??????
        #user_id = 3
        #yield scrapy.Request(url=surl, callback=self.parse, cookies=cookies, meta={'user_id': copy.deepcopy(user_id)})

    def parse(self, response):
        # print("??????????????????")
        user_id = response.meta['user_id']
        # html = response.body.decode('utf-8')
        html = response.body.decode(response.encoding)
        # html= str(html)
        # print(html)
        html = html.replace('\\t', '').replace('\\n', '').replace('\\r', '').replace(' ', '').replace('', '')
        try:
            user_name = re.findall(r'class=\\"username\\">([a-zA-Z0-9\u4e00-\u9fff_??-]+)<',html)[0]
        except:
            user_name = '-100'
        if(re.findall("W_icon_co3icon_verify_co_v", html)!=[]):
            authentication = '1'
            # print("????????????????????????")
        elif(re.findall("W_iconicon_verify_v",html)!=[]):
            authentication = '2'
            # print("????????????????????????")
        elif(re.findall("daren",html)!=[]):
            authentication = '3'
            # print("?????????????????????")
        elif(re.findall("W_iconicon_member",html)!=[]):
            authentication = '4'
            # print("??????")
        else:
            authentication = '5'
            # print("??????")
        try:
            location = re.findall(r'<spanclass=\\"item_icoW_fl\\"><emclass=\\"W_ficonficon_cd_placeS_ficon\\">2<\\/em><\\/span><spanclass=\\"item_textW_fl\\">([\u4e00-\u9fff]+)<',html)[0]
            if authentication == '1':
                province = '-100'
                city = '-100'
            else:
                lenth = len(location)
                if (len(location) > 3):
                    if ('?????????' in location or '?????????' in location):
                        province = location[0:3]
                        city = location[3:lenth]
                        print('???:' + province + '???:' + city)
                    else:
                        province = location[0:2]
                        city = location[2:lenth]
                        print('???:' + province + '???:' + city)
                else:
                    if ('?????????' in location or '?????????' in location):
                        province = location[0:3]
                        city = '-100'
                        print('???:' + province)
                    else:
                        province = location[0:2]
                        print('???:' + province)
                        city = '-100'
        except:
            province = '-100'
            city = '-100'
        try:
            interest = re.findall(r'>(\d+)<\\/strong><spanclass=\\"S_txt2\\">??????<\\/span>', html)
            if interest == []:
                interest = re.findall(r'?????????\((\d+)\)', html)[0]
            else:
                interest = interest[0]
            if interest == []:
                interest =-100
            interest = int(interest)
        except:
            interest = -100
        try:
            fans = re.findall(r'>(\d+)<\\/strong><spanclass=\\"S_txt2\\">??????<\\/span>', html)
            if fans == []:
                fans = re.findall(r'?????????\((\d+)\)', html)[0]
            else:
                fans = fans[0]
            if fans == []:
                fans = -100
            fans = int(fans)
        except:
            fans = -100
        try:
            weibo_num =re.findall(r'>(\d+)<\\/strong><spanclass=\\"S_txt2\\">??????<\\/span>', html)[0]
            weibo_num = int(weibo_num)
        except:
            weibo_num = -100
        item = UserItem()
        # item['user_id'] = int(user_id)
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