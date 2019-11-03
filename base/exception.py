# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2019/10/8 11:19
desc:
'''

class ExpireError(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self) #初始化父类
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo
 