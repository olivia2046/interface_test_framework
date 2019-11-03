# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2019/6/24 11:43
desc: 自定义decorator
'''
from base.get_config import get_run_case_level
import functools
import time,unittest,logging
from unittest import SkipTest


def case_level_decorator(func,case_level):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if case_level in get_run_case_level() or get_run_case_level()==[]:
            return func(*args, **kwargs)
        else:
            raise unittest.SkipTest("case level not included") # case真正跳过，不会被统计为pass
    return wrapper

def Smoke(func):
    return case_level_decorator(func,"Smoke")

def Sanity(func):
    return case_level_decorator(func,"Sanity")

def Regression(func):
    return case_level_decorator(func, "Regression")

def retry(times=3,wait_time=10):
    def wrap_func(func):
        @functools.wraps(func) # 需要把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错
        def failed_retry(*args,**kwargs):
            for idx in range(times):
                try:
                    func(*args,**kwargs)
                    return
                except SkipTest: #如果是跳过执行，则仍抛出异常（目的是该用例不纳入report），退出循环
                    raise unittest.SkipTest("case set not to run")

                except Exception as e:
                    if idx==times-1: #最后一次则抛出异常
                        raise
                    else:
                        logging.info("Failure. Retrying...\n%s"%e)
                        time.sleep(wait_time)


        return failed_retry
    return wrap_func


