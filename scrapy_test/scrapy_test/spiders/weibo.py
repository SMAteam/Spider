# -*- coding: utf-8 -*-
import os

import scrapy
import json
import base64
import requests
import datetime
from urllib import parse
from data_model.models import weibo_user
from ..items import PostItem,UserItem
import logging
import re
import random
import emoji
import time
class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    def __init__(self,date_time_begin,date_time_end,keyword,xsort,scope,vip,category,task_id):
        self.allowed_domains = ['weibo.com']
        self.start_urls = ['http://weibo.com/']
        # self.cookies=cookies
        with open(os.path.join(os.path.dirname(os.getcwd()),"scrapy_monitor","cookie.json"),'r') as f:
            self.cookies_list = json.load(f)
            # print(self.cookies)
        self.date_time_begin = datetime.datetime.strptime(date_time_begin, '%Y-%m-%d-%H')
        self.date_time_end = datetime.datetime.strptime(date_time_end, '%Y-%m-%d-%H')
        self.days = (self.date_time_end - self.date_time_begin).days
        self.seconds = (self.date_time_end - self.date_time_begin).seconds
        self.time_sub = None
        if self.seconds%3600!=0:
            self.time_sub = self.seconds / 3600 + 1 + self.days * 24
        else:
            self.time_sub = self.seconds/3600+self.days*24
        self.keyword = parse.quote(keyword)
        self.xsort = int(xsort)  # 热门
        self.scope = int(scope)  # 原创
        self.vip = int(vip)  # 认证用户
        self.category = int(category)  # 媒体
        self.task_id = task_id
    def start_requests(self): #可以省略，但是一定要有parse函数
        # 数据爬取，按小时爬取
        for hour in range(int(self.time_sub)):
            begin_time = self.date_time_begin + datetime.timedelta(hours=hour)
            end_time = begin_time + datetime.timedelta(hours=1)
            begin_time = begin_time.strftime('%Y-%m-%d-%H')
            end_time = end_time.strftime('%Y-%m-%d-%H')
            # 要爬的微博时间段
            weibo_time = begin_time + ':' + end_time
            # 获取微博页数
            url = 'https://s.weibo.com/weibo?q=' + self.keyword
            if self.xsort:
                url = url + '&xsort=hot'
            if self.scope:
                url = url + '&scope=ori'
            if self.vip:
                url = url + '&vip=1'
            if self.category:
                url = url + '&category=4'
            url = url + '&suball=1&Refer=SWeibo_box&timescope=custom:' + weibo_time  # 热门微博
            print("下一小时的帖子:", url)
            lenth = len(self.cookies_list) - 1
            i = random.randint(0, lenth)
            cookies = self.cookies_list[i]
            print(cookies)
            yield scrapy.Request(url=url,callback=self.parse,cookies=cookies,meta={'weibo_time':weibo_time,'cookies':cookies})
    def parse(self, response):
        if response.xpath('.').re(f'抱歉，未找到'):
            print('没结果')
            return
        #查找微博页数
        page_num = response.xpath('//*[@id="pl_feedlist_index"]/div[3]/@class').extract_first()
        if page_num=='m-page':
            page_num = int(response.xpath('//*[@id="pl_feedlist_index"]/div[3]/div/span/ul/li[last()]/a/text()').re(r'第(.*?)页')[0])+1
        else:
            page_num = 1
        print('页数',page_num)
        for page in range(1, page_num + 1):
            time.sleep(1.5)
            url = 'https://s.weibo.com/weibo?q=' + self.keyword
            if self.xsort:
                url = url + '&xsort=hot'
            if self.scope:
                url = url + '&scope=ori'
            if self.vip:
                url = url + '&vip=1'
            if self.category:
                url = url + '&category=4'
            url = url + '&timescope=custom:'+response.meta['weibo_time'] + '&Refer=SWeibo_box&page=' + str(page)
            print("下一页的帖子:", page,url)
            yield scrapy.Request(url=url,callback=self.post_extract,cookies=response.meta['cookies'],meta={'weibo_time':response.meta['weibo_time'],'url':url,'cookies':response.meta['cookies']})
    def post_extract(self, response):
        # user识别
        user_re = re.compile(r'@.*')
        # 话题识别
        topic_re = re.compile(r'#.*#')
        #web_data = web_data.replace('\u200b', '')
        #web_data = web_data.replace('&#xe627;', '#S')
        # 找出所有微博
        posts = response.xpath('.//*[@id="pl_feedlist_index"]/div[2]/div')
        for (c, post) in enumerate(posts):
            # 用户信息详细链接网址
            user_url = None
            # 获取post_id
            post_id = None
            # 用户ID
            user_id = None
            # 粉丝数
            fans_num = None
            authentication_text = []
            # 转发数
            forward_num = 0
            # 评论数
            comment_num = 0
            # 点赞数
            like_num = 0
            # 发帖时间
            post_time = None
            # 原帖信息
            original_content = None
            # 匹配card-act,点赞转发评论
            bottom = post.xpath('./div/div[2]//li//text()').extract()
            num_re = re.compile('\d+')
            if num_re.search(bottom[1]):
                forward_num = int(num_re.search(bottom[1]).group())
            if num_re.search(bottom[2]):
                comment_num = int(num_re.search(bottom[2]).group())
            if num_re.search(bottom[-1]):
                like_num = int(num_re.search(bottom[-1]).group())
            authentication_text = post.xpath('.//*[@class="info"]//a/@title').extract()
            post_name = post.xpath('.//div[@class="content"]/div//a[@class="name"]/text()').extract_first()
            if authentication_text == []:
                authentication_text.append('其他用户')
            if '微博官方认证' in authentication_text:
                authentication = '1'
            elif '微博个人认证' in authentication_text:
                authentication = '2'
            elif '微博达人' in authentication_text:
                authentication = '3'
            elif '微博会员' in authentication_text:
                authentication = '4'
            else:
                authentication = '5'
            # 发帖user_id和post_id
            try:
                #提取帖子发布时间
                post_time = post.xpath('.//div[@class="content"]/p[@class="from"]/a[1]/text()').extract_first()
                #x分钟前
                user_url = post.xpath('.//div[@class="content"]/div[@class="info"]//a[@class="name"]/@href').extract_first()
                if re.search('(\d+)分钟前',post_time)!=None:
                    minutes = int(re.search('(\d+)分钟前', post_time).group(1))
                    post_time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
                    post_time = post_time.strftime("%Y-%m-%d %H:%M:%S")
                #x秒
                elif re.search('(\d+)秒前',post_time)!=None:
                    seconds = int(re.search('(\d+)秒前', post_time).group(1))
                    post_time = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
                    post_time = post_time.strftime("%Y-%m-%d %H:%M:%S")
                elif re.search("今天", post_time)!=None:
                    post_year = datetime.datetime.now().year
                    post_month = datetime.datetime.now().month
                    post_day = datetime.datetime.now().day
                    post_hour = re.search(r"(\d+):", post_time).group(1)
                    post_minute = re.search(r":(\d+)", post_time).group(1)
                    post_time = "{}-{}-{}-{}-{}".format(post_year, post_month, post_day, post_hour, post_minute)
                    post_time = datetime.datetime.strptime(post_time, "%Y-%m-%d-%H-%M")
                    post_time = post_time.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    post_time = re.sub('\s+','', post_time)
                    post_year = int(response.meta['weibo_time'].split('-')[0])
                    if re.match(r"年", post_time):
                        post_year = re.search(r"(\d+)年", post_time).group(1)
                    post_month = re.search(r"(\d+)月", post_time).group(1)
                    post_day = re.search(r"(\d+)日", post_time).group(1)
                    post_hour = re.search(r"(\d+):", post_time).group(1)
                    post_minute = re.search(r":(\d+)", post_time).group(1)
                    post_time = "{}-{}-{}-{}-{}".format(post_year, post_month, post_day, post_hour, post_minute)
                    post_time = datetime.datetime.strptime(post_time, "%Y-%m-%d-%H-%M")
                    post_time = post_time.strftime("%Y-%m-%d %H:%M:%S")
                # 当前帖子处理
                # 帖子链接
                original_post_url = post.xpath('.//div[@class="content"]/p[@class="from"]/a[1]/@href').extract_first()
                user_id = re.search(r'/(\d+)/', original_post_url).group(1)
                if(weibo_user.objects.filter(user_id=user_id).exists()==False):
                    print("添加新用户")
                    if user_id != None:
                        user_url = 'https://weibo.com/p/100505'+user_id+'/home?from=page_100505&mod=TAB&is_hot=1#place'
                        yield scrapy.Request(url=user_url, callback=self.user_extract,cookies= response.meta['cookies'], meta={'authentication': authentication,'user_id':user_id,'post_name':post_name})
                else:
                    print("用户已存在")
                post_id = re.search(r'/([a-zA-Z0-9]+)\?', original_post_url).group(1)

                content = post.xpath('.//div[@class="content"]')
                original_content_ele = content[0].xpath('./p[@class="txt"][last()]')  # [-1]
                # 帖子内容
                original_content = ''.join(original_content_ele.xpath('.//text()').extract())
                original_content = re.sub('\s+|收起全文d', '', original_content)
                # original_content = re.sub(r"收起全文d", '', original_content)
                # logging.info(f"{original_content}")
                # 匹配帖子中的链接，包含@的用户，话题链接等
                post_a = original_content_ele.xpath('.//a')
                for v in post_a:
                    post_url = str(v.xpath('./@href').extract_first())
                    post_url_value = v.xpath('.//text()').extract()
                    post_url_value = ''.join(post_url_value)
                    # 实体为用户
                    if user_re.match(post_url_value):
                        # print('<@>'+post_url_value+":"+post_url+'<@>')
                        original_content = original_content.replace('//' + post_url_value,
                                                                        '<@>' + post_url_value + ":" + post_url + '</@>')
                        # print(original_content)
                    # 实体为话题
                    elif topic_re.match(post_url_value):
                        original_content = original_content.replace(post_url_value,
                                                                        '<#>' + post_url_value + '</#>')
                    else:
                        original_content = original_content.replace(post_url_value,
                                                                        '<u>' + post_url_value + ":" + post_url + '</u>')
                #logging.info(f"{original_content}")
            except Exception:
                logging.error(Exception)
                logging.error("原帖{}出现问题url:{}".format(c,response.meta['url']))
            else:
                # 查看是否有转贴
                # 转贴repost_id,repost_user_id
                re_post_url = post.xpath('.//div[@class="content"]//div[@class="con"]//div[@class="func"]/p[@class="from"]/a[1]/@href').extract_first()
                if re_post_url!= None:  # 有转贴信息
                    try:
                        # 转发数
                        repost_forward_num = 0
                        # 评论数
                        repost_comment_num = 0
                        # 点赞数
                        repost_like_num = 0
                        # 转贴的用户的id
                        repost_user_id = re.search(r'/(\d+)/', re_post_url).group(1)
                        # 转贴的帖子的id
                        repost_id = re.search(r'/([a-zA-Z0-9]+)\?', re_post_url).group(1)
                        repost_user_name = post.xpath('.//div[@class="content"]/div[@class="card-comment"]/div[@class="con"]/div/div[1]/a[1]/@nick-name').extract_first()
                        repost_authentication_text = post.xpath('.//div[@class="content"]/div[@class="card-comment"]/div[@class="con"]/div/div[1]/a[2]/@title').extract_first()
                        if repost_authentication_text == []:
                            repost_authentication_text.append('其他用户')
                        if '微博官方认证' in repost_authentication_text:
                            repost_authentication = '1'
                        elif '微博个人认证' in repost_authentication_text:
                            repost_authentication = '2'
                        elif '微博达人' in repost_authentication_text:
                            repost_authentication = '3'
                        elif '微博会员' in repost_authentication_text:
                            repost_authentication = '4'
                        else:
                            repost_authentication = '5'
                        if (weibo_user.objects.filter(user_id=repost_user_id).exists() == False):
                            print("添加新用户")
                            if repost_user_id != None:
                                print("这转发是用户的id", repost_user_id)
                                repost_user_url = 'https://weibo.com/p/100505' + repost_user_id + '/home?from=page_100505&mod=TAB&is_hot=1#place'
                                print("这是转发用户的信息链接", repost_user_url)
                                yield scrapy.Request(url=repost_user_url, callback=self.user_extract, cookies=response.meta['cookies'],meta={'authentication': repost_authentication, 'user_id': repost_user_id,'post_name': repost_user_name})
                        else:
                            print("用户已存在")
                        # 转发的帖子的点赞评论数时间等
                        repost_time = post.xpath(
                            './/div[@class="content"]//div[@class="con"]//div[@class="func"]/p[@class="from"]/a[1]/text()').extract_first()
                        # x分钟前
                        if re.search('(\d+)分钟前', repost_time) != None:
                            minutes = int(re.search('(\d+)分钟前', repost_time).group(1))
                            repost_time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
                            repost_time = repost_time.strftime("%Y-%m-%d %H:%M:%S")
                        # x秒
                        elif re.search('(\d+)秒前', repost_time) != None:
                            seconds = int(re.search('(\d+)秒前', repost_time).group(1))
                            repost_time = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
                            repost_time = repost_time.strftime("%Y-%m-%d %H:%M:%S")
                        elif re.search("今天", repost_time) !=None:
                            post_year = datetime.datetime.now().year
                            post_month = datetime.datetime.now().month
                            post_day = datetime.datetime.now().day
                            post_hour = re.search(r"(\d+):", repost_time).group(1)
                            post_minute = re.search(r":(\d+)", repost_time).group(1)
                            repost_time = "{}-{}-{}-{}-{}".format(post_year, post_month, post_day, post_hour,
                                                                  post_minute)
                            repost_time = datetime.datetime.strptime(repost_time, "%Y-%m-%d-%H-%M")
                            repost_time = repost_time.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            repost_time = re.sub('\s+', '', repost_time)
                            post_year = int(response.meta['weibo_time'].split('-')[0])
                            if re.match(r"年", repost_time):
                                post_year = re.search(r"(\d+)年", repost_time).group(1)
                            post_month = re.search(r"(\d+)月", repost_time).group(1)
                            post_day = re.search(r"(\d+)日", repost_time).group(1)
                            post_hour = re.search(r"(\d+):", repost_time).group(1)
                            post_minute = re.search(r":(\d+)", repost_time).group(1)
                            repost_time = "{}-{}-{}-{}-{}".format(post_year, post_month, post_day, post_hour,
                                                                  post_minute)
                            repost_time = datetime.datetime.strptime(repost_time, "%Y-%m-%d-%H-%M")
                            repost_time = repost_time.strftime("%Y-%m-%d %H:%M:%S")
                        #评论点赞转发提取
                        repost_bottom = post.xpath(
                            './/div[@class="content"]//div[@class="con"]//div[@class="func"]//li//text()').extract()
                        if num_re.search(repost_bottom[0]):
                            repost_forward_num = int(num_re.search(repost_bottom[0]).group())
                        if num_re.search(repost_bottom[1]):
                            repost_comment_num = int(num_re.search(repost_bottom[1]).group())
                        if num_re.search(repost_bottom[-1]):
                            repost_like_num = int(num_re.search(repost_bottom[-1]).group())

                        # 转发的帖子的内容
                        repost_content_ele = content[0].xpath('.//div[@class="con"]//p[@class="txt"][last()]')#[-1]
                        repost_content = ''.join(repost_content_ele.xpath('.//text()').extract())
                        repost_content = re.sub('\s+|收起全文d','',repost_content)
                        repost_content = re.sub(r"收起全文d", '', repost_content)
                        repost_a = repost_content_ele.xpath('.//a')
                        for v in repost_a:
                            repost_url = str(v.xpath('./@href').extract_first())
                            repost_url_value = v.xpath('.//text()').extract()
                            repost_url_value = ''.join(repost_url_value)
                            # 实体为用户
                            if user_re.match(repost_url_value):
                                repost_content = repost_content.replace('//'+repost_url_value,
                                                                        '<@>' + repost_url_value + ":" + repost_url + '</@>')
                                # print('{}:1'.format(repost_url_value))
                            # 实体为话题
                            elif topic_re.match(repost_url_value):
                                repost_content = repost_content.replace(repost_url_value,
                                                                        '<#>' + repost_url_value + '</#>')
                                # print('{}:2'.format(repost_url_value))
                            # 实体为link
                            else:
                                repost_content = repost_content.replace(repost_url_value,
                                                                        '<u>' + repost_url_value + ":" + repost_url + '</u>')
                        #logging.info(
                            #f"{repost_content},{repost_time},{repost_forward_num},{repost_user_id},{repost_id},{repost_comment_num},{repost_like_num}")
                    except Exception:
                        logging.error(Exception)
                        logging.error("转贴{}转发的帖子出现问题url:{}".format(c, response.meta['url']))
                    else:
                        item = PostItem()
                        item['user_id'] = user_id
                        item['post_id'] = post_id
                        item['post_content'] = emoji.demojize(original_content)
                        item['post_time'] = post_time
                        item['forward_num'] = forward_num
                        item['comment_num'] = comment_num
                        item['like_num'] = like_num
                        item['repost_id'] = repost_id
                        item['task_id'] = self.task_id
                        yield item
                        reitem = PostItem()
                        reitem['user_id'] = repost_user_id
                        reitem['post_id'] = repost_id
                        reitem['post_content'] = emoji.demojize(repost_content)
                        reitem['post_time'] = repost_time
                        reitem['forward_num'] = repost_forward_num
                        reitem['comment_num'] = repost_comment_num
                        reitem['like_num'] = repost_like_num
                        reitem['repost_id'] ='-100'
                        reitem['task_id'] = self.task_id
                        yield reitem
                else:#没有转贴信息
                    item = PostItem()
                    item['user_id'] = user_id
                    item['post_id'] = post_id
                    # item['authentication'] = authentication_text[0]
                    # item['post_name'] = post_name
                    item['post_content'] = emoji.demojize(original_content)
                    item['post_time'] = post_time
                    item['forward_num'] = forward_num
                    item['comment_num'] = comment_num
                    item['like_num'] = like_num
                    item['repost_id'] = None
                    item['task_id'] = self.task_id
                    yield item
    def user_extract(self,response):
        print("到达这个网页")
        authentication = response.meta['authentication']
        user_id = response.meta['user_id']
        post_name =response.meta['post_name']
        html = response.body.decode('utf-8')
        html= str(html)
        html = html.replace('\\t', '').replace('\\n', '').replace('\\r', '').replace(' ', '').replace('', '')
        try:
            if response.meta["authentication"] == '1':
                province = '-100'
                city = '-100'
            else:
                location = re.findall(r'<spanclass=\\"item_icoW_fl\\"><emclass=\\"W_ficonficon_cd_placeS_ficon\\">2<\\/em><\\/span><spanclass=\\"item_textW_fl\\">([\u4e00-\u9fff]+)<',html)[0]
                lenth = len(location)
                if (len(location) > 3):
                    if ('内蒙古' in location or '黑龙江' in location):
                        province = location[0:3]
                        city = location[3:lenth]
                        # print('省:' + province + '市:' + city)
                    else:
                        province = location[0:2]
                        city = location[2:lenth]
                        # print('省:' + province + '市:' + city)
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
            weibo_num = re.findall(r'>(\d+)<\\/strong><spanclass=\\"S_txt2\\">微博<\\/span>', html)[0]
            weibo_num = int(weibo_num)
        except:
            weibo_num = -100
        user_item = UserItem()
        user_item['user_id'] = user_id
        user_item['authentication'] = authentication
        user_item['user_name'] = post_name
        user_item['province'] = province
        user_item['city'] = city
        user_item['interest'] = interest
        user_item['fans'] = fans
        user_item['weibo_num'] = weibo_num
        try:
            user_item.save()
        except:
            pass
        return


