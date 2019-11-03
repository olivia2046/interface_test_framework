# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2018/9/26 13:53
desc:数据库相关的工具函数
'''
import sys,logging,re
import os
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'  # cx_Oracle 中文乱码问题

import pymysql,cx_Oracle
from DBUtils.PooledDB import PooledDB
sys.path.append('..')
from base.get_config import get_db_type,get_db_host,get_db_user,get_db_pwd,get_db_database,get_db_port,get_db_service_name,\
    get_neo4j_uri,get_neo4j_username,get_neo4j_pwd,get_mongodb_host,get_mongodb_port,get_mongodb_username,get_mongodb_password,\
    get_mongodb_mechanism,get_redis_host,get_redis_port
import base.globalvars as glo
from neo4j.v1 import GraphDatabase,basic_auth
logging.getLogger("GraphDatabase").setLevel(logging.WARNING)
from pymongo import MongoClient
from rediscluster import StrictRedisCluster


def init_conn_pool(dbname='DB'):
    if get_db_type(dbname).upper()=="MYSQL":
        #@TODO： 根据不同数据库选择不同 驱动
        pool = PooledDB(pymysql, 5, host=get_db_host(dbname), user=get_db_user(dbname), passwd=get_db_pwd(dbname), db=get_db_database(dbname),
                    port=int(get_db_port(dbname)))
        #glo.set_value("db_pool",pool)
    elif get_db_type(dbname).upper()=="ORACLE":
        pool = PooledDB(cx_Oracle, user = get_db_user(dbname), password = get_db_pwd(dbname),
                        dsn = "%s:%s/%s" %(get_db_host(dbname), get_db_port(dbname), get_db_service_name(dbname)), mincached=20, maxcached=200)
    else:
        pool = None
    poolname = (dbname+'_pool').lower()
    glo.set_value(poolname, pool)


def get_conn_pool(dbname='DB'):
    poolname = (dbname + '_pool').lower()
    return glo.get_value(poolname)

def execute_query(sql,*args,dbname='DB'): #使用默认参数时，默认参数的位置要在args之后kwargs之前
    """
    :param sql: 待执行的sql
    :param dbname: 执行sql的数据库名，为测试框架配置文件中'DB'开头的section名
    :param args: tuple, list or dict，为解决执行插入None值的问题
    https://blog.csdn.net/legendary_Dragon/article/details/81254386
    调用方法：
    sql = "INSERT INTO test VALUES (%s,%s)"
    test_tuple=(3,None)
    execute_query(sql,*test_tuple,dbname="DB_XXX")

    :return: 查询的结果
    """
    pool = get_conn_pool(dbname)
    if pool is None:
        init_conn_pool(dbname)
        pool = get_conn_pool(dbname)

    conn = pool.connection()  # 每次需要数据库连接就是用connection（）函数获取连接就好了
    cursor = conn.cursor()

    try:
        # 执行SQL语句
        #logging.debug("sql: %s"%sql)
        cursor.execute(sql,args)
        conn.commit() # 对于增删改操作必须提交commit

        # 获取count
        results = cursor.fetchall()
        #logging.debug(results)
        return list(results) #PooledDB MySQl query执行结果为tuple， oracle为list,统一转换为list
    except Exception as e:
        logging.error("Error: unable to execute query, %s"%e)
        return []
    finally:
        cursor.close()
        conn.close()


def get_query_string(input_str):
    """

    :param input_str:
    :return:
    """
    pattern = 'select.+?;'
    #result = re.search(pattern,input_str)
    result = re.compile(pattern,re.S|re.I).search(input_str)
    if result is None: # 如果不能匹配到分号，则匹配到结尾
        pattern = 'select.+'
        #result = re.search(pattern,input_str)
        result = re.compile(pattern, re.S).search(input_str)
    if result is not None:
        return result.group()
    else:
        return ""

def get_neo4j_driver():
    uri = get_neo4j_uri()
    if uri is not None:
        #return GraphDatabase.driver(uri, auth=(get_neo4j_username(), get_neo4j_pwd()))
        return GraphDatabase.driver(uri, auth=basic_auth(get_neo4j_username(), get_neo4j_pwd()))
    else:
        return None


def get_mongodb_connection():
    host = get_mongodb_host()
    port = get_mongodb_port()
    username = get_mongodb_username()
    password = get_mongodb_password()
    mechanism = get_mongodb_mechanism()
    try:
        conn = MongoClient(host, int(port))
        db_auth = conn.admin
        db_auth.authenticate(username,password,mechanism=mechanism)
        return conn
    except Exception as e:
        return None

def get_redis_connection():
    host = get_redis_host()
    port = get_redis_port()

    startup_nodes = [{"host": host, "port": port}]
    try:
        conn = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        return conn
    except Exception as e:
        logging.debug("Get Redis connection failed")
        return None
