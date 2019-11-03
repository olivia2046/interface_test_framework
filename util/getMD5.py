# -*- coding: utf-8 -*-
'''
作者：cn.Dixon
来源：CSDN
原文：https://blog.csdn.net/weixin_39553910/article/details/82774771?utm_source=copy
Created on: 2018/10/16 14:58
desc:
'''

import hashlib

def md5_convert(string):
    """
    计算字符串md5值
    :param string: 输入字符串
    :return: 字符串md5
    """
    m = hashlib.md5()
    m.update(string.encode())
    return m.hexdigest()

def get_file_md5(file_path):
    """
    获取文件md5值
    :param file_path: 文件路径名
    :return: 文件md5值
    """
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
    return str(_hash).upper()

#print (get_file_md5(r'F:\测试数据\威华-华泰-2018-07-11.pdf'))