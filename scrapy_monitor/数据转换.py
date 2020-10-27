import pymysql

db = pymysql.connect(host='152.136.59.62', user='root', passwd='buptweb007', db='test', port=3307)
cursor = db.cursor()
sql = f'select * from weibo_post limit 100;'
cursor.execute(sql)
ret = cursor.fetchall()
for r in ret:
    print(r[0])
# print(ret)