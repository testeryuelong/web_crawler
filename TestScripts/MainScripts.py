# -*-coding:utf-8 -*-
# @Author : Zhigang

from Util.DataBaseInit import *
from Util.CompositeData import *
from multiprocessing.dummy import Pool

def getData(url):
    start = time.time()
    sina = GetSinaLink(url)
    validLink=sina.getValidLink()
    dataList = compositeData(validLink)
    end = time.time()
    return dataList,"耗费时间为%s" % (end-start)

def main(dataList):
    start=time.time()
    fire = DataBaseInit(host="127.0.0.1",
                        port=2663,
                        dbName="fireline",
                        username="HuoxianYZG",
                        password="HuoxianYZG",
                        charset="utf8")
    pool = Pool(5)
    pool.map(fire.runThread, dataList)
    pool.close()
    pool.join()
    end=time.time()
    fire.selectData()  # 查看插入数据
    print ("插入数据库耗费时间为%s" % (end-start))


if __name__=="__main__":
    url = "https://mil.news.sina.com.cn/"
    dataList,elapsedTime=getData(url)
    print ("获取数据耗费时间为%s" % elapsedTime)
    main(dataList)

