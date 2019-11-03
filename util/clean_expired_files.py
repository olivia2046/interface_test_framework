# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2019/8/9 16:52
desc: https://www.cnblogs.com/changbo/p/5595030.html
'''

import os,datetime,time

def delfile(folder,days):
    """

    :param folder:需要清理的文件夹
    :param days: 天数，超过该天数的文件将被清理
    :return:
    """
    f = list(os.listdir(folder))
    print("开始清理%s文件夹下超过%s天的文件...." %(folder,days))
    for i in range(len(f)):
        filedate = os.path.getmtime(folder + os.sep+ f[i])
        time1 = datetime.datetime.fromtimestamp(filedate).strftime('%Y-%m-%d')
        date1 = time.time()
        num1 = (date1 - filedate) / 60 / 60 / 24
        if num1 >= days:
            try:
                os.remove(folder +os.sep + f[i])
                print(u"已删除文件：%s ： %s" % (time1, f[i]))
            except Exception as e:
                print(e)
    else:
        print("......")

 