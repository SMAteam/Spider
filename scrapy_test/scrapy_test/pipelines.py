# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import datetime
import pymongo
import pika
from urllib.parse import unquote
import pymysql
import json
import os
import re
from .items import XinlangItem,PostItem
import functools
from Datafiltering.datatextCNN import init_data,textCNNFilter
import gc
data_list =[]
class ScrapyTestPipeline:
    def __init__(self):
        self.post_id = set()
    def process_item(self, item, spider):
        try:
            #处理新浪微博数据
            if spider.name == "weibo":
                item['post_content'] = re.sub('\\u200b','',item['post_content'])
                post_time = item['post_time']
                post_time = datetime.datetime.strptime(post_time, "%Y-%m-%d %H:%M:%S")
                item['post_time'] = post_time
                if (post_time < datetime.datetime.now()):
                    # weibo_item 是mysql用来存储微博的数据
                    weibo_item = PostItem()
                    weibo_item["user_id"] = item['user_id']
                    weibo_item['post_id'] = item['post_id']
                    weibo_item['post_content'] = item['post_content']
                    weibo_item['post_time'] = post_time
                    weibo_item['forward_num'] = item['forward_num']
                    weibo_item['comment_num'] = item['comment_num']
                    weibo_item['like_num'] = item['like_num']
                    weibo_item['repost_id'] = item['repost_id']
                    weibo_item['task_id'] = item['task_id']
                    weibo_item.save()
                    print("传递数据")
                    return item
                else:
                    print(post_time)
                    print("日期不正确")

            #处理新浪新闻数据
            if spider.name == "xinlang":
                Xitem = XinlangItem()
                Xitem["post_id"]= item["post_id"]
                item["title"] = re.sub('原标题：[【】《》！、，。,\u4e00-\u9fff]+\s+','',item["title"])
                item["title"] = re.sub(
                    '([\u4e00-\u9fff]+客户端[\u4e00-\u9fff]*[\|:，：,。！.]*)|(([\u4e00-\u9fff]+新闻[\u4e00-\u9fff]*[\|:，：,。！.]*)|([\u4e00-\u9fff]+网[\u4e00-\u9fff]*[\|:，：,。！.]*)|([\u4e00-\u9fff]+早报[\|:，：,。！.]*)|([\u4e00-\u9fff]+资讯[\|:，：.,。！]*)|([\u4e00-\u9fff]+晚报[\|:，：,。！]*)|(@[\u4e00-\u9fff]+[\|:，：.,。！]*))',
                    '', item["title"])
                item["brief"] = re.sub('原标题：[【】《》！、，。,\u4e00-\u9fff]+\s+', '', item["brief"])
                item["brief"] = re.sub(
                    '([\u4e00-\u9fff]+客户端[\u4e00-\u9fff]*[\|:，：,。！.]*)|(([\u4e00-\u9fff]+新闻[\u4e00-\u9fff]*[\|:，：,。！.]*)|([\u4e00-\u9fff]+网[\u4e00-\u9fff]*[\|:，：,。！.]*)|([\u4e00-\u9fff]+早报[\|:，：,。！.]*)|([\u4e00-\u9fff]+资讯[\|:，：.,。！]*)|([\u4e00-\u9fff]+晚报[\|:，：,。！]*)|(@[\u4e00-\u9fff]+[\|:，：.,。！]*))',
                    '', item["brief"])
                Xitem["title"] = item["title"]
                Xitem["user_name"] = item["author"]
                Xitem["post_time"] = item["date"]
                Xitem["brief"] = item["brief"]
                Xitem["detail_link"] = item["detail_link"]
                # Xitem["content"] = item["content"]
                Xitem["post_content"]=[]
                Xitem["task_id"] = item["task_id"]
                date = Xitem['post_time']
                date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                index = 0
                for li in item['content']:
                    index+=1
                    li = re.sub('\s', ' ', li)
                    li = re.sub('@[\u4e00-\u9fff]+[\|:，：.,。！]*','',li)
                    # 处理开头
                    if("原标题" in li or "本文转自" in li or "原题" in li or "摄影报道" in li or "资料：" in li):
                        continue
                    if("记者" in li and len(li)<15):
                        continue
                    #  处理结尾
                    if(("来源：" in li) or ("来源于" in li) or("文字：" in li ) or("记者：" in li ) or ("通讯员：" in li) or ("来源|" in li) or ("'资料：" in li) or ("编辑：" in li) or ("作者" in li) or ("媒体记者" in li) or ("新闻记者" in li) or ("新闻来源丨" in li) or ("责编" in li)):
                        if(index>1):
                            if(index>3):
                                break
                            else:
                                continue
                    if(len(li)<8):
                        continue
                    Xitem["post_content"].append(li)
                if(Xitem["post_content"]):
                    if("记者 " in Xitem["post_content"][-1] or "报社" in Xitem["post_content"][-1]):
                        if(len(Xitem["post_content"][-1])<20):
                            del Xitem["post_content"][-1]

                if (date < datetime.datetime.now()):
                    Xitem['post_time'] = date
                    Xitem.save()
                    print("数据已存在")
                    return Xitem
                else:
                    print(date)
                    print("日期不正确")
        except:
            print(item)
            print('错误')



#######################################################
# 用于处理数据的管道2


class ScrapyDataFusion:
    def open_spider(self, spider):
        print("爬虫开启")
        # spider.hello = "world"  # 为spider对象动态添加属性，可以在spider模块中获取该属性值
        # 可以开启数据库等
    def process_item(self, item, spider):
        if item == None:
            print("数据不正确")
        else:
            real_time_task = spider.real_time_task
            if spider.name == 'weibo':
                weibo_data = {}
                weibo_data['media'] = '1'
                task = item['task_id'].split('_')[1]
                weibo_data['task'] = task
                weibo_data['user_id'] = item['user_id']
                weibo_data['post_id'] = item['post_id']
                weibo_data['post_content'] = item['post_content']
                weibo_data['post_time'] = item['post_time']
                weibo_data['forward_num'] = item['forward_num']
                weibo_data['comment_num'] = item['comment_num']
                weibo_data['like_num'] = item['like_num']
                weibo_data['repost_id'] = item['repost_id']
                weibo_data["user_name"] = item["user_name"]
                weibo_data["province"] = item["province"]
                weibo_data["province"] = item["province"]
                weibo_data["authentication"] = item["authentication"]
                weibo_data["fans"] = item["fans"]
                weibo_data["interest"] = item["interest"]
                weibo_data["weibo_num"] = item["weibo_num"]
                weibo_data["post_url"] = "https://weibo.com/" + str(weibo_data['user_id']) + "/" + str( weibo_data['post_id'] ) + "/"
                # 微博数据过滤
                stopwords, model, word_index = init_data()
                weibo_data = textCNNFilter(weibo_data, model, word_index, stopwords)

                # 存储到mongo数据库中
                conn = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "152.136.59.62", "27017", "admin"))
                db = conn.SocialMedia
                collection = db.posts
                collection.update_one({'task': weibo_data['task'], 'post_id': weibo_data['post_id']}, {'$set': weibo_data}, True)
                conn.close()
                # 将数据添加到列表中
                weibo_time = item['post_time']
                weibo_time = datetime.datetime.strftime(weibo_time, '%Y-%m-%d %H:%M:%S')
                weibo_data['post_time'] = weibo_time
                if(real_time_task=='0'):
                    print("非实时任务，不需要消息传递")
                else:
                    data_list.append(weibo_data)
            # 处理新浪新闻的数据
            if spider.name == 'xinlang':
                sina_data = {}
                sina_data['media'] = '2'
                task = item['task_id'].split('_')[1]
                sina_data['task']  = task
                sina_data["post_id"] = item["post_id"]
                sina_data["title"] = item['title']
                sina_data["user_name"] = item["user_name"]
                sina_data["post_time"] = item['post_time']
                sina_data["brief"] = item["brief"]
                sina_data["post_url"] = item["detail_link"]
                sina_data["post_content"] = item["post_content"]
                # 垃圾过滤
                stopwords, model, word_index = init_data()
                sina_data = textCNNFilter(sina_data, model, word_index, stopwords)
                # 存储到mongo数据库中
                conn = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format("root", "buptweb007", "152.136.59.62", "27017", "admin"))
                db = conn.SocialMedia
                collection = db.posts
                collection.update_one({'task': sina_data['task'], 'post_id': sina_data['post_id'],}, {'$set': sina_data}, True)
                conn.close()
                sina_time = datetime.datetime.strftime(item['post_time'], '%Y-%m-%d %H:%M:%S')
                sina_data["post_time"] = sina_time
                # 将新闻数据添加到列表
                if (real_time_task == '0'):
                    print("非实时任务，不需要消息传递")
                else:
                    data_list.append(sina_data)
    def close_spider(self, spider):
        real_time_task = spider.real_time_task
        if(real_time_task =='0'):
            print("非实时任务，爬虫结束！")
        else:
            task_id = spider.task_id
            media = int(task_id.split('_')[0])
            task = int(task_id.split('_')[1])
            # print(spider.keyword)
            # keyword = unquote(spider.keyword).strip()
            # 爬虫数据完成，将数据导入
            with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'r', encoding='utf-8') as f:
                data = json.load(f)
                f.close()
            if(data_list!=[]):
                data["data"] = data["data"] + data_list
            print('数据长度',len(data["data"]))
            with open(os.path.join(os.path.dirname(__file__), 'data.json'), "w", encoding="utf8") as f:
                json.dump(data, f, ensure_ascii=False)
                f.close()
            db = pymysql.connect(host='152.136.59.62', user='root', passwd='buptweb007', db='social_database', port=3307,autocommit=True)
            cursor = db.cursor()
            sql1 = f'update message set value = 1 where media = {media} and task ={task}'
            cursor.execute(sql1)
            cursor.close()
            db.close()
            print("消息修改")
            # 验证是否已经数据全部完成
            db = pymysql.connect(host='152.136.59.62', user='root', passwd='buptweb007', db='social_database', port=3307,autocommit=True)
            cursor = db.cursor()
            sql = f'select * from message where task = {task}'
            cursor.execute(sql)
            message = cursor.fetchall()
            cursor.close()
            db.close()
            flag = 1  # 标志字段
            for i in message:
                if (i[2] == 0):
                    flag = 0
                    break
            # 处理数据全部获取完毕的情况
            if (flag == 1):
                with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    f.close()
                data =data['data']
                def compare(item1, item2):
                    #t1 = datetime.datetime.strptime(item1["post_time"], "%Y-%m-%d %H:%M:%S")
                    #t2 = datetime.datetime.strptime(item2["post_time"], "%Y-%m-%d %H:%M:%S")
                    if (item1["post_time"] >= item2["post_time"]):
                        return 1
                    else:
                        return -1
                social_data = sorted(data, key=functools.cmp_to_key(compare))
                # 转换为json格式
                social_data = json.dumps(social_data,ensure_ascii=False)
                print("数据长度",len(social_data))
                with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'r', encoding='utf-8') as f:
                           new_data = json.load(f)
                           f.close()
                new_data["data"] =[]
                with open(os.path.join(os.path.dirname(__file__), 'data.json'), "w", encoding="utf8") as f:
                           json.dump(new_data, f, ensure_ascii=False)
                           f.close()

                # 传递消息队列
                credentials = pika.PlainCredentials('root', 'buptweb007')  # mq用户名和密码
                # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
                connection = pika.BlockingConnection(pika.ConnectionParameters(host="152.136.59.62", port=5672, virtual_host='scrapy',credentials=credentials))
                channel = connection.channel()
                # 声明消息队列，消息将在这个队列传递，如不存在，则创建
                result = channel.queue_declare(queue='earthquake')
                # 向队列插入数值 routing_key是队列名
                channel.basic_publish(exchange='', routing_key='earthquake', body=social_data)
                connection.close()
                # print(social_data)
                db = pymysql.connect(host='152.136.59.62', user='root', passwd='buptweb007', db='social_database', port=3307,autocommit=True)
                cursor = db.cursor()
                sql1 = f'update message set value = 0 where task ={task}'
                cursor.execute(sql1)
                cursor.close()
                db.close()
                gc.collect()
                print("全部数据已经获取完毕")


