# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 13:59:53 2018

@author: olivia
"""
import sys
sys.path.append('..')
from base.runmethod import RunMethod
from base.dependent_data import DependentData
from util.json_util import JsonUtil
import main.globalvars as glo


class ExecuteStep():
    
    def execute(self,casedata):
        print(casedata)
        url = casedata['URL']
        if casedata['是否携带header'].upper()=='Y':
            header_label = casedata['header内容']
            #jutil = JsonUtil('../data/headers.json')
            jutil = JsonUtil(glo.header_file)
            header = jutil.get_data(header_label)
        else:
            header = None
        
        #获取case依赖数据
        if casedata['case依赖'] !='':#casedata已先期将None替换为''
            depend_data = DependentData(casedata['case依赖'])
            execute(depend_data)
            #depend_response_data = casedata['case依赖']
                  
         
        if casedata['新会话'].upper()=='Y':
            print("新会话~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            new_session=True
        else :
            print("保持会话~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
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