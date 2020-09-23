from django.test import TestCase

# Create your tests here.
import datetime
dt = datetime.date.today()
for i in range(0,30):
    d1 = datetime.timedelta(days=i)
    dt1 = dt-d1
time = datetime.datetime.now()
time = datetime.datetime.strftime(time, "%Y-%m-%d %H")
print(time)
print(dt)

