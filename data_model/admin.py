from django.contrib import admin

# Register your models here.
from .models import scrapy_manage,weibo_post,xinlang_new,xinlang_manage,weibo_user

class Scrapy_manageAdmin(admin.ModelAdmin):
    #列表页属性
    #显示字段属性名
    def tas(self):
        if self.real_time_task=='1':
            return "实时"
        else:
            return "非实时"
    tas.short_description = '任务类别'
    list_display = ['task_id',tas,'scrapy_id','scope','xsort','category','vip','keyword','date_time_begin','date_time_end',]
    #过滤器  过滤字段
    list_filter = ['real_time_task']
    # 搜索字段
    search_fields = ['task_id']
    list_per_page = 50
    #添加，修改页属性
    #属性的先后顺序
    fields = []
    #添加分组
    fieldsets = []
#注册
admin.site.register(scrapy_manage, Scrapy_manageAdmin)


class Weibo_postAdmin(admin.ModelAdmin):

    list_display =['task_id','user_id','post_id','post_time','post_content','forward_num','comment_num','like_num','repost_id']
    list_filter = ['task_id']
    search_fields = ['task_id']
    list_per_page=100

admin.site.register(weibo_post,Weibo_postAdmin)

class Weibo_userAdmin(admin.ModelAdmin):
    list_display = ['user_id','user_name','province','city','authentication','fans','interest','weibo_num']
    list_filter = ['province']
    search_fields = ['user_id','user_name','province','city']
    list_per_page = 100
admin.site.register(weibo_user,Weibo_userAdmin)

class Xinlang_newsAdmin(admin.ModelAdmin):
    list_display = ['task_id','post_id','user_name','post_time','title','brief','post_content','detail_link']
    list_filter = ['task_id']
    search_fields = ['task_id']
    list_per_page = 100
admin.site.register(xinlang_new,Xinlang_newsAdmin)
class Xinlang_manageAdmin(admin.ModelAdmin):
    list_display = ['task_id','scrapy_id','range','keyword','date_time_begin','date_time_end','real_time_task']
    list_filter = ['task_id']
    search_fields = ['task_id']
    list_per_page = 100
admin.site.register(xinlang_manage,Xinlang_manageAdmin)
