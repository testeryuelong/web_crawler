# -*-coding:utf-8 -*-
# @Author : Zhigang

import pymysql
from Util.RaiseTime import *

class DataBaseInit(object):

    """初始化数据库操作，向article表中插入爬取数据"""

    def __init__(self,host,port,dbName,username,password,charset):
        self.host=host
        self.port=port
        self.dbName=dbName
        self.username=username
        self.password=password
        self.charset=charset

    def __insertDatas(self,dataList):
        "插入多条数据,留作后面优化使用"
        try:
            # 连接mysql数据库中具体某个库
            conn = pymysql.connect(
                host = self.host,
                port = self.port,
                db = self.dbName,
                user = self.username,
                passwd = self.password,
                charset = self.charset
            )
            cur = conn.cursor()
            # 向测试表中插入多条测试数据
            sql = "insert into article(title,content,create_time,source,category,author_id) values(%s,%s,%s,%s,%s,%s);"
            res = cur.executemany(sql, dataList)
        except pymysql.Error as e:
            raise e
        else:
            conn.commit()
        cur.close()
        conn.close()

    def __insertData(self,data):
        "插入单条数据"
        try:
            # 连接mysql数据库中具体某个库
            conn = pymysql.connect(
                host = self.host,
                port = self.port,
                db = self.dbName,
                user = self.username,
                passwd = self.password,
                charset = self.charset
            )
            cur = conn.cursor()
            sql = "insert into article(title,content,create_time,source,edit_time,category,author_id) values(%s,%s,%s,%s,%s,%s,%s);"
            res = cur.execute(sql, data)
        except pymysql.Error as e:
            raise e
        else:
            conn.commit()
        cur.close()
        conn.close()

    def selectTodayArticles(self):
        "查询当日已插入数据的所有文章标题，以list形式返回"
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                db=self.dbName,
                user=self.username,
                passwd=self.password,
                charset=self.charset
            )
            cur = conn.cursor()
            cur.execute("select title from article t where t.edit_time like '{0}%';".format(RaiseTime.getToday()))
            dataExistsList=[]
            for i in cur.fetchall():
                # print (i)
                dataExistsList.append(i[0])
            return dataExistsList
        except pymysql.Error as e:
            raise e
        else:
            cur.close()
            conn.close()

    def run(self,dataList):
        "遍历爬取后的数据，与表中已存在的数据进行比对，如果已存在，则不执行插入动作；不存在则插入，避免重复插入"
        for id in range(len(dataList)):
            if dataList[id][0] not in self.selectTodayArticles():
                self.__insertData(dataList[id])

    def runThread(self,data):
        "多线程插入，功能同上"
        if data[0] not in self.selectTodayArticles():
            self.__insertData(data)

    def selectTodayData(self):
        "查询已插入的数据"
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                db=self.dbName,
                user=self.username,
                passwd=self.password,
                charset=self.charset
            )
            cur = conn.cursor()
            cur.execute("select * from article t where t.edit_time like '{0}%';".format(RaiseTime.getToday()))
            dataExistsList = []
            for i in cur.fetchall():
                print (i)
        except pymysql.Error as e:
            raise e
        else:
            cur.close()
            conn.close()

    def selectData(self):
        "查询已插入的数据"
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                db=self.dbName,
                user=self.username,
                passwd=self.password,
                charset=self.charset
            )
            cur = conn.cursor()
            cur.execute("select * from article")
            dataExistsList = []
            for i in cur.fetchall():
                print (i)
        except pymysql.Error as e:
            raise e
        else:
            cur.close()
            conn.close()

    def deleteData(self):
        "删除所有数据"
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                db=self.dbName,
                user=self.username,
                passwd=self.password,
                charset=self.charset
            )
            cur = conn.cursor()
            cur.execute("delete from article")
        except pymysql.Error as e:
            raise e
        else:
            conn.commit()
            cur.close()
            conn.close()

if __name__=="__main__":
    fire=DataBaseInit(host="127.0.0.1",
        port=2663,
        dbName="fireline",
        username="HuoxianYZG",
        password="HuoxianYZG",
        charset="utf8")
    # dataList=[("测试1","测试1",RaiseTime.getTimeStamp(),3,RaiseTime.getTime(),"新浪军事深度",8),
    #           ("测试2","测试2",RaiseTime.getTimeStamp(),3,RaiseTime.getTime(),"新浪军事深度",8),
    #           ("测试3","测试2",RaiseTime.getTimeStamp(),3,RaiseTime.getTime(),"新浪军事深度",8),
    #           ("测试4","测试2",RaiseTime.getTimeStamp(),3,RaiseTime.getTime(),"新浪军事深度",8),
    #           ("测试5","测试2",RaiseTime.getTimeStamp(),3,RaiseTime.getTime(),"新浪军事深度",8),]
    # print (fire.selectTodayArticles())
    # print(fire.selectTodayData())
    # fire.run(dataList)
    # fire.deleteData()
    fire.selectData()


