# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 11:12:29 2018
@author: olivia
"""

import requests,json
#import globalvars as glo # why no module named 'globalvars'
import sys,logging
sys.path.append('..')
import base.globalvars as glo



#glo._init()#先必须在主模块初始化（只在Main模块需要一次即可）    

class RunMethod:
    #@Todo: 使用eval()调用post/get，只需保留run_main?
    def post_main(self, url, data=None, json=None, headers=None, verify=False, cert = None, new_session=False):
    #def post_main(self, url, json, headers=None, verify=False, new_session=False):
        res = None
        if new_session:
            s = requests.Session()
            #res = s.post(url=url,data=data,headers=headers,verify=verify)
        else :
            s = glo.get_value('Session') #获取全局变量Session
            #res = s.post(url=url,data=data,verify=verify)
        if headers is None:
            # knews必须使用data参数, 否则post请求不成功, inews post json格式的数据必须使用json参数
            res = s.post(url=url, data=data, json=json, verify=verify, cert = cert)
        else:

            res = s.post(url=url, data=data, json=json, headers=headers, verify=verify, cert = cert)

        if new_session:
            glo.set_value('Session',s)
        #return res.json()
        return res

    def get_main(self, url, data=None, json=None, headers=None, verify=None, cert = None, new_session=False):
        res = None
        if new_session:
            s = requests.Session()
            #s.proxies = {'http': ''}
            #res = s.get(url=url,data=data,headers=headers,verify=verify)

        else :
            s = glo.get_value('Session') #获取全局变量Session
        if headers is None:
            res = s.get(url=url, params=data, json=json, verify=verify, cert=cert)

        else:
            res = s.get(url=url, params=data,  json=json, headers=headers, verify=verify,cert = cert)

        glo.set_value('Session',s)

        return res

    def delete_main(self, url, data=None, json=None, headers=None, verify=False, cert = None, new_session=False):
        res = None
        if new_session:
            s = requests.Session()

        else :
            s = glo.get_value('Session') #获取全局变量Session
        if headers is None:
            res = s.delete(url=url, params=data, json=json, verify=verify, cert = cert)

        else:
            res = s.delete(url=url, params=data,  json=json, headers=headers, verify=verify, cert = cert)

        glo.set_value('Session',s)

        return res

    def put_main(self, url, data=None, json=None, headers=None, verify=False, cert = None, new_session=False):
        res = None
        if new_session:
            s = requests.Session()

        else :
            s = glo.get_value('Session') #获取全局变量Session
        if headers is None:
            res = s.put(url=url, params=data, json=json, verify=verify, cert = cert)

        else:
            res = s.put(url=url, params=data,  json=json, headers=headers, verify=verify, cert = cert)

        glo.set_value('Session',s)

        return res

    def run_main(self, method, url, data=None, json=None, headers=None, verify=False, cert = None, new_session=False):
        res = None

        if method.upper() == 'POST':
            res = self.post_main(url, data, json, headers, verify, cert, new_session)

        elif method.upper() == 'GET':
            res = self.get_main(url, data, json, headers, verify, cert, new_session)
        elif method.upper()=="DELETE":
            res = self.delete_main(url, data, json, headers, verify, cert, new_session)
        elif method.upper()=="PUT":
            res = self.put_main(url, data, json, headers, verify, cert, new_session)
        else:
            logging.exception("request method empty or is not supported")

        # return json.dumps(res,ensure_ascii=False)
        # return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)

        # Todo: 使用eval()调用get user/info时url为/user/info，而使用单独定义的get_main()时url为url/info?ids=<id>,why?
        # if new_session:
        #     s = requests.Session()
        #
        # else :
        #     s = glo.get_value('Session') #获取全局变量Session
        #
        # if headers is None:
        #     # knews必须使用data参数, 否则post请求不成功, inews post json格式的数据必须使用json参数
        #     res = eval("s."+method.lower()+"(url=url, data=data, json=json, verify=verify, cert = cert)")
        # else:
        #     res = eval("s."+method.lower()+"(url=url, data=data, json=json, headers=headers, verify=verify, cert = cert)")
        #
        # if new_session:
        #     glo.set_value('Session',s)

        return res

