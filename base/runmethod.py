# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 11:12:29 2018
@author: olivia
参考了慕课网Python接口自动化测试框架的部分实现
"""

import requests
import json
import sys
sys.path.append('..')
import main.globalvars as glo

class RunMethod:
    def post_main(self,url,data,headers=None,verify=False,new_session=False):
        res = None
        if new_session:
            s = requests.Session()
        else :
            s = glo.get_value('Session') #获取全局变量Session
        print("cookies for post")
        print(s.cookies)
        res = s.post(url=url,data=data,headers=headers,verify=verify)
        glo.set_value('Session',s)
        #return res.json()
        return res

    def get_main(self,url,data=None,headers=None,verify=False,new_session=False):
        res = None
        if new_session:
            s = requests.Session()
        else :
            s = glo.get_value('Session') #获取全局变量Session       
        res = s.get(url=url,data=data,headers=headers)
        print("set session~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        glo.set_value('Session',s)
        
        #return res.json()
        return res

    def run_main(self,method,url,data=None,headers=None,verify=False,new_session=False):
        res = None
        if method.upper() == 'POST':
            print("Posting~~~~~~~~~~~~~~~~~~~~~~")
            res = self.post_main(url,data,headers,verify=verify,new_session=new_session)
        else:
            print("Getting~~~~~~~~~~~~~~~~~~~~~~")
            res = self.get_main(url,data,headers,verify=verify,new_session=new_session)
        #return json.dumps(res,ensure_ascii=False)
        #return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)
        return res
