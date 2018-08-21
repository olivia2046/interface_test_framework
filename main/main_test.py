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
        #print(data)
        url = casedata['URL']
        if casedata['请求类型'].lower()=='get':
            res = requests.get(url)
        else:
            data_label = casedata['请求数据']
            jutil = JsonUtil('../data/data.json')
            data = jutil.get_data(data_label)
            print(data)
            res = requests.post(url,data = data)
        print("response code:%s"%res.status_code)
        #print("response headers:%s"%res.headers)
        expected_status_code = casedata['期望响应代码']
        expected_res_txt = casedata['期望响应文本']
        #self.assertEqual(res.status_code,expected_status_code, 'Status Code not as expected!')
        self.assertIn(expected_res_txt,res.text, 'Response text not as expected!')
        #self.assertIn('200',res.text,'Test Failed!')
        
        #print(res.text)
        
    
    def tearDown(self):
        pass
    
    
if __name__=='__main__':

    
    unittest.main()