from django.shortcuts import render

# Create your views here.
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render
from data_model.models import scrapy_manage,xinlang_manage,weibo_post,xinlang_new
from scrapy_test.tasks import scrapy_start,scrapy_xinlang
import datetime
from django.db import connection
import json

def weibo_search(request):
    # 关键字
    cursor = connection.cursor()
    keyword = request.POST['keyword']
    weibo_type = request.POST['type']
    scope = 0
    xsort = 0
    vip = 0
    category = 0
    if weibo_type=='1':
        scope = 1
    if weibo_type == '2':
        xsort = 1
    if weibo_type == '3':
        vip = 1
    if weibo_type == '4':
        category = 1
    date_time_begin = request.POST['date_time_begin']
    date_time_begin_hour = request.POST['date_time_begin_hour']
    date_time_end = request.POST['date_time_end']
    date_time_end_hour = request.POST['date_time_end_hour']
    real_time_task = request.POST['real_time_task']
    date_time_begin = date_time_begin+'-'+date_time_begin_hour
    date_time_end = date_time_end+'-'+date_time_end_hour
    sql = 'select task_id from scrapy_manage where task_id like \'1_%\';'
    cursor.execute(sql)
    result = cursor.fetchall()
    task_id = 0
    for i in result:
        i = i[0].split('_')
        i = int(i[1])
        task_id = max(task_id,i)
    task_id = int(task_id)+1
    task_id = "1_"+str(task_id)
    if real_time_task=='0':#如果为实时任务
        res = scrapy_start.delay(date_time_begin,date_time_end,keyword,xsort,scope,vip,category,task_id)
        data = scrapy_manage(date_time_begin=date_time_begin, date_time_end=date_time_end
                             , keyword=keyword, xsort=xsort, scope=scope, vip=vip, category=category,
                             task_id=task_id, scrapy_id=res.id,real_time_task=real_time_task)
        data.save()
    else:#如果为实时任务
        date_time_now = datetime.datetime.now()
        date_time_now = str(date_time_now.year)+'-'+str(date_time_now.month)+'-'+str(date_time_now.day)+'-'+str(date_time_now.hour)
        res = scrapy_start.delay(date_time_begin, date_time_now, keyword, xsort, scope, vip, category, task_id)
        data = scrapy_manage(date_time_begin=date_time_begin,date_time_end=date_time_now
                         ,keyword=keyword,xsort=xsort,scope=scope,vip=vip,category=category,
                         task_id=task_id,scrapy_id=res.id,real_time_task=real_time_task)
        data.save()
    return HttpResponseRedirect("/scrapy_monitor/weibo_index")
    # return render(request, 'weibo_scrapy.html')
def weibo_index(request):
    return render(request,'weibo_scrapy.html')
def xinlang_search(request):
    cursor = connection.cursor()
    keyword = request.POST['keyword']
    range = request.POST['range']
    date_time_begin = request.POST['date_time_begin']
    date_time_begin_hour = request.POST['date_time_begin_hour']
    date_time_end = request.POST['date_time_end']
    date_time_end_hour = request.POST['date_time_end_hour']
    real_time_task = request.POST['real_time_task']
    date_time_begin = date_time_begin + '-' + date_time_begin_hour
    date_time_end = date_time_end + '-' + date_time_end_hour
    sql = 'select task_id from xinlang_manage where task_id like \'2_%\';'
    cursor.execute(sql)
    result = cursor.fetchall()
    task_id = 0
    for i in result:
        i = i[0].split('_')
        i = int(i[1])
        task_id = max(task_id, i)
    task_id = int(task_id) + 1
    task_id = "2_"+str(task_id)
    if real_time_task=='0':#如果是非实时任务
        res = scrapy_xinlang.delay(date_time_begin,date_time_end,keyword,range,task_id)
        data = xinlang_manage(date_time_begin=date_time_begin,scrapy_id=res.id, date_time_end=date_time_end, keyword=keyword,range=range,task_id=task_id,real_time_task=real_time_task)
        data.save()
    else:   #如果为实时任务
        date_time_now = datetime.datetime.now()
        # date_time_now = str(date_time_now.year) + '-' + str(date_time_now.month) + '-' + str(date_time_now.day) + '-' + str(date_time_now.hour)
        date_time_now = date_time_now.strftime('%Y-%m-%d-%H')
        res = scrapy_xinlang.delay(date_time_begin, date_time_now, keyword, range, task_id)
        data = xinlang_manage(date_time_begin=date_time_begin, scrapy_id=res.id, date_time_end=date_time_now,
                              keyword=keyword, range=range, task_id=task_id, real_time_task=real_time_task)
        data.save()
    return render(request,'Xinlang_scrapy.html')
def xinlang_index(request):
    return render(request,'Xinlang_scrapy.html')

# 爬虫的index页面
def index(request):
    sinaWeibo_count = weibo_post.objects.count()
    sinaNews_count = xinlang_new.objects.count()
    Earthquake_count = weibo_post.objects.filter(task_id='1_1').count()+ xinlang_new.objects.filter(task_id='2_1').count()
    Typhoon_count = weibo_post.objects.filter(task_id='1_2').count()+ xinlang_new.objects.filter(task_id='2_2').count()
    Rain_count = weibo_post.objects.filter(task_id='1_3').count()+ xinlang_new.objects.filter(task_id='2_3').count()
    source_data ={'sinaWeibo_count':sinaWeibo_count,'sinaNews_count':sinaNews_count}
    diaster_data={'Earthquake_count':Earthquake_count,'Typhoon_count':Typhoon_count,'Rain_count':Rain_count}
    return render(request, 'index.html',{'source_data':source_data,'diaster_data':diaster_data})

# 爬虫任务表前端展示
def spider_manage(request):
    Xinlang = xinlang_manage.objects.all()
    Weibo = scrapy_manage.objects.all()
    return render(request, 'spider_manage.html', {'Xinlang':Xinlang, 'Weibo':Weibo,})

# 爬虫的每日监控界面
def day_monitor(request):
    dateList = []

    totalNum_list = []
    sinaWeiboNum_list = []
    sinaNewsNum_list = []
    EarthquakeNum_list=[]
    TyphoonNum_list = []
    RainNum_list = []
    date_now = datetime.date.today()
    for i in range(0,30):
        i = 30 - i
        delta = datetime.timedelta(days=i)
        date_past = date_now - delta
        dateList.append(str(date_past))
        Weibo_count = weibo_post.objects.filter(post_time__contains=date_past).count()
        News_count = xinlang_new.objects.filter(date__contains=date_past).count()

        totalNum_list.append(Weibo_count+News_count)
        sinaWeiboNum_list.append(Weibo_count)
        sinaNewsNum_list.append(News_count)
        Earthquake_count = weibo_post.objects.filter(post_time__contains=date_past,task_id='1_1').count()+xinlang_new.objects.filter(date__contains=date_past,task_id='2_1').count()
        Typhoon_count = weibo_post.objects.filter(post_time__contains=date_past,task_id='1_2').count()+xinlang_new.objects.filter(date__contains=date_past,task_id='2_2').count()
        Rain_count = weibo_post.objects.filter(post_time__contains=date_past,task_id='1_3').count()+xinlang_new.objects.filter(date__contains=date_past,task_id='2_3').count()

        EarthquakeNum_list.append(Earthquake_count)
        TyphoonNum_list.append(Typhoon_count)
        RainNum_list.append(Rain_count)
    dayMonitorList={'date':dateList,'totalNum_list':totalNum_list,'sinaWeiboNum_list':sinaWeiboNum_list,'sinaNewsNum_list':sinaNewsNum_list,'EarthquakeNum_list':EarthquakeNum_list,'TyphoonNum_list':TyphoonNum_list,'RainNum_list':RainNum_list}
    return render(request,'day_monitor.html',{'dayMonitorList':dayMonitorList})
def timed_monitor(request):
    time_now = datetime.datetime.now()
    time_list =[]
    totalCount = 0
    sinaWeiboCount = 0
    sinaNewsCount = 0
    EarthquakeCount = 0
    TyphoonCount = 0
    RainCount = 0
    totalNum_list = []
    sinaWeiboNum_list = []
    sinaNewsNum_list = []
    EarthquakeNum_list = []
    TyphoonNum_list = []
    RainNum_list = []
    for i in range(0,23):
        i = 24 - i
        delta = datetime.timedelta(hours=i)
        time_pastl = time_now - delta
        time_past=datetime.datetime.strftime(time_pastl, "%Y-%m-%d %H")
        time_li = datetime.datetime.strftime(time_pastl, "%H:00:00")
        time_list.append(time_li)
        Weibo_count = weibo_post.objects.filter(post_time__contains=time_past).count()
        News_count = xinlang_new.objects.filter(date__contains=time_past).count()
        totalNum_list.append(Weibo_count + News_count)
        sinaWeiboNum_list.append(Weibo_count)
        sinaNewsNum_list.append(News_count)
        totalCount += (Weibo_count + News_count)
        sinaWeiboCount += Weibo_count
        sinaNewsCount += News_count
        Earthquake_count = weibo_post.objects.filter(post_time__contains=time_past,task_id='1_1').count() + xinlang_new.objects.filter(date__contains=time_past,task_id='2_1').count()
        Typhoon_count = weibo_post.objects.filter(post_time__contains=time_past,task_id='1_2').count() + xinlang_new.objects.filter(date__contains=time_past,task_id='2_2').count()
        Rain_count = weibo_post.objects.filter(post_time__contains=time_past,task_id='1_3').count() + xinlang_new.objects.filter(date__contains=time_past,task_id='2_3').count()
        EarthquakeNum_list.append(Earthquake_count)
        TyphoonNum_list.append(Typhoon_count)
        RainNum_list.append(Rain_count)
        EarthquakeCount += Earthquake_count
        TyphoonCount += Typhoon_count
        RainCount += Rain_count
    count = {'totalCount':totalCount,'sinaWeiboCount':sinaWeiboCount,'sinaNewsCount':sinaNewsCount,'EarthquakeCount':EarthquakeCount,'TyphoonCount':TyphoonCount,'RainCount':RainCount}
    TimedMonitorList={'time_list':time_list,'totalNum_list':totalNum_list,'sinaWeiboNum_list':sinaWeiboNum_list,'sinaNewsNum_list':sinaNewsNum_list,'EarthquakeNum_list':EarthquakeNum_list,'TyphoonNum_list':TyphoonNum_list,'RainNum_list':RainNum_list}

    return render(request,'timed_monitor.html',{'count':count,'TimedMonitorList':TimedMonitorList})
def test(request):
    return render(request,'weib.html')