import os
import smtplib
from email import encoders
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import Global
from Global import username


def send_email(to_addr, body, subject="自动化中心", from_addr=username, password=Global.password,
               smtp_server='smtp.qq.com'):
    # 创建一个 MIMEText 对象，代表邮件正文
    msg = MIMEText(body, 'plain', 'utf-8')
    # 设置发件人和收件人
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    # 设置邮件主题
    msg['Subject'] = Header(subject, 'utf-8')
    # 创建 SMTP 对象，连接 SMTP 服务器
    smtp = smtplib.SMTP_SSL(smtp_server, 465)
    # 登录 SMTP 服务器
    smtp.login(from_addr, password)
    # 发送邮件
    smtp.sendmail(from_addr, [to_addr], msg.as_string())
    # 关闭连接
    smtp.quit()


def send_email_with_attachment(to_addr, body, file_path, subject="自动化中心", from_addr=username,
                               password=Global.password,
                               smtp_server='smtp.qq.com'):
    # 创建一个 MIMEMultipart 对象，代表邮件
    msg = MIMEMultipart()
    # 设置发件人和收件人
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    # 设置邮件主题
    msg['Subject'] = Header(subject, 'utf-8')

    # 创建一个 MIMEText 对象，代表邮件正文，并添加到邮件中
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # 读取附件文件并创建一个 MIMEApplication 对象
    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)
        file_mime = MIMEApplication(file_data, _subtype='octet-stream', _encoder=encoders.encode_base64)
        file_mime.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', file_name))
        # 将附件添加到邮件中
        msg.attach(file_mime)

    # 创建 SMTP 对象，连接 SMTP 服务器
    smtp = smtplib.SMTP_SSL(smtp_server, 465)
    # 登录 SMTP 服务器
    smtp.login(from_addr, password)
    # 发送邮件
    smtp.sendmail(from_addr, [to_addr], msg.as_string())
    # 关闭连接
    smtp.quit()
