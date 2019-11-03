# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 17:36:50 2018

@author: olivia
This module is for variable and functions called in excel test cases
将Excel测试用例/header文件里的函数和全局变量表达式替换成相应的值

"""

import re,sys,logging
sys.path.append('..')
import base.globalvars as glo
import json


def eval_simple_expression(target_str):
    '''
    输入目标字符串，输出匹配到的表达式模式字符串列表和需要替换成的字符串列表
    参数： target_str:需要做表达式替换的字符串

    '''
    matched = re.match("(.*?)\(.*\)",target_str)
    if matched:
        outer = matched.group(1)
        splits = outer.split('.')
        function_name = splits[-1]
        module = outer.replace(function_name, '').rstrip('.')
        exec("from %s import %s" % (module, function_name))
        function = target_str.replace(module, '').lstrip('.')
        #去除function字符串里的转义符\
        if "\\" in function:
            function = function.replace("\\","")
        return eval(function)
    else:
        return glo.get_value(target_str)


def find_entities(content):
    evalBegin = "\${"
    evalEnd = "}"
    evalRegex = r"("+evalBegin+"|"+evalEnd+")"

    #起始结束标志的数量决定着，匹配的结尾在哪里
    #遇到开头标志，就加一，遇到结尾标志就减一
    #直到减到0的时候就是结束的时候
    matchNum = 0;
    start = 0
    firstMatch = 0;

    pattern = re.compile(evalRegex)
    matcher = pattern.search(content)

    #循环匹配开头标志和结尾标志
    while matcher:
        group = matcher.group()

        if group == evalBegin.lstrip(r'\\'): # 上面模式里转义多两个\
            #开头标志，数量加1
            matchNum = matchNum + 1
            if firstMatch == 0:
                start = matcher.span()[0]
                firstMatch = 1

        else:
            #结尾标志，数量减1
            matchNum = matchNum - 1

        #标签数量为0，循环结束，范围起始处的下标。
        if matchNum == 0:
            return start,matcher.span()[1]
        elif matchNum < 0: # 实体位于字典内部，替换后后侧有无法匹配的右花括号
            matchNum = 0
        #下一次循环
        matcher = pattern.search(content,matcher.span()[1])

    #如果标志不匹配，返回0。
    return None

'''
平衡组查找
'''
def balanceGroup(regex,text):
    #使用贪婪模式，尽可能多的找到内容，然后从找到的内容中筛选
    matcher = re.compile(regex).search(text)

    Content = ""
    if matcher:
        Content = matcher.group(1) # 获取${...}模式内部的字符串
        end = 0

        orgContent = Content
        while end < len(orgContent):
            orgContent = orgContent[end:]
            start_end = find_entities(orgContent)
            if start_end is not None:
                start,end = start_end

                value = balanceGroup(regex,orgContent[start:end])
                if not isinstance(value, str):
                    value = repr(value)
                #oldContent = Content
                #Content = oldContent.replace(oldContent[start:end], value)
                # end = end + len(Content) - len(oldContent) # 更新end位置
                Content = Content.replace(orgContent[start:end], value)

            else:
                end = len(Content)

    return eval_simple_expression(Content)


def eval_expression(expression):
    regex = r"\${(.*)}"
    result = balanceGroup(regex,expression)

    return result

#def eval_from_string(target_str,return_str = True,json_str = False):
def eval_from_string(target_str):
    """把${}格式的函数/全局变量表达式替换为函数执行的返回值"""
    # if json_str == True:
    #  matches = re.search(r'[\'"](\${.+?})[\'"]', target_str)
    #  while matches:
    #      target_str = target_str.replace(matches[0], matches[1])
    #      matches = re.search(r'[\'"](\${.+?})[\'"]', target_str)
    #if re.match(r'({.+?})',target_str):#json格式字符串

    try:
        # json格式字符串
        target_dict = json.loads(json.dumps(eval(target_str)))  # 此时target_str中键名为单引号，直接用json.loads(header_str)
        # 会报json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
        for k,v in target_dict.items():
            if isinstance(v,str) and re.match(r'.*\${.+?}.*',v): #值为表达式
                target_dict[k]=eval_from_string(v)

        return target_dict
    except Exception as e:
        # logging.error(e)
        # return None
        #if re.match(r'[\'"](\${.+?})[\'"]',target_str): #形如${..}的字符串，直接返回值，不需替换字符串再拼接
        #if re.match(r'^\${[^(},${)]+}$',target_str):  # 形如${..}的字符串，直接返回值，不需替换字符串再拼接
        if re.match(r'^\${((?!},\${).)*}$', target_str):  # 形如${..}的字符串，直接返回值，不需替换字符串再拼接
            # https: // blog.csdn.net / jk775800 / article / details / 90236812
            #不想匹配abc字符串就用这个表达式： (?!abc)
            #包含error不包含多个字符串，比如abc和def，这么写正则： error((?!(abc|def)).)*$
            return_str=False
        else:
            return_str=True

        text = target_str

        end = 0
        result=""
        return_result = True
        while end < len(text):
            text = text[end:]
            start_end = find_entities(text) # 找到${...}模式的字符串
            if start_end is not None:
                start,end = start_end
                entity = text[start:end]

                result = eval_expression(entity)
                if return_str == True:

                    if not isinstance(result, str):
                        result = repr(result)
                    target_str = target_str.replace(entity, result,1) #只替换一次，比如生成10次随机股票代码，不能一次替换全部
                elif isinstance(result,bool): #eval_expression的返回值是bool型
                    return_result = result&return_result

            else:
                end = len(text) # 跳出循环


        if return_str == True:
            if re.match(r".*\(.+\)$",target_str):#对于形如‘+1#_#BA005006’的字符串（inews的label），eval也能成功并且返回为1，
                                                #因此限定
                try:
                    result = eval(target_str) #拼接字符串可能包含外层内置函数调用
                    return result
                except Exception as e:
                    logging.error("%s\n%s"%(target_str,e))
                    return target_str
            else:
                return target_str
            #对于形如‘+1#_#BA005006’的字符串（inews的label），eval也能成功并且返回为1，因此需要再加上str()调用，增加了复杂度
            #因此对于函数调用，还是需要使用什么类型，函数就返回什么类型
        # if return_str == True:
        #     return target_str
        elif isinstance(result, bool):
            return return_result
        else:
            return result



# if __name__ == '__main__':
#     #result = eval_from_string("http://localhost/sdfdf${util.date_util.get_datetime_from_now(weeks=-1)}xdlkfjdlkfj${util.date_util:get_datetime_from_now(days=0)}")

#     print ("result:%s"%repr(result))

