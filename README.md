# Spider
## 系统文件结构
- social_media_data_analyse_system
  - 下面的Settings文件配置爬虫相关基础信息：数据库的连接/文件的根目录/
- data_model
  - 主要定义了Mysql的数据库相关数据表
- scrapy_test
  - 使用了scrapy完成了爬虫的监控
- scrapy_monitor
  - 完成了爬虫状况的监控后端
- DataFiltering
  - 定义了数据过滤：下面包含textCNN模型
- temlpates 
  - 爬虫监控界面的HTML模板
## 系统启动命令
  - 启动系统
    `nohup python manage.py runserver 0.0.0.0:80 > myout.file 2>&1 & `
  - 启动定时任务 
    - `nohup python manage.py celery beat -l info  > myout_beat.file 2>&1 &`
    - `nohup python manage.py celery worker -l info  > myout_worker.file 2>&1 &`
