# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 13:59:53 2018

@author: olivia
"""
import sys,re
from jsonpath_rw import jsonpath,parse
sys.path.append('..')
from base.runmethod import RunMethod
from util.json_util import JsonUtil
from base.getdata import GetData
from config.get_config import get_header_file,get_data_file


class DependentData:
    def __init__(self,case_id):
        self.case_id = case_id
        #self.data = GetData()
        self.depend_case_data = None

    #执行依赖测试，获取结果
    def run_dependent(self):

        #通过case_id去获取该case_id的整行数据
        #print("run dependent case: %s"%self.case_id)
        self.depend_case_data = GetData().get_case_data(self.case_id)
        #print("self.depend_case_data")
        #print(self.depend_case_data)
        res = ExecuteStep().execute(self.depend_case_data)
        return res
        

    #根据依赖的key去获取执行依赖测试case的响应,然后返回
    def get_data_for_case(self,case_data):
        depend_data = case_data['Post Data依赖的返回数据']
        depend_url = case_data['URL后缀依赖的返回数据']
        response_data = self.run_dependent()
        
#        with open('loginpage.html','wt',encoding='utf8') as f:
#            f.write(response_data.text)
            
        #获取依赖数据的key
        #print("dependent data: %s"%depend_data) 
        #print("dependent case response_data:")
        #print(response_data.text)
        if depend_data.startswith('json:'):
            json_exe = parse(depend_data.replace('json:'),'')
            madle = json_exe.find(response_data)
            return [math.value for math in madle][0]
        elif depend_data.startswith('html:'):
            pattern = re.compile(depend_data.split(':')[1])#取中间的字符串
            matches = re.findall(pattern,response_data.text)
            #print(matches)
            indice = int(depend_data.split(':')[2])
            dependent_value = matches[indice] #到底应该取第一个还是第二个？
            #print("dependent value:%s"%dependent_value)
            return dependent_value
        
        #if depend_url = 
    
class ExecuteStep():
    
    def execute(self,casedata):
        #print(casedata)

        if casedata['指定header'].upper()=='Y':
            header_label = casedata['header内容']
            jutil = JsonUtil(get_header_file())
            header = jutil.get_data(header_label)
        else:
            header = None

        data = []
        if casedata['请求数据']!='':            
            data_label = casedata['请求数据']
            jutil = JsonUtil(get_data_file())
            data = jutil.get_data(data_label)
        
        #获取case依赖数据
        if casedata['case依赖'] !='':#casedata已先期将nan替换为''
            depend_data = DependentData(casedata['case依赖'])
            #value = depend_data.get_data_for_key(casedata['依赖的返回数据'])
            #依赖的返回数据可能不止一处，返回的json数据，返回的html页面的一部分(authenticity_token， 如果要动态操作repository，则url也依赖返回的html页面元素)
            value = depend_data.get_data_for_case(casedata) 
            field = casedata['数据依赖字段']
            data[field] = value            
        
        url = casedata['URL']
           
        if casedata['新会话'].upper()=='Y':
            #print("新会话~~~~~~~~~~~~~~~~~~~~~~~~")
            new_session=True
        else :
            #print("保持会话~~~~~~~~~~~~~~~~~~~~~~")
            new_session=False
            
        #print("data:")
        #print(data)
        res = RunMethod().run_main(method=casedata['请求类型'],url=url,data=data,headers = header,verify=False,new_session=new_session)
        return res