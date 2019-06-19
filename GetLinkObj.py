# -*-coding:utf-8 -*-
# @Author : Zhigang

import re
import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from Util.GetSinaLink  import *
from Util.RaiseTime import  *
from ProjectVar.Var import *
from requests_toolbelt import MultipartEncoder

def getLinkObj(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")  # html可以是html内容
    soupStr = repr(soup)  # 匹配正则使用
    title = soup.title.string.split("|")[0]
    # 爬取正文开始至结束
    content = re.search(r'<!-- 正文 start -->\n<div class="article" id="article">([\s\S]*)<!-- 正文 end -->',
                        soupStr).group()

    content=re.sub(r"<!--\s*.*\s*-->","",content)  # \s*匹配若干空格，去掉单行注释
    # print((content))
    # print (content.split("\n"))
    # for line in content.split("\n"):
    #     print (line)
    # 过滤具体规则
    result=[]
    Flag = True
    for part in content.split("\n"):
        if part=="":
            continue
        elif part=="<!--" and Flag==True:
            Flag = False
            continue
        elif part=="-->" and Flag ==False:
            Flag =True
            continue
        if part and Flag==True:
            result.append(part)
    content="\n".join(result)
    # 预留出图片
    print(soup.select("div.img_wrapper > img"))
    imgObjList = soup.select("div.img_wrapper > img")
    # print (imgObjList)
    imgUrlList = []
    # 将拼接好的图片路径添加到列表中,用于读取文件流；
    # 取出原来的图片路径（除图片名）替换成我们自己的：https://zhigang.com/Crawling_Img/
    if imgObjList:
        for imgObj in imgObjList:
            print (imgObj["src"])
            oldUrl=imgObj["src"]
            needReplaceUrl="/".join(imgObj["src"].split("/")[:-1])
            print (needReplaceUrl)
            imgUrl = "http:" + imgObj["src"]
            imgUrlList.append(imgUrl)

    for imgUrl in imgUrlList:
        print(imgUrl)
        # print(imgUrl.split("/"))
        # 图片名称
        photoName = imgUrl.split("/")[-1]
        fireUrl="https://zhigang.com/Crawling_Img/"
        newUrl=fireUrl+photoName
        print (newUrl)
        print(photoName)
        # 读取图片并保存在本地
        photoBinaryformat  = (urllib.request.urlopen(imgUrl)).read()  # 单一图片文件文件流，还需要上传文件名；直接调用接口传；批量上传需要保存为列表形式
        # print (photoBinaryformat)
        # with open(photoName, "wb") as fp:
        #     fp.write(photoBinaryformat)
        url="http://zhigang/api/upload/upImg"
        # fields ={"file":(photoName,open(photoName, "rb"))}
        fields = {"file": (photoName, photoBinaryformat)}
        res=requests.post(url,files =fields)
        print (res.request.headers)
        print(res.request.body)
        print (res.status_code)
        print (res.text)
        # print (photoBinaryformat) # 图片文件流

    # return title, content
    content=content.replace(oldUrl,newUrl)
    # print (content)

    # http://zhigang/api/upload/upImg 上传图片接口

if __name__=="__main__":
    url="https://mil.news.sina.com.cn/world/2019-03-14/doc-ihsxncvh2372317.shtml"
    url1="https://mil.news.sina.com.cn/dgby/2019-03-18/doc-ihsxncvh3342391.shtml"
    getLinkObj(url)

