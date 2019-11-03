# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2019/4/15 9:46
desc:
'''

import re
import urllib.parse


def url_encode_special_char(string):

    # 模式(?!pattern), 零宽负向先行断言(zero-widthnegative lookahead assertion),代表字符串中的一个位置，紧接该位置之后的字符序列不能匹配pattern
    #'%'开始，但是后面两个字符不是数字，也不是字母
    string = re.sub("%(?![0-9a-fA-F]{2})","%25",string)
    string = string.replace("\\+", "%2B")

    return string


def encode_url_parameter(param_dict):
    for key,value in param_dict.items():
        value = url_encode_special_char(value)
        param_dict[key]=value

    encoded_url = urllib.parse.urlencode(param_dict)
    return encoded_url

def hit_string(target_str,str_list):
    """验证target_str是否在str_list中匹配到（字符串patial匹配）"""
    hit = False
    for str in str_list:
        if target_str in str:
            hit = True
            break
    return hit
