import scrapy
import re

class GeteqlistSpider(scrapy.Spider):
    name = 'getEqlist'
    allowed_domains = ['news.ceic.ac.cn']
    start_urls = ['http://news.ceic.ac.cn/']

    def parse(self, response):
        html = response.body.decode(response.encoding)
        html = html.replace('\\t', '').replace('\\n', '').replace('\\r', '').replace(' ', '').replace('', '')
        ret = []
        eqrank = re.findall(r'<tdalign=\"center\"style=\"padding-left:20px\">([0-9.]+)<',html)
        eqtime = re.findall(r'<tdalign=\"center\"style=\"width:155px;\">([0-9:-]+)<',html)
        tmplist =re.findall(r'<tdalign=\"center\">([0-9.-]+)<',html)
        location = re.findall(r'>([\u4e00-\u9fff()（）]+)<\/a><\/td>',html)
        for i in range(len(eqtime)):
            eqtime[i] = eqtime[i][:10]+' ' +eqtime[i][10:]
        longitude,latitude,depth = list(),list(),list()
        for i in range(len(tmplist)):
            if(i%3==0):
                longitude.append(tmplist[i])
            elif(i%3==1):
                latitude.append(tmplist[i])
            else:
                depth.append(tmplist[i])

        ret = []
        for i in range(len(eqrank)):
            earthquake = {}
            earthquake['震级(M)'] = eqrank[i]
            earthquake['发震时刻(UTC+8)'] = eqtime[i]
            earthquake['纬度(°)'] = longitude[i]
            earthquake['经度(°)'] = latitude[i]
            earthquake['深度(千米)'] = depth[i]
            earthquake['参考位置'] = location[i]
            ret.append(earthquake)

        # print(ret)
        pass
