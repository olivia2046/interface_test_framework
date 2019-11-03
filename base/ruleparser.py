# -*- coding: utf-8 -*-
'''
ref: https://blog.csdn.net/luyaran/article/details/53928967
Created on: 2019/2/13 16:04
desc:

'''

#Todo: 针对jsonpath的结果均为列表的情况，定义only_contains运算
#      =:第一个参数为仅一个元素的数组，第二个参数为单一值

import json,logging,re
from jsonpath import jsonpath
import pandas as pd
from base.expression_evaluation import eval_from_string
from util.misc import is_list
from util.jsonmatch import my_list_cmp

class RuleParser(object):
    def __init__(self, rule, response):
        #if isinstance(rule, basestring): # Python 2
        if isinstance(rule, str):
            rule = rule.strip()
            self.rule = json.loads(rule)
            logging.debug("rule: %s"%repr(rule))
        else:
            self.rule = rule
        self.validate(self.rule)
        if 'Content-Type' in response.headers.keys() and 'application/json' in response.headers['Content-Type']:
            self.json_obj = response.json()
        self.res_text = response.text

    class Functions(object):

        ALIAS = {
            '=': 'eq',
            '!=': 'neq',
            '>': 'gt',
            '>=': 'gte',
            '<': 'lt',
            '<=': 'lte',
            'and': 'and_',
            'in': 'in_',
            'not in': 'not_in_',
            'contains': 'contains_',
            'not contains': 'not_contains_',
            'or': 'or_',
            'not': 'not_',
            'str': 'str_',
            'int': 'int_',
            'length':'length_',
            '+': 'plus',
            '-': 'minus',
            '*': 'multiply',
            '/': 'divide',
            'null': 'null_',
            'not null': 'not_null_',
            'set':'set_',
            'split':'split_'
        }

        def eq(self, *args):
            # 转换bool值
            result = None
            if isinstance(args[1],str) and args[1].upper()=='TRUE':
                result = (args[0] is True)
                if result is False:
                    logging.error("%s is not True"%args[0])
                return result
            elif isinstance(args[1],str) and args[1].upper()=='FALSE':
                result = (args[0] is False)
                if result is False:
                    logging.error("%s is not False"%args[0])
                return result
            elif isinstance(args[0],list) and isinstance(args[1],list):
                return my_list_cmp(args[0],args[1])
            result = (args[0] == args[1])
            if result is False:
                logging.error("%s not equal to %s"%(args[0],args[1]))
            return result

        def neq(self, *args):
            result = (args[0] != args[1])
            if result is False:
                logging.error("%s equal to %s"%(args[0],args[1]))
            return result

        def in_(self, *args):
            #logging.debug(args[1:])
            # 约定in操作只有两个参数
            if isinstance(args[0],list) and isinstance(args[1],list):
                result = set(args[0]).issubset(set(args[1]))
            else:
                result = (args[0] in args[1])
            if result is False:
                logging.error("%s not in %s"%(args[0],args[1]))
            return result

        def not_in_(self, *args):
            if isinstance(args[0],list) and isinstance(args[1],list):
                result = not(set(args[0]).issubset(set(args[1])))
            else:
                result = args[0] not in args[1:]
            if result is False:
                logging.error("%s in %s" % (args[0], args[1]))
            return result

        def gt(self, *args):
            result = (args[0] > args[1])
            if result is False:
                logging.error("%s not greater than %s" % (args[0], args[1]))
            return result

        def gte(self, *args):
            result = (args[0] >= args[1])
            if result is False:
                logging.error("%s not greater than and not equal to %s" % (args[0], args[1]))
            return result

        def lt(self, *args):
            result = args[0] < args[1]
            if result is False:
                logging.error("%s not less than %s" % (args[0], args[1]))
            return result

        def lte(self, *args):
            result = (args[0] <= args[1])
            if result is False:
                logging.error("%s not less than and not equal to %s" % (args[0], args[1]))
            return result

        def not_(self, *args):
            result = (not args[0])
            if result is False:
                logging.error("%s is %s" % (args[0], args[1]))
            return result

        def or_(self, *args):
            # Todo: 参数为列表的情况
            if all(map(is_list,args)): # 参数全部为列表
                # 不同列表中同一index的元素做或运算，形成结果列表。结果列表全为True的情况下才返回true
                l_series = list(map(pd.Series,args))
                result = pd.Series([False]*len(l_series[0]))
                for i in range(len(l_series)):
                    result = result|l_series[i]

                return all(result) #此处为all，不为any
            else:
                #针对any((False,[False]))为True解决
                args_list = []
                for arg in args:
                    if isinstance(arg,list):
                        arg = any(arg)
                    args_list.append(arg)
                return any(args)

        def and_(self, *args):
            #Todo: 参数为列表的情况
            if all(map(is_list,args)): # 参数全部为列表
                # 不同列表中同一index的元素做与运算，形成结果列表。结果列表全为True的情况下才返回true
                l_series = map(pd.Series, args)
                result = pd.Series([True] * len(l_series[0]))
                for i in range(1, len(l_series)):
                    result = result & l_series[i]

                return all(result)
            else:
                # 针对all((True,[False]))为True解决
                args_list = []
                for arg in args:
                    if isinstance(arg,list):
                        arg = all(arg)
                    args_list.append(arg)
                return all(args)

        def int_(self, *args):
            return int(args[0])

        def str_(self, *args):
            return str(args[0])

        def length_(self, *args):
            return len(args[0])

        def upper(self, *args):
            return args[0].upper()

        def lower(self, *args):
            return args[0].lower()

        def plus(self, *args):
            return sum(args)

        def minus(self, *args):
            return args[0] - args[1]

        def multiply(self, *args):
            return args[0] * args[1]

        def divide(self, *args):
            return float(args[0]) / float(args[1])

        def abs(self, *args):
            return abs(args[0])

        def null_(self, *args):
            return args[0] is None or args[0]=="" or args[0]==[] or args[0]=={}

        def not_null_(self, *args):
            return args[0] is not None and args[0]!="" and args[0]!=[] and args[0]!={}

        def contains_(self, *args):
            # 弃用多个参数的用法
            #if len(args)>2:
            #    return args[-1] in args[0:-1]
            #else:
            #    return args[1] in args[0]
            # 字符串表达式结果‘None’转回None
            if args[1]=='None':
                args_1 = None # tuple不能修改元素
            else:
                args_1 = args[1]

            if isinstance(args[0],list) and isinstance(args_1,list): # 列表a是否包含列表b ["contains",lista,listb]
                result = set(args_1).issubset(set(args[0]))
            else:
                result = (args_1 in args[0])
            if result is False:
                logging.error("%s not contains %s" % (args[0], args[1]))
            return result


        def not_contains_(self, *args):
            # 弃用多个参数的用法
            #     if len(args)>2:
            #         return not(args[-1] in args[0:-1])
            #     else:
            #         return not(args[1] in args[0])
            # 字符串表达式结果‘None’转回None
            if args[1]=='None':
                args_1 = None # tuple不能修改元素
            else:
                args_1 = args[1]
            if isinstance(args[0],list) and isinstance(args_1,list): # 列表a是否包含列表b ["contains",lista,listb]
                result = not (set(args_1).issubset(set(args[0])))
            else:
                result = (not (args_1 in args[0]))
            if result is False:
                logging.error("%s contains %s" % (args[0], args[1]))
            return result

        def set_(self,*args):
            return set(args[0])

        def split_(self,*args):
            return args[0].split(args[1])

    @staticmethod
    def validate(rule):
        if not isinstance(rule, list):
            #raise RuleEvaluationError('Rule must be a list, got {}'.format(type(rule)))
            raise Exception('Rule must be a list, got {}'.format(type(rule)))
        if len(rule) < 2:
            #raise RuleEvaluationError('Must have at least one argument.')
            raise Exception('Must have at least one argument.')

    def _evaluate(self, rule, fns, f_list_result):
        """
        递归执行list内容
        """

        def _recurse_eval(arg,f_list):

            if isinstance(arg, list):
                return self._evaluate(arg, fns,f_list)
            else:
                # if arg == 'and' or arg == 'or':
                #     # Todo: 仅and, or可能涉及结果列表的拼接evaluate
                #     f_list = 1
                # if isinstance(arg,str) and re.match("\[.*\]",arg):
                #     try:
                #         arg = json.loads(arg)
                #     except Exception as e:
                #         logging.error(e)
                return arg

        #r = map(_recurse_eval, rule) # Python 2
        #r = list(map(r[0], rule))
        r = []
        if rule==[]: # 如["=","$.message",[]]的最后一个元素
            return rule
        for item in rule:
            if len(r)>0 and (r[0]=='and' or r[0]=='or'):
                f_list_result=1
            else:
                f_list_result=0
            r.append(_recurse_eval(item,f_list_result))
        r[0] = self.Functions.ALIAS.get(r[0]) or r[0]

        f_func_call = 0 # 参数中是否有函数调用
        for i in range(1, len(r)): # 函数调用
            if type(r[i]) is str and re.match(".*\${.+}.*",r[i]):
                f_func_call = 1
                #r[i] = eval_from_string(r[i],return_str=True,json_str=False)
                r[i] = eval_from_string(r[i])
                logging.debug("evaluation result of r[%s]: %s"%(i,repr(r[i])))
                # 把形如'[\'/case/sam\']'的字符串转换成列表
                if isinstance(r[i],str) and re.match("\[.*\]",r[i]):
                    try:
                        r[i] = r[i].replace("\'",'"')
                        r[i] = json.loads(r[i])
                    except Exception as e:
                        logging.error(e)

        if r[0]!="and_" and r[0]!="or_" and type(r[1]) is str and (r[1].startswith('$.') or r[1].startswith('$[')): # and, or连接的表达式的第一个参数不会是jsonpath？？
            #jsonpath_expr = parse(r[1])
            try:
                #match_paths = jsonpath_expr.find(self.json_obj)
                match_paths = jsonpath(self.json_obj,r[1])
                #if match_paths == []:
                if match_paths is False and r[2]!='False':#若rule本身是验证jsonpath表达式是否为False（无满足条件的节点时结果为False而不是[]），则不应抛出异常
                    raise Exception('未找到对应的jsonpath:%s'%r[1])

                func = getattr(fns, r[0])

                result_list = []  # 保存结果的列表，供外层的and, or使用
                result = None
                if r[-1]=="list relation": #
                    r[1] = match_paths
                    result = func(*r[1:-1])
                    result_list.append(result)

                else: # 逐一比较

                    for match in match_paths:
                        #r[1] = match.value
                        r[1] = match
                        #
                        if f_func_call==1: # 参数中有函数调用，所有参数值转换为字符串型
                            for i in range(1,len(r)):
                                r[i] = str(r[i])

                        #logging.debug((*r[1:],))
                        #logging.debug("function: %s, params: %s" % (repr(func), (*r[1:],)))

                        result = func(*r[1:])
                        if result is False:
                            logging.debug("function: %s, params: %s"%(repr(func), (*r[1:],)))
                            #logging.debug("matched value:%s"%match)
                            #logging.debug("r[1]:%s"%r[1])
                            if f_list_result==0: #不需要返回结果列表
                                return False

                        result_list.append(result)
                if f_list_result == 1:
                    return result_list
                else:
                    return result #???
                #     if result is False:
                #         logging.debug("function: %s, params: %s"%(repr(func),(*r[1:],)))
                #         return result
                # return True
            except Exception as e:
                return False

        elif type(r[1]) is str and r[1].lower()=='$response_plain_text': # 同一接口可能存在返回json和返回文本两种情况，rule parser中需要兼容这种情况
            func = getattr(fns, r[0])
            r[1] = self.res_text
            result = func(*r[1:])
            return result
        else: #
            if r[0] in dir(fns): #r[0]是Functions类的一个方法
                func = getattr(fns, r[0])
                #logging.debug((*r[1:], ))
                logging.debug("function: %s, params: %s" % (repr(func), (*r[1:],)))
                result = func(*r[1:])
                # if result is False:
                #     logging.error("evaluation result not True: %s" % repr(self.rule))
                return result
            else: #r是普通列表
                return r

    def evaluate(self):
        fns = self.Functions()
        ret = self._evaluate(self.rule, fns, 0)
        if not isinstance(ret, bool):
            logging.warning('In common usage, a rule must return a bool value,'
                        'but get %s, please check the rule to ensure it is true'%ret)

        return ret

# if __name__=='__main__':
#     rparser = RuleParser("[\"=\",1,1]")
#     print(rparser.evaluate())
