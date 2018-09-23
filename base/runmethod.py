# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 11:12:29 2018
@author: olivia
参考了慕课网Python接口自动化测试框架的部分实现
"""

import requests
#import globalvars as glo # why no module named 'globalvars'
import sys,logging
sys.path.append('..')
import base.globalvars as glo 


glo._init()#先必须在主模块初始化（只在Main模块需要一次即可）    

class RunMethod:
    def post_main(self,url,data,headers=None,verify=False,new_session=False):
        res = None
        if new_session:
            s = requests.Session()
            res = s.post(url=url,data=data,headers=headers,verify=verify)
        else :
            s = glo.get_value('Session') #获取全局变量Session
            res = s.post(url=url,data=data,verify=verify)
        #print("cookies for post")
        #print(s.cookies)
        glo.set_value('Session',s)
        #return res.json()
        return res

    def get_main(self,url,data=None,headers=None,verify=None,new_session=False):
        res = None
        if new_session:
            s = requests.Session()
            #s.proxies = {'http': ''}
            #print("header:%s"%headers)
            #res = s.get(url=url,data=data,headers=headers,verify=verify)
           
        else :
            s = glo.get_value('Session') #获取全局变量Session
            #print("header:%s"%s.headers)
        if headers is None:
            logging.debug("header parameter is None, session header is: ")
            logging.debug("header:%s"%s.headers)
            res = s.get(url=url,data=data,verify=verify)
        else:
            logging.debug("header parameter is:")
            logging.debug("header:%s"%headers)
            res = s.get(url=url,data=data,headers=headers,verify=verify)
        #print("logging level in runmethod:")
        #print(logging.getLogger().level)
        
        logging.debug("session cookie: ")
        logging.debug(s.cookies)
        glo.set_value('Session',s)
        
        #return res.json()
        return res

    def run_main(self,method,url,data=None,headers=None,verify=False,new_session=False):
        res = None
        if method.upper() == 'POST':
            res = self.post_main(url,data,headers,verify=verify,new_session=new_session)
        else:
            res = self.get_main(url,data,headers,new_session=new_session)
        #return json.dumps(res,ensure_ascii=False)
        #return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)
        return res
