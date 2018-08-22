# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 20:55:06 2018

@author: olivia
"""

import unittest
import ddt
import pandas as pd
#import HTMLTestRunner
import sys
sys.path.append('..')
from base.executestep import ExecuteStep
import globalvars as glo

#datafrm = pd.read_excel('../case/testcase.xlsx')
datafrm = pd.read_excel(glo.testcase_file)
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

            res = ExecuteStep().execute(casedata)
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