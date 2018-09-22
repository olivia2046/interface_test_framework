# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 08:00:48 2018

@author: olivia
"""

import unittest
import pandas as pd
import sys,os,time
from jsonpath_rw import jsonpath,parse
sys.path.append('..')
from util import ddt
from base.executestep import ExecuteStep
from config.get_config import get_testcase_file


datafrm = pd.read_excel(get_testcase_file())
datafrm = datafrm.fillna('')
testdata = []
datafrm.apply(lambda x:testdata.append(x.to_dict()),axis=1)
#print(testdata)


@ddt.ddt
class InterfaceTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    @ddt.data(*testdata)
    def test_interface(self, casedata):
        '''测试接口'''
        
        if casedata['是否运行'].upper()=='Y': #如果未标注运行，则该testcase跳过
            #print("运行")

            res = ExecuteStep().execute(casedata)
            
            # 调试输出resonse文本
            if not os.path.exists('../report'):
                os.makedirs('../report')
            now=time.strftime("%Y-%m-%d %H_%M_%S",time.localtime())
            with open(r'../report/ResponsePage-%s.html'%now,'w',encoding='utf8') as f:
                f.write(res.text)
            #print("reason：%s"%res.reason)
            #print("response code:%s"%res.status_code)
            #print("response headers:%s"%res.headers)
            expected_status_code = casedata['期望响应代码']
            self.assertEqual(res.status_code,expected_status_code, 'Status Code not as expected!')
            
            expected_res_txt = casedata['期望响应文本']
            if expected_res_txt!="":
                eval("self."+ casedata['对比方法'])(expected_res_txt,res.text, 'Response text not as expected!')
            
            #print("response text:")
            #print(res.text)
            expected_json = casedata['期望返回Json内容']
            if expected_json!="":
                try:
                    json_obj = res.json()
                    print(json_obj)
                    for path in expected_json.split(','):
                        print(path)
                        jsonpath_expr = parse(path)
                        match = jsonpath_expr.find(json_obj)
                        #self.assertIsNotNone(match,"json path not found!")
                        self.assertNotEqual(match,[],"json path not found!")
                        (match,"json path not found!")
                        print(match)
                except Exception as e:
                    self.assertEqual(1,0,"no json object for the response!") # fails the test
              
           
        
    
    def tearDown(self):
        pass