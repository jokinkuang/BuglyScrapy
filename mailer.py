# -*- coding:utf-8 -*-
# @author jokinkuang

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 第三方 SMTP 服务
mail_host = "smtp.jokin.com"  # 设置服务器
mail_user = "kuangzukai@jokin.com"  # 用户名
mail_pass = "Kuang"  # 口令

def sendEmail(to, subject, body):
    # Create message container - the correct MIME type is multipart/alternative.
    frm = mail_user

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = frm
    msg['To'] = to[0]

    # Create the body of the message (a plain-text and an HTML version).
    html = body

    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(body, 'html', "utf-8")

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)

    # Send the message via local SMTP server.
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(frm, mail_pass)
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        smtpObj.sendmail(frm, to, msg.as_string())
        smtpObj.quit()
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"