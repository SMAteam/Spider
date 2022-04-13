import os
import json
data = {'data':[]}
with open ('data.json',"w",encoding="utf8") as f:
    f.write(json.dumps(data))
    f.close()
#with open('data.json', 'r', encoding='utf-8') as f:
#        data = json.load(f, strict=False)
#        f.close()
#with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'r', encoding='utf-8') as f:
#        data = json.load(f)
#        f.close()
#print(data)
# import datetime
# time = '2020-9-10 21:00:00'
# time =datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
# weibo_time = datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
# print(weibo_time)

# import pymysql
# db = pymysql.connect(host='localhost', user='root', passwd='123456', db='social_media', port=3306)
# cursor = db.cursor()
# sql  =  f'select * from weibo_user where user_id = "458866"'
