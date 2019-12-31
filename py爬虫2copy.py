#导入网络请求模块
import requests
import re
#安装支持 解析html和XML的解析库 lxml 
from lxml import etree
import csv

#定义一个爬虫类
class MaoyanSpider(object):
    def __init__(self):
        self.base_url = 'https://maoyan.com/board/4?offset={}'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36','Cookie': '__mta=55336468.1575276247194.1575429940175.1575429949815.67; uuid_n_v=v1; uuid=E7B78CD014DF11EA89470DC982E4B91ECFCA10BF3408461BA112ABD91C5D9A67; _csrf=e687df883a654bb3067be748d197da5f9725b18ea44454f1d8cd6436370d1415; _lxsdk_cuid=16ec5c7f812c8-0497ce11b8200a-2393f61-1fa400-16ec5c7f813c8; _lxsdk=E7B78CD014DF11EA89470DC982E4B91ECFCA10BF3408461BA112ABD91C5D9A67; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1575276247,1575343232,1575344888,1575345850; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=55336468.1575276247194.1575377584185.1575429886423.65; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1575429950; _lxsdk_s=16eceeff2d2-ab-d81-971%7C%7C12'}

    #请求页面信息
    def get_pageInfo(self,url):
        response = requests.get(url=url,headers=self.headers)
        if response.status_code == 200:
            #用x_path转解析类型
            xpath_data = etree.HTML(response.content.decode('utf-8'))
            return xpath_data
        else:
            return None
            print(response.status_code)
    #设置10个页面的url
    def get_url(self):
        urls = []
        for i in range(0,100,10):
            urls.append(self.base_url.format(i))
        return urls
    #解析界面1
    def parse_pageInfo(self,html):
        infos = html.xpath('//dl[@class="board-wrapper"]/dd')
        results = []
        for info in infos:
            title = info.xpath('div/div/div[1]/p[1]/a/text()')[0]
            #strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。strip('主演：')去除首尾字符主演
            starring = info.xpath('div/div/div[1]/p[2]/text()')[0].strip().strip('主演：')
            pub_time = info.xpath('div/div/div[1]/p[3]/text()')[0].strip('上映时间：')
            score1 = info.xpath('div/div/div[2]/p/i[1]/text()')[0]
            score2 = info.xpath('div/div/div[2]/p/i[2]/text()')[0]
            score = str(score1) + str(score2)
            movie_url = 'https://maoyan.com'+info.xpath('a/@href')[0]
            result = self.parse_pageInfo2(movie_url,title,starring,pub_time,score)
            results.append(result)
        return results
    #解析界面2
    def parse_pageInfo2(self,movie_url,title,starring,pub_time,score):
        html2 = self.get_pageInfo(movie_url)
        print(html2)
        style = html2.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a')
        styles = ''
        for styl in style:
            styles = styles + styl.xpath('text()')[0].strip() + ','
        styles = styles.strip(',')
        long_time = html2.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[2]/text()')[0].split('/')[1].strip().strip('分钟')
        result0 = [title,starring,pub_time,score,styles,long_time]
        return result0
             
    #保存数据
    def save(self,data):
        with open('maoyan.csv','a',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
            # print(data)
          
    #保存爬虫内容
    #爬虫的所有逻辑结构都放在这里
    def run(self):
        urls = self.get_url()
        for url in urls:
            html = self.get_pageInfo(url)
            results = self.parse_pageInfo(html)
            for result in results:
                self.save(result)

    
if __name__ == '__main__':
    maoyanspider = MaoyanSpider()
    maoyanspider.run()