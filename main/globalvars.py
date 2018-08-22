# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 08:23:02 2018
参考; https://www.cnblogs.com/suwings/p/6358061.html
利用global的单独文件全局性，从而可以定义在一个文件中的全局变量，
然后这个单个文件的全局变量可以保存多个文件的共同全局变量
"""


def _init():#初始化
    global _global_dict
    _global_dict = {}


def set_value(key,value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def get_value(key,defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
    
global testcase_file
#@ToDo: 需要获取文件完整路径，否则在不同级别路径下获取路径变量值，得到的路径不同
testcase_file = "../case/testcase.xlsx"
global header_file
header_file = "../data/headers.json"
global cookie_file
cookie_file = '../dataconfig/cookie.json'