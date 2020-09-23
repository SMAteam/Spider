# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy_djangoitem import DjangoItem
from data_model.models import weibo_post,weibo_user,xinlang_new

class PostItem(DjangoItem):
    django_model = weibo_post
class UserItem(DjangoItem):
    django_model = weibo_user
class XinlangItem(DjangoItem):
    django_model = xinlang_new
