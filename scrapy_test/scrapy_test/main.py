import sys
import os
from scrapy.cmdline import execute
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "weibo",
         '-a','date_time_begin=2020-07-07-15','-a','date_time_end=2020-07-07-16',
         '-a','keyword=贵州公交坠河','-a','xsort=0','-a','scope=0',
         '-a','vip=0','-a','category=0','-a','task_id=0'])
