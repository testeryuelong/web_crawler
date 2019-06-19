# -*-coding:utf-8 -*-
# @Author : Zhigang

from Util.RaiseTime import *
from Util.GetLinkData import *
from Util.GetSinaLink import *
from ProjectVar.Var import *


def compositeData(categoryAndValidUrlDict):
    "组合数据，上传图片；并将插入数据库表中的数据组装好"
    htmlDataList = []
    for key, value in categoryAndValidUrlDict.items():
        for url in value:
            category = key
            create_time = RaiseTime.getTimeStamp()
            edit_time=RaiseTime.getTime()
            page = ParseHtml(url)
            title=page.getPageTitle()
            content=page.replaceImgSrcReturnContent()
            page.uploadImg()  # 上传图片
            htmlDataList.append([title, content, create_time,source,edit_time,category,author_id])
    return htmlDataList

