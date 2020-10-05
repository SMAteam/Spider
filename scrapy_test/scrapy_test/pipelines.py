# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import datetime
import re
from .items import XinlangItem
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
                if (post_time < datetime.datetime.now()):
                    item['post_time'] = post_time
                    item.save()
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
                date = Xitem['date']
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

                # Xitem['content'] = re.sub('\\u200b', '', Xitem['content'])
                if (date < datetime.datetime.now()):
                    Xitem['post_time'] = date
                    Xitem.save()
                else:
                    print(date)
                    print("日期不正确")
        except:
            print(item)
            print('错误')

