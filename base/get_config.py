# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 13:46:36 2018
@author: olivia
Description: 获取配置文件各项内容，避免在需要相应内容的模块处分别调用configparser
"""

from configparser import ConfigParser
import os,sys,logging
sys.path.append('..')
import base.globalvars as glo
from util.crypt_util import decryption
cf=ConfigParser()
#cfgfile = os.path.abspath('.') + os.sep + "settings.ini" #会在运行时引用主程序的当前路径
#ConfigParser读取的配置文件必须是实际绝对路径！
abspath = os.path.split(os.path.realpath(__file__))[0]
cfgfile = abspath  + '/../config/'  + "settings - %s.ini"%glo.get_value("config_name")
cf.read(cfgfile,encoding="utf-8-sig")
#print(cf.sections())

def get_url_dict():
    if "URLs" in cf:
        return cf['URLs']
    else:
        return {}


def get_test_type():
    try:
        return cf.get('AUT', 'test_type')
    except Exception as e:
        logging.debug("e")
        return 'interface'


def get_testcase_file():
    try:
        return abspath + os.sep + '..' + os.sep + cf.get('FilePath','testcase_file')
    except Exception as e:
        return ""

def get_header_file():
    try:
        return abspath + os.sep + '..' + os.sep + cf.get('FilePath','header_file')
    except Exception as e:
        return ""

def get_data_file():
    try:
        return abspath + os.sep + '..' + os.sep + cf.get('FilePath','data_file')
    except Exception as e:
        return ""

def get_tc_rootdir():
    try:
        return abspath + os.sep + '..' + os.sep + cf.get('FilePath','tc_rootdir')
    except Exception as e:
        return ""

def get_data_rootdir():
    try:
        return abspath + os.sep + '..' + os.sep + cf.get('FilePath','data_rootdir')
    except Exception as e:
        return ""

def get_email_config():
    try:
        email_host = cf.get('Email','email_host')
        send_user = cf.get('Email','send_user')
        password = decryption(cf.get('Email','password')).decode() #解密再把byte解码成string
        user_list_str = cf.get('Email', 'user_list')
        user_list = []
        if ',' in user_list_str:
            user_list = user_list_str.split(',')
        else:
            user_list = user_list_str.split(';')
        cc_list = []
        cc_list_str = cf.get('Email','cc_list')
        if ',' in cc_list_str:
            cc_list = cc_list_str.split(',')
        else:
            cc_list = cc_list_str.split(';')


        return({'email_host':email_host,'send_user':send_user,
                'password':password,'user_list':user_list,'cc_list':cc_list})
    except Exception as e:
        return {}
    
def get_account_url():
    try:
        return cf.get('AUT', 'account_url')
    except Exception as e:
        logging.debug("e")
        return ''

def get_frontend_root_url():
    try:
        return cf.get('AUT','frontend_root_url')
    except Exception as e:
        return ""

def get_backend_root_url():
    try:
        return cf.get('AUT','backend_root_url')
    except Exception as e:
        return ""

def get_verify_str():
    try:
        return cf.get('AUT','verify')
    except Exception as e:
        return None

def get_certfile_path():
    try:
        return cf.get('AUT','cert')
    except Exception as e:
        return ""

def get_verify_cert():
    verify = get_verify_str()
    if verify.upper() == 'FALSE':
        # logging.debug("no need to vefify certification.")
        # verify = eval("False")
        verify = False
        cert = None
    else:
        verify = True
        cert = sys.path[0] + '/../' + get_certfile_path()
    return verify,cert

def get_log_level():
    try:
        level =  cf.get('Framework','log_level')
        return level
    except Exception as e:
        return "DEBUG"

def get_db_type(dbname='DB'):
    try:
        return cf.get(dbname, 'db_type')
    except Exception as e:
        return ""

def get_db_host(dbname='DB'):
    try:
        return cf.get(dbname, 'host')
    except Exception as e:
        return ""

def get_db_port(dbname='DB'):
    try:
        return cf.get(dbname, 'port')
    except Exception as e:
        return ""

def get_db_user(dbname='DB'):
    try:
        return cf.get(dbname, 'username')
    except Exception as e:
        return ""

def get_db_pwd(dbname='DB'):
    try:
        pwdstr = cf.get(dbname, 'password')
        return decryption(pwdstr).decode() #解密再把byte解码成string
    except Exception as e:
        return ""

#def get_db_sid():
#    return cf.get('DB','sid')

def get_db_service_name(dbname='DB'):
    try:
        '''oracle_cx 需要使用service name而不是sid
        查看Oracle service name:select value from v$parameter where name like '%service_name%'''
        return cf.get(dbname,'service_name')
    except Exception as e:
        return ""


def get_db_database(dbname='DB'):
    '''MySQL连接的database'''
    try:
        return cf.get(dbname, 'database')
    except:
        logging.debug("cannot find DB->database section")

def get_neo4j_uri():
    try:
        return cf.get('NEO4J', 'uri')
    except:
        logging.debug("cannot find NEO4J->uri section")
        return ""

def get_neo4j_username():
    try:
        return cf.get('NEO4J', 'username')
    except:
        logging.debug("cannot find NEO4J->username section")

def get_neo4j_pwd():
    try:
        pwdstr =  cf.get('NEO4J', 'password')
        return decryption(pwdstr).decode()
    except:
        logging.debug("cannot find NEO4J->password section")

def get_run_case_level():
    try:
        # 返回需要运行的case level的列表
        case_level_str = cf.get('Framework','run_case_level').replace(" ","")
        # if case_level_str=='':
        #     case_level_str='Smoke,Sanity,Regression'
    except Exception as e:\
        #case_level_str = 'Smoke,Sanity,Regression'
        case_level_str =''
    case_levels = case_level_str.split(',')
    if case_levels==['']:
        case_levels=[]
    return case_levels

def get_run_case_folder():
    try:
        # 返回需要运行的case level的列表
        case_folder_str = cf.get('Framework','run_case_folder').replace(" ","")
    except Exception as e:\
        case_folder_str =''
    case_folders = case_folder_str.split(',')
    if case_folders==['']:
        case_folders=[]
    return case_folders

def get_run_case_type():
    # 返回需要运行的case类型列表
    try:
        case_type_str = cf.get('Framework','run_case_type').replace(" ","")
        if case_type_str=="":
            case_type_str = "Excel,Code"
    except Exception as e:
        case_type_str = "Excel,Code"
    return case_type_str.split(',')

def get_and_set_global_vars():
    if cf.has_section('Globals'):
        '''从配置文件中读取需要设置的全局变量（不同于配置文件中在整个框架使用的其他变量，此处的全局变量只在特定项目中使用，因此不同配置文件做不同设置'''
        for var in cf['Globals'].keys():
            glo.set_value(var,cf.get('Globals',var))

def get_mongodb_host():
    if cf.has_section('MongoDB'):
        try:
            return cf.get('MongoDB', 'host')
        except:
            logging.debug("cannot find MongoDB->host section")
            return ""
    else:
        return ""

def get_mongodb_port():
    if cf.has_section('MongoDB'):
        try:
            return cf.get('MongoDB', 'port')
        except:
            logging.debug("cannot find MongoDB->port section")
            return ""
    else:
        return ""

def get_mongodb_username():
    if cf.has_section('MongoDB'):
        try:
            return cf.get('MongoDB', 'username')
        except:
            logging.debug("cannot find MongoDB->username section")
            return ""
    else:
        return ""

def get_mongodb_password():
    if cf.has_section('MongoDB'):
        try:
            password= cf.get('MongoDB', 'password')
            return decryption(password).decode()
        except:
            logging.debug("cannot find MongoDB->password section")
            return ""
    else:
        return ""

def get_mongodb_mechanism():
    if cf.has_section('MongoDB'):
        try:
            return cf.get('MongoDB', 'mechanism')
        except:
            logging.debug("cannot find MongoDB->mechanism section")
            return ""
    else:
        return ""

def get_redis_host():
    if cf.has_section('Redis'):
        try:
            return cf.get('Redis', 'host')
        except:
            logging.debug("cannot find Redis->host section")
            return ""
    else:
        return ""

def get_redis_port():
    if cf.has_section('Redis'):
        try:
            return cf.get('Redis', 'port')
        except:
            logging.debug("cannot find Redis->port section")
            return ""
    else:
        return ""

def get_environment():
    if cf.has_section('AUT'):
        try:
            return cf.get('AUT','environment')
        except:
            logging.debug("cannot find AUT->environment section")
            return ""
    else:
        return ""

