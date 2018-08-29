# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:53:07 2018

@author: olivia
"""
import pandas as pd
import sys
sys.path.append('..')
from config.get_config import get_testcase_file

class GetData:
    def get_case_data(self,caseid,file_path=None):
        '''根据test case id，以字典形式返回test case'''
        #print("caseid%s"%caseid)
        #print(file_path)
        if file_path is None:
            file_path = get_testcase_file()
        datafrm = pd.read_excel(file_path).fillna('') #把空值替换成空字符串
        #case_data = datafrm[datafrm['CaseId']==caseid]#取出一行仍为DataFrame类型，需要取Series
        #print("get case data")
        #print(case_data)
        case_data = datafrm[datafrm['CaseId']==caseid].iloc[0]#取出一行仍为DataFrame类型，需要取Series
        return case_data.to_dict()
        
    

