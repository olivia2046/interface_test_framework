#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 20:55:06 2018

@author: olivia
description: 测试框架入口
"""
#import platform
#print(platform.python_version())
import unittest
import os,sys,time,logging,argparse
import pandas as pd
from urllib.parse import urlparse
sys.path.append('..')
import base.globalvars as glo
glo._init()  # 先必须在主模块初始化（只在Main模块需要一次即可）
# 获取项目名并设置全局变量,必须在import InterfaceTest之前导入，因InterfaceTest导入的get_config需要在import阶段就获取配置文件
glo.set_value("config_name", sys.argv[1])
from base.get_config import get_log_level,get_run_case_folder,get_run_case_type
from util import HTMLTestRunner
from util.send_email import SendEmail
from util.clean_expired_files import delfile


logging.basicConfig(stream=HTMLTestRunner.stdout_redirector, level=eval("logging." + get_log_level())
#logging.basicConfig(stream=sys.stdout, level=eval("logging." + get_log_level())
                    # , format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    # datefmt='%a, %d %b %Y %H:%M:%S'
                    )
logging.getLogger("urllib3").setLevel(logging.WARNING)

# 输出到结果报告文件的同时，在控制台打印日志
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
ch.setFormatter(formatter)
logging.getLogger('').addHandler(ch)

from base.get_config import get_neo4j_uri,get_and_set_global_vars,get_url_dict,get_tc_rootdir
from util import db_util
from base.get_config import get_test_type
#test_type = get_test_type().lower()

# 使用argparse模块处理命令行参数
parser = argparse.ArgumentParser()
parser.add_argument("config_name")
parser.add_argument("-a", "--algorithm", help="specify target algorithm name")
parser.add_argument("--host", help="specify target algorithm host")
parser.add_argument("-p", "--port", help="specify target algorithm port")
parser.add_argument("-r", "--report", help="specify report name")
parser.add_argument("-e", "--email", help="specify condition to send email:fail/all")
#parser.add_argument("-e", action='store_true', default=False, dest='send_email', help="switch whether to send email")
args = parser.parse_args()

if __name__=='__main__':

    # 从配置文件中获取全局变量值并设置
    get_and_set_global_vars()

    test_type = get_test_type()
    if test_type=='interface' or test_type=='gui':
        # 获取配置文件中的url列表并依次设置对应的全局变量
        url_dict = get_url_dict()
        if url_dict!={}:
            for item in url_dict.items():
                glo.set_value(item[0],item[1])
                glo.set_value("host"+item[0][-1],urlparse(item[1]).hostname)
    elif test_type=='algorithm':
        # 读入算法地址文件
        paths = pd.read_excel(sys.path[0] + os.sep+ '..' + os.sep + glo.get_value("algo_path_file"))

        # 命令行参数指定算法的host,port overwrite文件中的配置
        if args.host:
            if not args.algorithm:
                sys.exit("请指定需要测试的算法(文件夹名，非实际接口名)：-a/--algorithm algorithm_folder")
            else:
                #paths.loc[paths.Algo_Name==args.algorithm,'Host']=args.host
                paths.loc[paths.Test_Folder == args.algorithm, 'Host'] = args.host
        if args.port:
            if not args.algorithm:
                sys.exit("请指定需要测试的算法(文件夹名，非实际接口名)：-a/--algorithm algorithm_folder")
            else:
                paths.loc[paths.Test_Folder == args.algorithm, 'Port']=args.port

        paths_map ={}
        #glo.set_value("algo_paths",paths)
        #{"match_company":{"Host":"xxx.xxx.xxx.xxx","Port":"xxxxx"},...}
        for i in range(len(paths)):
            paths_map[paths.iloc[i]['Test_Folder']]={"Algo_Name":paths.iloc[i]['Algo_Name'],"Host":paths.iloc[i]['Host'],
                                                     "Port":paths.iloc[i]['Port'],"Data_File":paths.iloc[i]['Data_File'],
                                                     "Schema_File":paths.iloc[i]['Schema_File']}
        glo.set_value("algo_paths_map", paths_map)


    if get_neo4j_uri()!="":
        neo4j_driver = db_util.get_neo4j_driver()
        glo.set_value("neo4j_driver",neo4j_driver)


    general_case_class_mapping = {"db":"case.db.general_db_test.DBTest","interface":"case.interface.general_interface_test.InterfaceTest"}

    if test_type in ['db','interface']:
        classname = general_case_class_mapping[test_type].split('.')[-1]
        classpath = general_case_class_mapping[test_type].replace("." + classname, "")

    run_case_types = get_run_case_type()

    if run_case_types==["Excel"]: #仅运行Excel驱动的general case
        exec("from %s import %s"%(classpath,classname))
        run_testsuite = unittest.TestLoader().loadTestsFromTestCase(eval(classname))
    else:
        if run_case_types==["Code"]: #仅运行独立的Python代码test case
            run_testsuite = unittest.TestSuite()
        else: # 两种都运行
            exec("from %s import %s" % (classpath, classname))
            run_testsuite = unittest.TestLoader().loadTestsFromTestCase(eval(classname))

        run_case_folders = get_run_case_folder()

        if len(run_case_folders) == 0:  # 未指定运行case的level,则运行根目录下case（包括所有子目录）
            run_case_folders = ['.']

        # 算法测试可在命令行制定需要测试的算法
        # if test_type=='algorithm' and len(sys.argv)>2:
        #     run_case_levels = [sys.argv[2]]
        if test_type=='algorithm' and args.algorithm:
            run_case_folders = [args.algorithm]

        #run_case_folders.append('.')
        for folder in run_case_folders:
            path = get_tc_rootdir() + '/' + folder
            if not os.path.exists(path) or not os.listdir(path):
                logging.warning("Folder '%s' doesn't exist or empty!" % folder)
                continue
            discover = unittest.defaultTestLoader.discover(os.path.abspath(path),
                                                           # discover = unittest.defaultTestLoader.discover(os.path.abspath(get_tc_rootdir()),
                                                           pattern='*.py',
                                                           top_level_dir=get_tc_rootdir())

            # discover 方法筛选出来的用例，循环添加到测试套件中
            for test_suite in discover:
                for test_case in test_suite:
                    run_testsuite.addTests(test_case)
                    # print(testsuite)

    now = time.strftime('%Y-%m-%d %H_%M_%S',time.localtime())#时分秒中间不能用:连接，无效的文件名

    if not os.path.exists('../testreport'):
        os.makedirs('../testreport')
    if args.report:
        report_file = r'../testreport/%s.html'%args.report
    else:
        report_file = r'../testreport/report-%s-%s.html'%(args.config_name,now)
    #report_file = r'../testreport/report.html' # 测试Jenkins publish report功能

    #fp=open(report_file,'wb')
    with open(report_file,'wb') as fp:

        runner=HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'%s %s测试报告'%(test_type,args.config_name),
        description=u'用例执行情况：',
        verbosity=2
        )

        runner.run(run_testsuite)

        logging.shutdown()

    if args.email:
        SendEmail().send_main(report_file,"%s test %s测试报告"%(test_type,args.config_name),args.email)

    # 清理过期报告
    delfile('../testreport',30)
