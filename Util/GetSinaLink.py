# -*-coding:utf-8 -*-
# @Author : Zhigang

import re
import requests
from Util.RaiseTime import *

class GetSinaLink(object):

    """获取新浪军事的当天最新军事新闻"""

    def __init__(self,sourceUrl,header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}):
        self.sourceUrl=sourceUrl
        self.header=header
        self.jssdList = []  # 军事深度
        self.chinaList = []  # 中国军情
        self.dgbyList = []  # 大国博弈
        self.worldList = []  # 世界军情
        self.historyList = []  # 军事历史
        self.summaryDict=\
            {"新浪,军事深度":self.jssdList,
             "新浪,中国军情":self.chinaList,
             "新浪,大国博弈":self.dgbyList,
             "新浪,世界军情":self.worldList,
             "新浪,军事历史":self.historyList
             }

    def getAllLink(self):
        "使用正则匹配出所有的网址链接"
        html = requests.get(self.sourceUrl,headers =self.header)
        pattern = re.compile(r'href="(.*?)"')
        linkList = pattern.findall(html.text)
        return linkList

    def getValidLink(self):
        "获取当天日期的链接，返回字典形式，key为数据表中的category，value为url列表"
        linkList=self.getAllLink()
        for link in linkList:
            if re.search(r"/jssd/%s/" % RaiseTime.getCurrent(), link):
            # if re.search(r"/jssd/%s/" % "2019-03-15", link): # 测试代码
                self.jssdList.append(link)
            elif re.search(r"/china/%s/" % RaiseTime.getCurrent(), link):
                self.chinaList.append(link)
            elif re.search(r"/dgby/%s/" % RaiseTime.getCurrent(), link):
                self.dgbyList.append(link)
            elif re.search(r"/world/%s/" % RaiseTime.getCurrent(), link):
                self.worldList.append(link)
            elif re.search(r"/history/", link):
                self.historyList.append(link)
        return self.summaryDict

if __name__=="__main__":
    # 访问要爬取的网站
    url = "https://mil.news.sina.com.cn/"
    sina=GetSinaLink(url)
    print (sina.getValidLink())
    for key,value in sina.getValidLink().items():
        for url in value:
            print ("%s:%s" % (key,url))