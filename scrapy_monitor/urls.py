#-*- coding = utf-8 -*-
from django.urls import path
from django.contrib import admin
from django.conf.urls import url
from . import views
app_name = 'scrapy_monitor'
urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^weibo_search/$', views.weibo_search, name='weibo_search'), #+ 新增一个新的URL
    url(r'^weibo_index/$', views.weibo_index, name='weibo_index'), #+ 新增一个新的URL
    url(r'^xinlang_index/$',views.xinlang_index,name='xinlang_index'),
    url(r'^xinlang_search/$',views.xinlang_search,name='xinlang_search'),
    url(r'^index/$',views.index,name='index'),
    url(r'^spider_mange/$',views.spider_manage,name='spider_manage'),
    url(r'^day_monitor/$',views.day_monitor,name='day_monitor'),
    url(r'^test/$',views.test,name='test'),
    url(r'^timed_monitor/$',views.timed_monitor,name='timed_monitor')
    # path('data_control/',admin.site.urls)
]



