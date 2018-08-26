# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:28:09 2018
@author: olivia
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import sys
sys.path.append('..')
from config.get_config import get_email_config


class SendEmail:
    
    def get_result(self,filename):
        '''从report文件里获取内容'''
        pass        
    

    def send_main(self,result_filename):
        
        email_host = get_email_config()['email_host']
        send_user = get_email_config()['send_user']
        password = get_email_config()['password']
        user_list = get_email_config()['user_list']
        cc_list = get_email_config()['cc_list']
        
        f = open(result_filename,'rb')
        content = f.read()
        f.close
        #self.send_mail(user_list,sub,content)
        #user = "Report Sender"+"<"+send_user+">"
        msg = MIMEMultipart()
        # 编写html类型的邮件正文，MIMEtext()用于定义邮件正文
        text = MIMEText(content,_subtype='html',_charset='utf-8')
        # 定义邮件正文标题
        text['Subject'] = Header("接口运行报告")
        msg['From'] = send_user
        msg['Cc'] = ";".join(cc_list) #抄送给自己，为解决163邮箱554 DT:SPM问题
        msg['To'] = ";".join(user_list)
        #server = smtplib.SMTP()
        #server.connect(email_host)
        server = smtplib.SMTP(email_host,25)
        server.login(send_user,password)
        #server.sendmail(send_user,user_list + cc_list,msg.as_string())
        server.sendmail(send_user,user_list+cc_list,msg.as_string())
        server.close()
        
        #cc给自己，使用客户端授权码登录，仍然SMTPDataError: (554, b'DT:SPM 163 smtp12,EMCowADXTVqSSIJb0plTDQ--.29699S2 1535264926,please see http://mail.163.com/help/help_spam_16.htm?ip=222.67.183.98&hostid=smtp12&time=1535264926')