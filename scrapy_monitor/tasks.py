import base64
import os
import subprocess
import requests
import os,django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")
django.setup()
from celery import task

from data_model.models import scrapy_manage,xinlang_manage
from scrapy_test.tasks import scrapy_start,scrapy_xinlang
import datetime
import json
import os
import django
django.setup()
from django.db import connection
from .weibo_login import get_cookie
@task
def timed_cookies():
    print("定时获取cookie")
    get_cookie()
    # p=getCookies()
    # print("后面获取的是我更新的cookie：","这是我的cookie")
    # with open(os.path.join(os.path.dirname(__file__),'cookie.json'), 'w') as f:
    #     json.dump(p, f,ensure_ascii=False)
    #     print(p)
    #     print("cookies写入成功")

@task
def timed_task():
    print("这是我的定时任务")
    scrapys = scrapy_manage.objects.filter(real_time_task='1')
    for s in scrapys:
        date_time_now = datetime.datetime.now()
        date_time_now = str(date_time_now.year) + '-' + str(date_time_now.month) + '-' + str(
            date_time_now.day) + '-' + str(date_time_now.hour)
        date_end=s.date_time_end
        res = scrapy_start.delay(date_end, date_time_now, s.keyword, s.xsort, s.scope, s.vip, s.category,s.task_id)
        q = scrapy_manage.objects.get(task_id=s.task_id)
        q.date_time_end = date_time_now
        q.scrapy_id = res.id
        q.save()



@task
def xinlang_task():
    print("新浪新闻爬虫")
    Xscrapys =xinlang_manage.objects.filter(real_time_task='1')
    for s in Xscrapys:
        date_time_now = datetime.datetime.now()
        date_time_now = str(date_time_now.year) + '-' + str(date_time_now.month) + '-' + str(
            date_time_now.day) + '-' + str(date_time_now.hour)
        date_end=s.date_time_end
        res = scrapy_xinlang.delay(date_end, date_time_now, s.keyword, s.range,s.task_id)
        q = xinlang_manage.objects.get(task_id=s.task_id)
        q.date_time_end = date_time_now
        q.scrapy_id = res.id
        q.save()