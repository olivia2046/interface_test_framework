"""check if two JSON objects are isomorphic
@Modified by olivia.dou
Update Data: 2018-10-14
Desc:
修改：对于以逗号,连接的字符串，若为拼接数据，则不应严格匹配字符串，而应转为字符串的列表，对比排序后的列表
        针对列表中字典的顺序可能不同的情况，添加了列表比较的函数my_list_cmp，参考：
        https://stackoverflow.com/questions/25851183/how-to-compare-two-json-objects-with-the-same-elements-in-a-different-order-equa

"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.4 $"


import sys,logging

# For python3 portability
if sys.version_info[0] == 3:
    xrange = range

def my_list_cmp(list1, list2):
    '''比较列表内容，列表中元素位置可以不同（由于列表的元素可能是字典，而字典无法比较从而对列表无法排序，只能对两个列表的元素逐一调用jsonmatch对比）'''
    if (list1.__len__() != list2.__len__()):
        return False

    for l in list1:
        found = False
        for m in list2:
            res = jsonmatch(l, m)
            if (res):
                found = True
                break

        if (not found):
            #logging.debug("%s not found in list2"%repr(l))
            return False

    return True

def jsonmatch(x, y):
    """check if two JSON objects are isomorphic"""

    if isinstance(x, dict) and isinstance(y, dict):
        if len(x) != len(y):
            #logging.debug("dictionary length not match: %d, %d"%(len(x), len(y)))
            return False
        for k in x:
            if k not in y:
                #logging.debug("key %s not found in dict2"%k)
                return False
            if not jsonmatch(x[k], y[k]):
                #logging.debug("x[k]: %s doesn't match y[k]: %s"%(repr(x[k]),repr(y[k])))
                return False
        return True
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            #logging.debug("dictionary length not match: %d, %d" % (len(x), len(y)))
            return False
        return my_list_cmp(x, y)

    elif type(x) is type(y):
        #######added by olivia.dou#########
        if type(x) is str and type(y) is str and len(x.split(','))>1 and len(y.split(','))>1: # 由逗号分隔的字符串
            return jsonmatch(x.split(','),y.split(','))
        else:
        ####################################
            return x == y

    return False

