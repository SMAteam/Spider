#-*- coding = utf-8 -*-
# da = []
# if da==[]:
#     print("空")
# li ="知道"
# print(len(li))
import re
str = "原标题：《注意！这些路段塌方、落石、封闭！》,　　近期,受强降雨影响极易发生滑坡塌方、落石等自然灾害,造成安全隐患,为方便群众安全出行,现对淅川县、西峡县部分道路受灾及施工情况通告如下：,　,　淅川县"
str1 = re.sub('原标题：[【】《》！、，。,\u4e00-\u9fff]+\s+','',str)
str2 ="原标题：【群测群防】重庆“四重”网格化防灾体系避免人员伤亡,来源:重庆发布"
str3 =  re.sub('原标题：[【】“”《》！、，。,\u4e00-\u9fff]+\s+','',str2)
# str4 = "齐鲁早报|山东发布山洪灾害预警！涉及潍坊临沂等6市"
str4 = "@齐鲁8，山东发布山洪灾害预警！涉及潍坊临沂等6市"
str5 = re.sub('(([\u4e00-\u9fff]+网[\u4e00-\u9fff]*[\|:，：,。！.]*)|([\u4e00-\u9fff]+早报[\|:，：,。！.]*)|([\u4e00-\u9fff]+资讯[\|:，：.,。！]*)|([\u4e00-\u9fff]+晚报[\|:，：,。！]*)|(@[\u4e00-\u9fff]+[\|:，：.,。！]*))','',str4)
print(str5)
print(str3)
str6 = "sda/sda_2019-____地震-wqe<>d.shtml"
str7 = re.findall('sda/([a-zA-Z0-9\u4e00-\u9fff_-]+)',str6)
print(str7)
import datetime
print(datetime.datetime.now().hour+1)

