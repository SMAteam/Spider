# from django.db.models import Max
# from django.shortcuts import render
# from .models import scrapy_manage,xinlang_manage
# from scrapy_test.tasks import scrapy_start,scrapy_xinlang
# import datetime
# from django.db import connection
#
# def weibo_search(request):
#     # 关键字
#     cursor = connection.cursor()
#     keyword = request.POST['keyword']
#     weibo_type = request.POST['type']
#     scope = 0
#     xsort = 0
#     vip = 0
#     category = 0
#     if weibo_type=='1':
#         scope = 1
#     if weibo_type == '2':
#         xsort = 1
#     if weibo_type == '3':
#         vip = 1
#     if weibo_type == '4':
#         category = 1
#     date_time_begin = request.POST['date_time_begin']
#     date_time_begin_hour = request.POST['date_time_begin_hour']
#     date_time_end = request.POST['date_time_end']
#     date_time_end_hour = request.POST['date_time_end_hour']
#     real_time_task = request.POST['real_time_task']
#     date_time_begin = date_time_begin+'-'+date_time_begin_hour
#     date_time_end = date_time_end+'-'+date_time_end_hour
#     sql = 'select task_id from scrapy_manage where task_id like \'1_%\';'
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     task_id = 0
#     for i in result:
#         i = i[0].split('_')
#         i = int(i[1])
#         task_id = max(task_id,i)
#     task_id = int(task_id)+1
#     task_id = "1_"+str(task_id)
#     if real_time_task=='0':#如果为实时任务
#         res = scrapy_start.delay(date_time_begin,date_time_end,keyword,xsort,scope,vip,category,task_id)
#         data = scrapy_manage(date_time_begin=date_time_begin, date_time_end=date_time_end
#                              , keyword=keyword, xsort=xsort, scope=scope, vip=vip, category=category,
#                              task_id=task_id, scrapy_id=res.id,real_time_task=real_time_task)
#         data.save()
#     else:#如果为实时任务
#         date_time_now = datetime.datetime.now()
#         date_time_now = str(date_time_now.year)+'-'+str(date_time_now.month)+'-'+str(date_time_now.day)+'-'+str(date_time_now.hour)
#         res = scrapy_start.delay(date_time_begin, date_time_now, keyword, xsort, scope, vip, category, task_id)
#         data = scrapy_manage(date_time_begin=date_time_begin,date_time_end=date_time_now
#                          ,keyword=keyword,xsort=xsort,scope=scope,vip=vip,category=category,
#                          task_id=task_id,scrapy_id=res.id,real_time_task=real_time_task)
#         data.save()
#
#     return render(request, 'weibo_scrapy.html')
# def weibo_index(request):
#     return render(request,'weibo_scrapy.html')
# def xinlang_search(request):
#     cursor = connection.cursor()
#     keyword = request.POST['keyword']
#     range = request.POST['range']
#     date_time_begin = request.POST['date_time_begin']
#     date_time_begin_hour = request.POST['date_time_begin_hour']
#     date_time_end = request.POST['date_time_end']
#     date_time_end_hour = request.POST['date_time_end_hour']
#     real_time_task = request.POST['real_time_task']
#     date_time_begin = date_time_begin + '-' + date_time_begin_hour
#     date_time_end = date_time_end + '-' + date_time_end_hour
#     sql = 'select task_id from xinlang_manage where task_id like \'2_%\';'
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     task_id = 0
#     for i in result:
#         i = i[0].split('_')
#         i = int(i[1])
#         task_id = max(task_id, i)
#     task_id = int(task_id) + 1
#     task_id = "2_"+str(task_id)
#     if real_time_task=='0':#如果是非实时任务
#         res = scrapy_xinlang.delay(date_time_begin,date_time_end,keyword,range,task_id)
#         data = xinlang_manage(date_time_begin=date_time_begin,scrapy_id=res.id, date_time_end=date_time_end, keyword=keyword,range=range,task_id=task_id,real_time_task=real_time_task)
#         data.save()
#     else:   #如果为实时任务
#         date_time_now = datetime.datetime.now()
#         # date_time_now = str(date_time_now.year) + '-' + str(date_time_now.month) + '-' + str(date_time_now.day) + '-' + str(date_time_now.hour)
#         date_time_now = date_time_now.strftime('%Y-%m-%d-%H')
#         res = scrapy_xinlang.delay(date_time_begin, date_time_now, keyword, range, task_id)
#         data = xinlang_manage(date_time_begin=date_time_begin, scrapy_id=res.id, date_time_end=date_time_now,
#                               keyword=keyword, range=range, task_id=task_id, real_time_task=real_time_task)
#         data.save()
#     return render(request,'Xinlang_scrapy.html')
# def xinlang_index(request):
#     return render(request,'Xinlang_scrapy.html')
#

