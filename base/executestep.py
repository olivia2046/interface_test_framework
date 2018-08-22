# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 13:59:53 2018

@author: olivia
"""
import sys
sys.path.append('..')
from base.runmethod import RunMethod
from util.json_util import JsonUtil

class ExecuteStep():
    
    def execute(self,casedata):
        url = casedata['URL']
        if casedata['是否携带header'].upper()=='Y':
            header_label = casedata['header内容']
            jutil = JsonUtil('../data/headers.json')
            header = jutil.get_data(header_label)
        else:
            header = None
        
        
        
        #获取case依赖数据
        if casedata['case依赖'] !='':#casedata已先期将None替换为''
            depend_case = casedata['case依赖']
            depend_response_data = depend_case
                  
         
        if casedata['新会话'].upper()=='Y':
            new_session=True
        else :
            new_session=False
            
        data = []
        if casedata['请求数据']!='':
            
            data_label = casedata['请求数据']
            jutil = JsonUtil('../data/data.json')
            data = jutil.get_data(data_label)
        print("data:")
        print(data)
        res = RunMethod().run_main(method=casedata['请求类型'],url=url,data=data,headers = header,verify=False,new_session=new_session)
        
        return res