# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 08:00:48 2018
@author: olivia
Description: 通用接口测试类
"""


import pandas as pd
import numpy as np
import sys,logging, re
import json
from jsonpath import jsonpath #eval中用到，勿删
import unittest
sys.path.append('..')
from util import ddt
from util.jsonmatch import jsonmatch
from base.executestep import ExecuteStep
from base.get_config import get_testcase_file,get_run_case_level
from base.expression_evaluation import eval_from_string
import base.globalvars as glo
from base.ruleparser import RuleParser
from base.decorators import retry


#从Excel test case文件中读取数据，用以驱动测试
datafrm = pd.read_excel(get_testcase_file(),dtype='str')
datafrm = datafrm.fillna('') #将空值统一替换为空字符串
testdata = []
datafrm.apply(lambda x:testdata.append(x.to_dict()),axis=1) #将每一行转换为字典，所有行组成一个字典的列表


@ddt.ddt
class InterfaceTest(unittest.TestCase):
    @ddt.data(*testdata)
    def setUp(self,casedata):
        #无法实现数据驱动？
        # if casedata['SetUp'] != "":
        #     eval_from_string(casedata['SetUp'])
        pass


    @ddt.data(*testdata)
    #@retry(3, 10)
    def test_interface(self, casedata):
        '''测试接口'''
        if (casedata['Case_Level'] in get_run_case_level() or get_run_case_level()==[]) and casedata['是否运行'].upper()=='Y': #如果不在指定运行的case level中或未标注运行，则该testcase跳过
            #执行SetUp内容
            if 'SetUp' in casedata.keys() and casedata['SetUp']!="":
                #eval_from_string(casedata['SetUp'], return_str=False, json_str = True)
                eval_from_string(casedata['SetUp'])

            #执行测试内容
            exec_step = ExecuteStep()
            res = exec_step.execute(casedata)
            
            # 调试输出resonse文本
            '''
            if not os.path.exists('../testreport'):
                os.makedirs('../testreport')
            now=time.strftime("%Y-%m-%d %H_%M_%S",time.localtime())
            with open(r"../testreport/ResponsePage-%s-%s.html"%(casedata['Case_Name'],now),'w',encoding='utf-8-sig') as f: # 中文即使用utf-8也还是乱码
                f.write(res.text)
            '''

            expected_status_code = casedata['期望响应代码']
            # # inews测试prod连接不稳定
            # #pdb.set_trace()
            # if res.status_code==403 and 'message' in res.json().keys() and res.json()['message']=='forbidden2' and expected_status_code!=403:
            #     #pdb.set_trace()
            #     self.fail("Token Expired")
            #     raise ExpireError("Token Expired")
            logging.debug(res.status_code)
            #try:
            self.assertEqual(str(res.status_code),expected_status_code, 'Status Code not as expected! Expected:%s, Actual: %s, %s'%(expected_status_code,res.status_code,res.text))
            #except:
            #    raise

            # res.raise_for_status()

            expected_res_txt = casedata['期望响应文本']
            if expected_res_txt!="":
                if casedata['对比方法']=="" or casedata['对比方法'] is np.nan:
                    #logging.error("需要输入对比方法！")
                    self.fail("需要输入对比方法！")
                else:
                    logging.debug("casedata['对比方法']：%s"%casedata['对比方法'])
                    eval("self."+ casedata['对比方法'])(str(expected_res_txt),res.text, 'Response text not as expected!')

            expected_json = casedata['期望返回Json内容']

            if expected_json!="":
                # 验证返回的Json内容
                try:
                    if 'Content-Type' in res.headers.keys() and 'application/json' in res.headers['Content-Type']:
                        actual_json_obj = res.json()
                    else:
                        actual_json_obj = {}
                    if re.compile("^\${.+}$").match(expected_json) is not None: # 仅包含${...}函数表达式
                        #eval_result = eval_from_string(expected_json,return_str=True,json_str=True)
                        #expected_json = eval_from_string(expected_json, return_str=True, json_str=True)
                        expected_json = eval_from_string(expected_json)
                        # 进行字符串替换时返回结果已转换成字符串,需要解码json对象，作为jsonmatch的参数
                        eval_result = json.loads(json.dumps(eval(expected_json))) #由于eval_result包含单引号，需要先用json.dumps(eval(xxx))进行转换
                        logging.debug("expected Json string: %s"%repr(eval_result))
                        logging.debug("Json string in response:%s"%repr(actual_json_obj))
                        self.assertTrue(jsonmatch(eval_result, actual_json_obj))

                    elif re.compile("^{.+}$").match(expected_json) is not None: #仅包含{}json表达式
                        logging.debug("expected Json string: %s" % repr(expected_json))
                        logging.debug("Json string in response:%s" % repr(actual_json_obj))
                        self.assertTrue(jsonmatch(json.loads(expected_json),actual_json_obj))

                    else: #按json_path处理
                        for element in expected_json.split(';'):
                            if element.strip()=="":#最常见的情况是case的最后一个json表达式末尾也跟了一个分号;
                                #logging.warning("json expression is empty")
                                continue #跳过

                            #rparser = RuleParser(element.strip(),actual_json_obj)
                            rparser = RuleParser(element.strip(), res)
                            if 'Content-Type' in res.headers.keys()  and 'application/json' in res.headers['Content-Type']:
                                actual_result = res.json()
                            else:
                                actual_result = res.text

                            #assert rparser.evaluate() is True, "验证失败：%s\nactual response:\n%s"%(element,actual_json_obj)
                            assert rparser.evaluate() is True, "验证失败：%s\nactual result:\n%s" % (
                            element, actual_result)

                except Exception as e:
                    #self.assertEqual(1,0,"Exception occured: %s"%e) # fails the test
                    self.fail("Exception occured: %s" % e)  # fails the test


            if '结果验证方法名' in casedata.keys() and casedata['结果验证方法名']!="":
                # 本地变量无法传递到expression_evaluation模块，需要使用全局变量
                glo.set_value('post_data', exec_step.data)
                #glo.set_value('response', res)
                glo.set_value('res_json', res.json())
                logging.debug("res.json(): %s"%repr(res.json()))

                #eval_from_string(casedata['结果验证方法名'].rstrip('}') + '(${post_data},${response})}')
                validation_result = eval_from_string(casedata['结果验证方法名'].rstrip('}') +
                                                     #'(base.globalvars.getvalue("post_data"),base.globalvars.getvalue("response"))}',return_str=False,json_str=False)
                                                    '(${post_data},${res_json})}', return_str = False, json_str = False)
                self.assertTrue(validation_result,'验证不通过')



            if '设置全局变量' in casedata.keys() and casedata['设置全局变量']!="":
                if casedata['设置全局变量'].startswith("text:"): #text:变量名
                    var_name=casedata['设置全局变量'].replace("text:","")
                    glo.set_value(var_name,res.text)
                elif casedata['设置全局变量'].startswith("json:"): #json:表达式:索引下标:变量名，如json:$.newsId:[0]:newsId
                    values = casedata['设置全局变量'].split(':')
                    var_name=values[-1]
                    jp_exp = values[1] #jsonpath
                    # if values[2]!="":
                    #     index = values[2]
                    glo.set_value(var_name,eval("jsonpath(res.json(),jp_exp)"+values[2]))
                else:
                    self.fail("设置全局变量格式不正确")



            if 'Post_Case_Action' in casedata.keys() and casedata['Post_Case_Action']!="":
                # 执行post case action
                #eval_from_string(casedata['Post_Case_Action'],return_str=False,json_str=True)
                eval_from_string(casedata['Post_Case_Action'])
        else:
            raise unittest.SkipTest("case set not to run") # case真正跳过，不会被统计为pass

    def tearDown(self):
        pass