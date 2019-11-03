# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 11:28:09 2018
@author: olivia
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import sys,re
from lxml import etree
from bs4 import BeautifulSoup
sys.path.append('..')
from base.get_config import get_email_config


class SendEmail:
    
    def get_result(self,content):
        html = etree.HTML(content)
        testresult = html.xpath("//html/body/div[@class='heading']/p[3]/text()") #数组

        result_str = testresult[0].strip()
        #print(result_str)
        pattern = r"(Pass \d+)? ?(Failure \d+)? ?(Error \d+)?"
        matches = re.match(pattern,result_str)
        #print(matches)
        #print(matches.group(1))
        #print(matches.group(2))
        #print(matches.group(3))
        if matches is not None and (matches.group(2) is not None or matches.group(3) is not None):
            testpass = False
        else:
            testpass = True

        print(result_str,testpass)
        return result_str,testpass

    def get_failed_or_error_case_names(self, content):
        html = etree.HTML(content)
        #print(content)
        rows = html.xpath("//table[@id='result_table']/tr") #content中没有tbody节点，why?
        prefix=""
        fail_or_error_cases=[]
        for row in rows:
            if "class" in row.keys() and row.get("class") is not None and row.get("class")=="failClass":
                prefix=row.xpath("./td[1]/text()")[0]
            elif "id" in row.keys() and row.get("id") is not None and row.get("id").startswith('ft'):
                if row.xpath("./td[@class='failCase']")!=[]:
                    fail_or_error_cases.append(prefix + '.' + row.xpath("./td[@class='failCase']/div/text()")[0])
                else:
                    fail_or_error_cases.append(prefix + '.' + row.xpath("./td[@class='errorCase']/div/text()")[0])
        #failed_cases = html.xpath("//html/body/table[@id='result_table']/tbody/tr/td[@class='failCase']/div")  # 数组
        #failed_cases = html.xpath("//tr/td[@class='failCase']/div/text()")  # 数组,content中没有tbody节点，why?
        print(fail_or_error_cases)
        if fail_or_error_cases==[]:
            return ""
        else:
            return '\n'.join(fail_or_error_cases)

    def remove_script(self,content):
        soup = BeautifulSoup(content, 'html.parser')
        soup.find('p', id='show_detail_line').decompose()
        links = soup.find_all('a')
        for n in links:
            n.decompose()
        return str(soup)

    def send_main(self, result_filepath, subject, condition):
        
        email_host = get_email_config()['email_host']
        send_user = get_email_config()['send_user']
        password = get_email_config()['password']
        user_list = get_email_config()['user_list']
        cc_list = get_email_config()['cc_list']
        
        f = open(result_filepath, 'rb')
        content = f.read()
        f.close
        #self.send_mail(user_list,sub,content)

        # 编写html类型的邮件正文，MIMEtext()用于定义邮件正文
        #msg = MIMEText(content,_subtype='html',_charset='utf-8')
        # 编写带附件的邮件
        msg = MIMEMultipart()
        # 定义邮件正文标题
        result_str, testpass = self.get_result(content)
        msg['Subject'] = Header("%s-%s"%(subject,result_str))
        msg['From'] = send_user
        msg['Cc'] = ";".join(cc_list) #抄送给自己，为解决163邮箱554 DT:SPM问题
        msg['To'] = ";".join(user_list)
        # 邮件正文内容
        #body = MIMEText(self.remove_script(content), "html", "utf-8")
        #msg.attach(body)  # 挂起
        #msg.attach(MIMEText('', 'plain', 'utf-8'))
        body = MIMEText("Failed or Error Cases:\n\n" + self.get_failed_or_error_case_names(content), "html", "utf-8")
        msg.attach(body)  # 挂起
        # 构造附件，传送content内容
        att1 = MIMEText(content, 'html', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="%s"' % result_filepath.split('/')[-1]
        msg.attach(att1)
        server = smtplib.SMTP(email_host,25)
        # server.ehlo()
        # server.starttls()
        server.login(send_user,password)

        if condition.lower()=='any' or (condition.lower()=='fail' and testpass is False):
            server.sendmail(send_user,user_list+cc_list,msg.as_string())
        server.close()
