# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 20:55:06 2018

@author: olivia
"""

import unittest
import ddt
import pandas as pd
import requests
#import HTMLTestRunner
import sys
sys.path.append('..')
from util.json_util import JsonUtil
from base.runmethod import RunMethod
import globalvars as glo


#datafrm = pd.read_excel('testcase.xlsx').drop(columns=['CaseId','Desc'])
datafrm = pd.read_excel('../case/testcase.xlsx')
datafrm = datafrm.fillna('')
testdata = []
datafrm.apply(lambda x:testdata.append(x.to_dict()),axis=1)
#print(testdata)


@ddt.ddt
class EndPointTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    @ddt.data(*testdata)
    def test_interface(self, casedata):
        if casedata['是否运行'].upper()=='Y': #如果未标注运行，则该testcase跳过
            
            url = casedata['URL']
            if casedata['是否携带header'].upper()=='Y':
                header_label = casedata['header内容']
                jutil = JsonUtil('../data/headers.json')
                header = jutil.get_data(header_label)
            else:
                header = None
            
            '''
            
            #获取case依赖数据
            if casedata['case依赖'] !='':#casedata已先期将None替换为''
                depend_case = casedata['case依赖']
                depend_response_data = depend_case
                      
            ''' 
            if casedata['新会话'].upper()=='Y':
                new_session=True
            else :
                new_session=False
            data_label = casedata['请求数据']
            jutil = JsonUtil('../data/data.json')
            data = jutil.get_data(data_label)
            res = RunMethod().run_main(method=casedata['请求类型'],url=url,data=data,headers = header,verify=False,new_session=new_session)
            print("response code:%s"%res.status_code)
            #print("response headers:%s"%res.headers)
            expected_status_code = casedata['期望响应代码']
            expected_res_txt = casedata['期望响应文本']
            self.assertEqual(res.status_code,expected_status_code, 'Status Code not as expected!')
            #self.assertIn(expected_res_txt,res.text, 'Response text not as expected!')
            
            
            #print(res.text)
        
    
    def tearDown(self):
        pass
    
    
if __name__=='__main__':
    
    unittest.main()