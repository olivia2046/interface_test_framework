# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 06:20:19 2018
参考了慕课网Python接口测试自动化课程的部分实现
@author: olivia
"""

import json

class JsonUtil:
    def __init__(self, file_path=None):
        if file_path  == None:
            self.file_path = '../data/data.json'
        else:
            self.file_path = file_path
        self.data = self.read_data()
        
    #读取json文件
    def read_data(self):
        with open(self.file_path,encoding='utf8') as fp:
            data = json.load(fp)
            return data  
        
    #根据关键字获取数据
    def get_data(self,id):
        #print type(self.data)
        return self.data[id]

#    #写json
#    def write_data(self,data):
#        #with open('../dataconfig/cookie.json','w') as fp:
#        with open(cookie_file,'w') as fp:
#            fp.write(json.dumps(data))
