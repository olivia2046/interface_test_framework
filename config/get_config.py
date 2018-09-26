# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 13:46:36 2018

@author: olivia
"""

from configparser import ConfigParser
import os
cf=ConfigParser()
#conffile = os.path.abspath('.') + os.sep + "settings.ini" #会在运行时引用主程序的当前路径
#ConfigParser读取的配置文件必须是实际绝对路径！
abspath = os.path.split(os.path.realpath(__file__))[0]
cfgfile = abspath  + os.sep + "settings.ini"
cf.read(cfgfile,encoding="utf-8-sig")
#print(cf.sections())

def get_testcase_file():
    return abspath + os.sep + '..' + os.sep + cf.get('FilePath','testcase_file')

def get_header_file():
    return abspath + os.sep + '..' + os.sep + cf.get('FilePath','header_file')

def get_data_file():
    return abspath + os.sep + '..' + os.sep + cf.get('FilePath','data_file')

def get_email_config():
    email_host = cf.get('Email','email_host')
    send_user = cf.get('Email','send_user')
    password = cf.get('Email','password')
    user_list = cf.get('Email','user_list').split(';')
    cc_list = cf.get('Email','cc_list').split(';')
    return({'email_host':email_host,'send_user':send_user,
            'password':password,'user_list':user_list,'cc_list':cc_list})
    
def get_root_url():
    return cf.get('AUT','root_url')

def get_verify():
    return cf.get('AUT','verify')

def get_log_level():
    return cf.get('Framework','log_level')

def get_db_type():
    return cf.get('DB', 'DB_type')

def get_db_host():
    return cf.get('DB', 'Host')

def get_db_port():
    return cf.get('DB', 'port')

def get_db_user():
    return cf.get('DB', 'username')

def get_db_pwd():
    return cf.get('DB', 'password')

def get_db_database():
    return cf.get('DB', 'database')