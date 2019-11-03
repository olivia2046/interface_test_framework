#!/user/bin/env python
# -*-coding:utf-8-*-
'''
@author: Patty
@project: automation_framework
@file: randomstr_util.py
@time: 2019/8/20  16:12
@IDE: PyCharm 
'''

import random
import string

"""随机生存类型（a-z,A-Z,0-9）指定长度的字符串"""


def random_char(i):
    return ''.join(random.choice(string.ascii_letters + string.digits) for j in range(i))
