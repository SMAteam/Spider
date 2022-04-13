from django.db import models

# Create your models here.
class scrapy_manage(models.Model):
    task_id = models.CharField(max_length=20,primary_key=True)
    scrapy_id = models.CharField(max_length=500,null=True,blank=True)
    scope = models.CharField(max_length=2, null=True, blank=True)
    xsort = models.CharField(max_length=2, null=True, blank=True)
    category = models.CharField(max_length=2, null=True, blank=True)
    vip = models.CharField(max_length=2, null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)
    date_time_begin = models.CharField(max_length=500, null=True, blank=True)
    date_time_end = models.CharField(max_length=500, null=True, blank=True)
    real_time_task = models.CharField(max_length=2, null=True, blank=True)
    class Meta:
        db_table = "scrapy_manage"
class weibo_user(models.Model):
    user_id = models.BigIntegerField(primary_key=True,)
    user_name = models.CharField(max_length=100)
    province = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    authentication = models.CharField(max_length=100,null=True,blank=True)
    fans =models.IntegerField(null=True,blank=True)
    interest =models.IntegerField(null=True,blank=True)
    weibo_num =models.IntegerField(null=True,blank=True)
    class Meta:
        db_table = "weibo_user"
class weibo_post(models.Model):
    user_id = models.BigIntegerField(null=True,blank=True)
    post_id = models.CharField(max_length=100,)
    post_content = models.TextField(null=True,blank=True)
    post_time = models.DateTimeField(null=True,blank=True)
    forward_num = models.IntegerField(null=True,blank=True)
    comment_num = models.IntegerField(null=True,blank=True)
    like_num = models.IntegerField(null=True,blank=True)
    repost_id = models.CharField(max_length=20,null=True,blank=True)
    task_id = models.CharField(max_length=20)
    # 接下来设置联合主键
    class Meta:
        unique_together = ("post_id","task_id")
        ordering = ["-post_time","-forward_num","-comment_num","-like_num"]
        db_table = "weibo_post"

class noise_judge(models.Model):
    post_id = models.CharField(max_length=100)
    task_id = models.CharField(max_length=100)
    noise = models.CharField(max_length=2,null=True,blank=True)
    # 接下来设置联合主键
    class Meta:
        unique_together = ("post_id", "task_id")
        db_table = "noise_judge"
class category(models.Model):
    post_id = models.CharField(max_length=100)
    task_id = models.CharField(max_length=100)
    category = models.CharField(max_length=500,null=True,blank=True)
    # 接下来设置联合主键
    class Meta:
        unique_together = ("post_id", "task_id")
        db_table = "category"
class event(models.Model):
    post_id = models.CharField(max_length=100)
    task_id = models.CharField(max_length=100)
    time = models.DateTimeField(null=True, blank=True)
    province = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    area = models.TextField(null=True, blank=True)
    event = models.TextField(null=True,blank=True)
    cluster = models.CharField(max_length=500,null=True,blank=True)
    # 接下来设置联合主键
    class Meta:
        unique_together = ("post_id", "task_id")
        db_table = "event"

class xinlang_manage(models.Model):
    task_id = models.CharField(max_length=20, primary_key=True)
    scrapy_id = models.CharField(max_length=500, null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)
    range = models.CharField(max_length=10, null=True, blank=True)
    date_time_begin = models.CharField(max_length=500, null=True, blank=True)
    date_time_end = models.CharField(max_length=500, null=True, blank=True)
    real_time_task = models.CharField(max_length=2, null=True, blank=True)
    class Meta:
        db_table = "xinlang_manage"


class xinlang_new(models.Model):
    post_id = models.CharField(primary_key=True,max_length=100)
    user_name = models.CharField(max_length=100)
    post_time = models.DateTimeField(null=True,blank=True)
    title = models.TextField(null=True,blank=True)
    brief = models.TextField(null=True,blank=True)
    post_content = models.TextField(null=True,blank=True)
    detail_link = models.CharField(max_length=100)
    task_id = models.CharField(max_length=20)
    class Meta:
        unique_together = ("task_id","post_id")
