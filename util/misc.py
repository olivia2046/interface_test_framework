# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2018/12/6 16:42
desc:
'''
import random

def convert_number_to_chinese(keyword):
    num_to_ch_dict = {'1':'一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '0': '零'}
    for char in keyword:
        if char in num_to_ch_dict.keys():
            keyword = keyword.replace(char, num_to_ch_dict[char])
    return keyword


def random_partial_string(input_str):
    length = len(input_str)
    start = random.randint(0,length - 2)
    end = random.randint(start + 1, length - 1)
    return input_str[start:end]


def is_list(obj):
    if isinstance(obj, list):
        return True
    else:
        return False

def gen_id(prefix=""):
    '''生成id标识'''

    pass
