# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 08:00:48 2018

@author: olivia
"""


import pandas as pd
import sys,os,time,logging
from jsonpath_rw import jsonpath,parse
import unittest
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
            '''
            if not os.path.exists('../report'):
                os.makedirs('../report')
            now=time.strftime("%Y-%m-%d %H_%M_%S",time.localtime())
            with open(r'../report/ResponsePage-%s.html'%now,'w',encoding='utf8') as f:
                f.write(res.text)
            '''
            logging.debug("reason：%s"%res.reason)
            logging.debug("response code:%s"%res.status_code)
            logging.debug("response headers:%s"%res.headers)
            expected_status_code = casedata['期望响应代码']
            self.assertEqual(res.status_code,expected_status_code, 'Status Code not as expected!')
            #res.raise_for_status()

            
            expected_res_txt = casedata['期望响应文本']
            if expected_res_txt!="":
                eval("self."+ casedata['对比方法'])(expected_res_txt,res.text, 'Response text not as expected!')
            
            #print("response text:")
            #print(res.text)
            expected_json = casedata['期望返回Json内容']
            #print(expected_json)
            if expected_json!="":
                try:
                    json_obj = res.json()
                    logging.debug(json_obj) 
                    for element in expected_json.split(';'):
                        if element=="":#最常见的情况是case的最后一个json表达式末尾也跟了一个分号;
                            logging.warning("json expression is empty")
                            continue
                        #print("expected json: %s"%element)
                        key_values = element.strip('\n').split('=')
                        path = key_values[0]
                        logging.debug("path: %s"%path)
      
                        jsonpath_expr = parse(path)
                        matches = jsonpath_expr.find(json_obj)
                        #self.assertIsNotNone(match,"json path not found!")
                        self.assertNotEqual(matches,[],"json path not found!")
                        logging.debug(matches[0].value)
                        if len(key_values)>1:
                            expected_value = key_values[1]
                            if expected_value=='(null)':#期望为空值时可写成(null)或者None
                                expected_value = 'None'
                            logging.debug("expected value: %s"%expected_value)
                            self.assertEqual(expected_value,str(matches[0].value),"expected value: %s, actual: %s"%(expected_value,matches[0].value))
                        
                except Exception as e:
                    self.assertEqual(1,0,"no json object for the response!") # fails the test
              
           
        
    
    def tearDown(self):
        pass