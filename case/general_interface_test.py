# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 08:00:48 2018

@author: olivia
"""

import unittest
import ddt
import pandas as pd
import sys,time
sys.path.append('..')
from base.executestep import ExecuteStep
import main.globalvars as glo

#glo._init()#先必须在主模块初始化（只在Main模块需要一次即可）
#datafrm = pd.read_excel('../case/testcase.xlsx')
datafrm = pd.read_excel(glo.testcase_file)
datafrm = datafrm.fillna('')
testdata = []
datafrm.apply(lambda x:testdata.append(x.to_dict()),axis=1)
#print(testdata)


@ddt.ddt
class InterfaceTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    @ddt.data(*testdata)
    #@ddt.data({'CaseId': 'github-001', 'Case_Name': 'get_login_page', '概要': '获取登录页面，返回页面的隐藏字段包含后面登录需要的token', '是否运行': 'Y', '新会话': 'Y', 'Site Specific': '', 'case依赖': '', '依赖的返回数据': '', '数据依赖字段': '', 'URL': 'https://github.com/login', 'URL后缀依赖的返回数据': '', '请求类型': 'GET', '指定header': 'Y', 'header内容': 'header1', '请求数据': '', '期望响应代码': 200.0, '期望响应文本': 'Sign in to GitHub'})
    #@ddt.unpack
    def test_interface(self, casedata):
        '''测试接口'''
        
        if casedata['是否运行'].upper()=='Y': #如果未标注运行，则该testcase跳过

            res = ExecuteStep().execute(casedata)
            
            now=time.strftime("%Y-%m-%d %H_%M_%S",time.localtime())
            with open(r'../report/ResponsePage-%s.html'%now,'w',encoding='utf8') as f:
                f.write(res.text)
            #print("reason：%s"%res.reason)
            print("response code:%s"%res.status_code)
            #print("response headers:%s"%res.headers)
            expected_status_code = casedata['期望响应代码']
            expected_res_txt = casedata['期望响应文本']
            self.assertEqual(res.status_code,expected_status_code, 'Status Code not as expected!')
            #self.assertRegexpMatches(expected_res_txt,res.text, 'Response text not as expected!')
            #self.assertIn('302',res.headers['Status'], 'Response status not as expected!')
            #validate(self,casedata['对比方法'],expected_res_txt,res.text, 'Response text not as expected!')
            eval("self."+ casedata['对比方法'])(expected_res_txt,res.text, 'Response text not as expected!')

     
            
            #print(res.text)
        
    
    def tearDown(self):
        pass