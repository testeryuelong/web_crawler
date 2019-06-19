# -*-coding:utf-8 -*-
# @Author : Zhigang

import re
import urllib
import requests
from bs4 import BeautifulSoup
from lxml import etree


class ParseHtml(object):

    """解析网页，获取元素"""

    def __init__(self,url,header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}):
        "初始化访问url,获取网页源码"
        self.url=url
        self.header=header
        html = requests.get(self.url,headers=self.header)
        self.soup = BeautifulSoup(html.content, "html.parser")

    def getPageSource(self):
        "返回soup对象"
        return self.soup

    def getPageTitle(slef):
        "获取网页文章标题，返回字符串"
        title = slef.soup.title.string.split("|")[0]
        return title

    def getArticle(self):
        "用xpath解析，优势：速度快；只获取文章部分，去掉多余的内容"
        res = requests.get(self.url,headers =self.header)
        html_doc = res.content.decode("utf-8")
        selector = etree.HTML(html_doc)
        info = selector.xpath('//div[@class="article"]')[0]
        article = etree.tostring(info, encoding='utf-8')
        article = article.decode("utf-8")
        article = re.sub(r"<!--\s*.*\s*-->", "", article)
        return article

    # def getArticleBody(self):
    #     "获取文章主体部分，返回字符串"
    #     soupStr = repr(self.getPageSource())
    #     articleBody = re.search(r'<!-- 正文 start -->\n<div class="article" id="article">([\s\S]*)<!-- 正文 end -->',
    #                         soupStr).group()
    #     # articleBody = re.sub(r"<!--\s*.*\s*-->", "", articleBody)  # \s*匹配若干空格，去掉单行注释
    #     # articleBody = re.sub(r"<!--(.*?)-->","",articleBody,flags=re.S)  # 去掉多行注释
    #     with open("3.txt","w",encoding="utf-8") as fp:
    #         fp.write(articleBody)
    #     return articleBody

    def getFilterArticle(self):
        "过滤规则，目前是用来过滤多行注释，后期针对需求主要对此函数进行扩展;返回过滤后的文章主体"
        article=self.getArticle()
        content = []
        Flag = True
        for part in article.split("\n"):
            if part == "":
                continue
            elif part == "<!--" and Flag == True:
                Flag = False
                continue
            elif part == "-->" and Flag == False:
                Flag = True
                continue
            if part and Flag == True:
                content.append(part)
        content = "\n".join(content)
        return content

    def getImgSrc(self):
        "获取网页源码中指定路径下的图片，通过css方式获取，返回图片路径列表"
        soup=self.getPageSource()
        imgObjList = soup.select("div.img_wrapper > img")
        imgSrc = []
        if imgObjList:
            for imgObj in imgObjList:
                imgSrc.append(imgObj["src"])
        return imgSrc

    def replaceImgSrcReturnContent(self,fireUrl="https://zhigang.com/Crawling_Img/"):
        "将文章主体中的原图片路径替换为火线保存路径,返回最终插入数据"
        content = self.getFilterArticle()
        imgSrc=self.getImgSrc()
        for imgPath in imgSrc:
            oldPath = imgPath
            newPath = fireUrl + imgPath.split("/")[-1]
            content=content.replace(oldPath,newPath)
        return content

    def uploadImg(self,url="http://127.0.0.1/api/upload/upImg"):
        "将网页中的图片名称和文件流--二进制形式，上传至服务器,实现multipart/form-data 来提交请求"
        imgSrc = self.getImgSrc()
        successImgNum=0
        for imgPath in imgSrc:
            photoName = imgPath.split("/")[-1]
            imgUrl = "http:"+imgPath  # 拼接绝对路径
            photoBinaryformat = (urllib.request.urlopen(imgUrl)).read()  # 获取文件流
            fields = {"file": (photoName, photoBinaryformat)}
            res = requests.post(url, files=fields)
            if res.text:
                successImgNum+=1
        if successImgNum == len(imgSrc):
            print ("%s:上传文章图片成功,共%s张" % (self.url,len(imgSrc)))


if __name__=="__main__":
    url1="https://mil.news.sina.com.cn/dgby/2019-03-18/doc-ihsxncvh3342391.shtml"
    page=ParseHtml(url1)
    # page.uploadImg()
    # content=page.replaceImgSrcReturnContent()
    # for line in content.split("\n"):
    #     print (line)
    # print (page.getPageTitle())
    # print (page.getFilterArticle())
    # print (page.getArticle())
    print (page.replaceImgSrcReturnContent())