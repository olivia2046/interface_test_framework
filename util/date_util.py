# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2018/10/18 17:37
desc:
'''

import base.globalvars as glo
from datetime import datetime
from dateutil.relativedelta import *
import time,logging


def get_datetime_from_now(floor_time = False, format="%Y-%m-%d %H:%M:%S", **kwargs):
    '''

    获取距离今天给定时间段的日期
    to be called in excel test case, like in the parameter
    part of URL as below:
    ?start=${get_date_from_today(-7)}&end=${get_date_from_today(0)}
    参数：
        floor_time: 时间向下取整到零时
        format:返回的时间字符串格式
        kwargs:可变参数，支持years, months, days, leapdays, weeks,
                 hours, minutes, seconds, microseconds（与dateutil中的relativedelta类的构造函数参数对应）
                 正数代表当前时间之后的时间，负数代表当前时间之前的时间
    '''

    for key in kwargs.keys():
        if key not in ['years', 'months', 'days', 'leapdays', 'weeks',
                 'hours', 'minutes', 'seconds', 'microseconds']:
            logging.error("params error! %s not a legal parameter"%key)
            return
    date_time = datetime.now() + relativedelta(**kwargs)
    if floor_time:
        time_tuple = date_time.timetuple()
        time_obj =  time.mktime(time_tuple)
        timestamp = time_obj - time_obj % 86400 # 用时间戳减去时间戳对24小时取的余数，即时间戳的整数
        return datetime.utcfromtimestamp(timestamp).strftime(format) #fromtimestamp转换为Local time，此处需要的是0时的字符串，因此用utcfromtimestamp
    else:
        return date_time.strftime(format)

def wait(seconds=5):
    time.sleep(seconds)

def get_current_timestamp(n=0,convert_str=False,get_round=False):
    """

    :param n: 需乘以10的n次方
    :param convert_str: 是否需要转换为字符串
    :return:
    """
    result = time.time()*pow(10,n)
    if get_round:
        result = round(result)

    if convert_str:
        result =  str('{:.0f}'.format(result)) #大整数取消科学计数法显示

    glo.set_value("timestamp",result)
    return result

def datetime_roundly_equal(inbound,outbound,format_str):
    """

    :param inbound: 接口输入的日期时间字符串
    :param outbound: 接口返回的日期时间字符串
    :format_str: 日期时间的格式字符串，如‘%Y-%m-%dT%H:%M:%S.%f%z’
    :return: inbound四舍五入是否等于outbound
    """
    inbound_datetime = datetime.strptime(inbound,format_str)
    outbound_datetime= datetime.strptime(outbound,format_str)
    inbound_timestamp = inbound_datetime.timestamp()
    outbound_timestamp = outbound_datetime.timestamp()

    return round(inbound_timestamp==outbound_timestamp)