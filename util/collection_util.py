# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2018/11/23 15:20
desc:
'''
import random


def random_select_from_list(input_list,n=0): #Todo: 可指定返回结果的元素个数？
    if len(input_list)==1:
        return input_list[0]
    else:
        result = []
        if n==0: #未指定需返回的元素个数
            n = random.randint(1,len(input_list))  #随机选定返回结果的元素个数
        for i in range(n):
            result.append(input_list[random.randint(0, len(input_list)-1)])

        return result


 