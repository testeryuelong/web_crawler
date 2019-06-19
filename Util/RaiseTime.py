# -*-coding:utf-8 -*-
# @Author : Zhigang

import time

class RaiseTime(object):

    @classmethod
    def getTimeStamp(cls):
        "用在插入数据库中的时间戳"
        return int(time.time())

    @classmethod
    def getTime(cls):
        "用在插入数据库中的edit_time,用于比较"
        return time.strftime("%Y%m%d%H%M%S")

    @classmethod
    def getToday(cls):
        "用在比对数据库中的当天插入数据"
        return time.strftime("%Y%m%d")

    @classmethod
    def getCurrent(cls):
        "用在比对url日期"
        return time.strftime("%Y-%m-%d",time.localtime())

if __name__=="__main__":
    print (RaiseTime.getTimeStamp())
    print (RaiseTime.getToday())
    print (RaiseTime.getCurrent())