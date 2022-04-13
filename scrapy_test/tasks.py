from celery import task
import subprocess

@task
def scrapy_start(date_time_begin,date_time_end,keyword,xsort,scope,vip,category,task_id,real_time_task):
    subprocess.Popen(["scrapy", "crawl", "weibo",
             '-a', f'date_time_begin={date_time_begin}', '-a', f'date_time_end={date_time_end}',
             '-a', f'keyword={keyword}', '-a', f'xsort={xsort}', '-a', f'scope={scope}',
             '-a', f'vip={vip}', '-a', f'category={category}', '-a', f'task_id={task_id}','-a',f'real_time_task={real_time_task}'],shell=False,cwd='./scrapy_test')
    return task_id

@task
def scrapy_xinlang(date_time_begin,date_time_end,keyword,range,task_id,real_time_task):
    subprocess.Popen(["scrapy", "crawl", "xinlang",
             '-a', f'date_time_begin={date_time_begin}', '-a', f'date_time_end={date_time_end}',
             '-a', f'keyword={keyword}', '-a', f'range={range}','-a', f'task_id={task_id}','-a',f'real_time_task={real_time_task}'],shell=False,cwd='./scrapy_test')
    return task_id