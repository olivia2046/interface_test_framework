# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2018/10/16 17:24
desc: 和文件操作相关的常用库
'''
import logging,os,shutil,urllib,re
from functools import reduce

def clear_folder(folderpath):
    contents =  os.listdir(folderpath)
    if contents!=[]:
        for item in contents:
            item_path = os.path.join(folderpath, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)


def download_file(url,local_path):
    #logging.debug(url)
    #logging.debug(local_path)
    urllib.request.urlretrieve(url,local_path)

def get_legal_filaname(raw_filename):
    '''去除字符串中不能被文件名使用的非法字符'''
    #return raw_filename.translate(None, r"|\\?*<\":>+[]/'")
    pattern = r'[\\/:*?"<>|\r\n]+'
    return re.sub(pattern,'',raw_filename)




 