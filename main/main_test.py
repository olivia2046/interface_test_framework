# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 20:55:06 2018

@author: olivia
"""
import unittest,HTMLTestRunner
import sys,time
sys.path.append('..')
from case.general_interface_test import InterfaceTest
    
    
if __name__=='__main__':
    
    #unittest.main()
    #testsuite = unittest.TestSuite()
    #testsuite.addTests(InterfaceTest("test_interface"))
    testsuite = unittest.TestLoader().loadTestsFromTestCase(InterfaceTest)
    
    now = time.strftime('%Y-%m-%d %H_%M_%S',time.localtime())#时分秒中间不能用:连接，无效的文件名
    report_file = r'../report/report-%s.html'%now
    fp=open(report_file,'wb')
    
    runner=HTMLTestRunner.HTMLTestRunner(
    stream=fp,
    title=u'接口测试报告',
    description=u'用例执行情况：')
    
    runner.run(testsuite)

    #关闭文件流，不关的话生成的报告是空的
    fp.close()
    