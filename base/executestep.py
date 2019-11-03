# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 13:59:53 2018

@author: olivia
"""
import sys,re,logging,json
from jsonpath_rw import parse
from jsonpath import jsonpath
sys.path.append('..')
from base.runmethod import RunMethod
from util.json_util import JsonUtil
from base.getdata import GetData
from base.get_config import get_header_file,get_data_file, get_verify_cert
#@Todo:get_header_file,get_data_file,get_root_url,get_verify不需要执行每个case时调用一次，用全局变量即可
from base.expression_evaluation import eval_from_string


class DependentData:
    def __init__(self,case_id):
        self.case_id = case_id
        self.depend_case_data = None
        self.data = None

    #执行依赖测试，获取结果
    def run_dependent(self):

        #通过case_id去获取该case_id的整行数据
        self.depend_case_data = GetData().get_case_data(self.case_id)
        res = ExecuteStep().execute(self.depend_case_data)
        return res
        

    #根据依赖的key去获取执行依赖测试case的响应,然后返回
    def get_data_for_case(self,case_data):
        depend_data = case_data['Post Data依赖的返回数据']
        response_data = self.run_dependent()
        
        #获取依赖数据的key
        if depend_data.startswith('json:'):
            return jsonpath(response_data,depend_data.replace('json:'),'')

        elif depend_data.startswith('html:'):
            pattern = re.compile(depend_data.split(':')[1])#取中间的字符串
            matches = re.findall(pattern,response_data.text)
            indice = int(depend_data.split(':')[2])
            dependent_value = matches[indice] #到底应该取第一个还是第二个？
            return dependent_value

class ExecuteStep():
    
    def execute(self,casedata):
        #logging.debug(casedata.keys())
        if '指定header' in casedata.keys() and casedata['指定header'].upper()=='Y':
            if 'header内容' in casedata.keys():
                header_value = casedata['header内容']
            else:
                header_value = {}
            # 如果header内容为{...}格式则直接解析为json内容，否则根据header_file中对应标签提取json内容
            #Todo: header内容直接写在Excel中也应支持表达式替换
            if re.findall("^{.+}$", header_value.replace("\n", "")) != []:  # 含\n时匹配为空，why?
                header = json.loads(header_value)
            else:
                jutil = JsonUtil(get_header_file())
                header = jutil.get_data(header_value)
                #header_str = eval_from_string(repr(header),return_str=True,json_str=True)
                #header = json.loads(json.dumps(eval(header_str))) #直接用json.loads(header_str)会报json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
                header = eval_from_string(repr(header))
        else:
            header = None

        data = []
        if '请求数据' in casedata.keys() and casedata['请求数据']!='':
            request_data = casedata['请求数据'].strip()
            # 如果请求数据为{...}格式则直接解析为json内容，否则根据data_file中对应标签提取json内容
            #if re.findall("^{.+}$",request_data.replace("\n",""))!=[]: #含\n时匹配为空，why?
            try:
                data = json.loads(request_data)
                data_str = request_data
            except:
                if ';' in request_data: # 分号分隔的等式，针对json格式数据中调用函数返回值非字符串型，原有方法难以处理的问题
                    items = request_data.split(';')
                    data = {}
                    for item in items:
                        key,value = tuple(ele.strip('\n') for ele in item.split('=',1))
                        data[key] = eval(eval_from_string(value))
                    data_str = repr(data)

                elif not '=' in request_data: #request_data为data文件中标签名
                    jutil = JsonUtil(get_data_file())
                    data = jutil.get_data(request_data) #json格式数据
                    data_str = repr(data)


                else: #形如url=/xxx&type=POST&params={"id":"123","type":"1","paths":{}}&contentType=1的接口
                    data_str = request_data.strip()

            # result = eval_from_string(data_str,return_str=True,json_str=True)
            # if not isinstance(result,str):
            #     result = repr(result)
            # #logging.debug("data_str: %s"%data_str)
            # #将函数执行后的结果再重新构造成json对象
            # data = json.loads(json.dumps(eval(result))) #json.dumps(eval(data_str))的作用是兼容单引号内容
            # 解析表达式
            data = eval_from_string(data_str)
            if isinstance(data,str):
                try:
                    # 如果data是json格式字符串则转换为json对象
                    data = json.loads(data)  # json.dumps(eval(xxx))的作用是兼容单引号内容
                except:
                    pass


        #获取case依赖数据
        if 'case依赖' in casedata.keys() and casedata['case依赖'] !='':#casedata已先期将nan替换为''
            depend_data = DependentData(casedata['case依赖'])
            #依赖的返回数据可能不止一处，返回的json数据，返回的html页面的一部分(authenticity_token， 如果要动态操作repository，则url也依赖返回的html页面元素)
            value = depend_data.get_data_for_case(casedata)
            if '数据依赖字段' in casedata.keys():
                field = casedata['数据依赖字段']
                data[field] = value
            else:
                return "未指定数据依赖字段"


        if 'Root_URL' in casedata:
            root_url = casedata['Root_URL']
        else:
            root_url = ""
        #root_url = eval_from_string(root_url, return_str=True, json_str=False)
        root_url = eval_from_string(root_url)
        if 'relative_URL' in casedata.keys():
            #relative_url = eval_from_string(casedata['relative_URL'], return_str=True, json_str=False)
            relative_url = eval_from_string(casedata['relative_URL'])
        else:
            relative_url = ""

        # if 'encode_URL' in casedata.keys() and casedata['encode_URL'].upper()=='Y':
        #     relative_url = quote(relative_url, 'utf-8')


        url = root_url + relative_url


        if '新会话' in casedata.keys() and casedata['新会话'].upper()=='Y':
            #print("新会话~~~~~~~~~~~~~~~~~~~~~~~~")
            new_session=True
        else :
            #print("保持会话~~~~~~~~~~~~~~~~~~~~~~")
            new_session=False

        if '+' in data:
            data = data.replace("+","%2B")
        logging.debug("data:" + repr(data))
        self.data = data
        #glo.set_value("post_data",data)

        #verify = get_verify_str()
        # if verify.upper()=='FALSE':
        #     # logging.debug("no need to vefify certification.")
        #     #verify = eval("False")
        #     verify = False
        #     cert = None
        # else:
        #     verify=True
        #     cert = sys.path[0] + '/../' + get_certfile_path()
        #cert = get_cert()
        verify,cert = get_verify_cert()


        if not '请求类型' in casedata.keys():
            return "未指定请求类型"
        if '数据传参' in casedata.keys() and casedata['数据传参'].lower()=='json':
            res = RunMethod().run_main(method=casedata['请求类型'], url=url, json=data, headers=header, verify=verify, cert = cert,
                                       new_session=new_session)
        else:
            res = RunMethod().run_main(method=casedata['请求类型'], url=url, data=data, headers = header, verify = verify, cert = cert, new_session=new_session)

        return res