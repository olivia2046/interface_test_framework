# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2018/10/8 11:43
desc: 有关加密/解密的工具库，后期可替换更复杂的加密/解密方法
'''

import base64
from cryptography.hazmat.primitives.ciphers import algorithms
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

def decryption(code):
    return  base64.b64decode(bytes(code,encoding='utf-8'))

def aes_encrypt(text, mode, key,iv):
    #cryptor = AES.new(key.encode('utf-8'), mode, b'IzMoaK3jSeBgDKQR')
    cryptor = AES.new(key.encode('utf-8'), mode, iv.encode('utf-8'))
    #text = text.encode('utf-8')

    # 这里密钥key 长度必须为16（AES-128）,
    # 24（AES-192）,或者32 （AES-256）Bytes 长度
    # 目前AES-128 足够目前使用

    length = 16  # 这里只是用于下面取余
    count = len(text)  # 字符长度不同所以不能直接用，需要先编码转成字节
    #print(count)
    if (count % length != 0):
        add = length - (count % length)
    else:
        add = 0  # 看看你们对接是满16的时候加上16还是0.这里注意
    text = text + ('\0' * add)  # 其它语言nopadding时，python还是需要‘\0’或'\x00'这里注意与其它语言对接注意
    #text = text + ('\x00' * add)

    ciphertext = cryptor.encrypt(text.encode('utf-8'))

    # # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # # 所以这里统一把加密后的字符串转化为16进制字符串
    # return b2a_hex(ciphertext)
    return str(base64.b64encode(ciphertext),encoding='utf-8')

if __name__=="__main__":
    print(aes_encrypt("test", AES.MODE_CBC, "jSt3SttxMbBml3tc"))


