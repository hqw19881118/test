# !/usr/bin/env python
#encoding=utf-8
"""
@desc: 
@version: 1.0
@author: huangqingwei(huangqingwei@baidu.com)
@license: Copyright (c) 2016 Baidu.com,Inc. All Rights Reserved
@software: PyCharm Community Edition
@file: send_mail.py
@time: 2016/10/31 20:46
"""
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email import Encoders
from email.header import Header
from optparse import OptionParser


def send_mails(subject, sender, receivers, body, is_html=False, attachments=None):
    """

    :param subject: 邮件标题
    :param sender: 邮件发送方，可选，默认为ktv-rock@baidu.com
    :param receivers: 收件人列表
    :param body: 邮件内容
    :param is_html: 是否以html格式发送
    :param attachments: 附件列表
    :return: None
    """
    mail_from = "ktv-rock@baidu.com"
    if not sender:
        sender = mail_from
    if not subject:
        raise ValueError(u'邮件标题为空')
    if type(receivers) is not list:
        raise ValueError(u'receivers should be a list, but a %s is given.' % type(receivers))
    print mail_from, receivers
    msg_root = MIMEMultipart()
    msg_root["Accept-Charset"] = "UTF-8"
    msg_root["Accept-Language"] = "zh-CN"
    msg_root['Subject'] = Header(subject, "UTF-8")
    msg_root['From'] = sender
    msg_root['To'] = ','.join(receivers)
    msg_root.preamble = '%s is a MIME message' % subject

    msg_alternative = MIMEMultipart("alternative")
    msg_root.attach(msg_alternative)

    if not body:
        body = sys.stdin.read()

    msg_text = MIMEText(body)
    msg_text.set_charset("UTF-8")
    msg_alternative.attach(msg_text)

    if is_html:
        msg_text = MIMEText(body, 'html')
        msg_text.set_charset("UTF-8")
        msg_alternative.attach(msg_text)

    if attachments:
        for f in attachments:
            if os.path.exists(f):
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(f, "rb").read())
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename="%s"' % os.path.basename(f))
                msg_root.attach(part)
            else:
                print "%s not exists" % f

    s = smtplib.SMTP('proxy-in.baidu.com')
    s.sendmail(mail_from, receivers, msg_root.as_string())
    s.quit()


def main():
    usage_str = "usage: %prog [options] subject"
    version_str = "%prog 1.0.0"
    parser = OptionParser(usage=usage_str, version=version_str)
    parser.add_option("-f", "--from", dest="sender", default="",
                      help="set sender", type="string")
    parser.add_option("-t", "--to", action="append", dest="receivers", default=[],
                      help="add receiver", type="string")
    parser.add_option("-a", "--attach", action="append", dest="attachments", default=[],
                      help="add attachment", type="string")
    parser.add_option("-b", "--body", dest="body", default="",
                      help="set mail body,read from stdin if not set", type="string")
    parser.add_option("-r", "--rich", dest="rich", default=False, action="store_true",
                      help="send html body")
    parser.add_option("-p", "--plain", dest="rich", action="store_false",
                      help="send plain body,default")

    (options, args) = parser.parse_args()
    nargs = len(args)
    if nargs != 1:
        parser.error("missing required params")
        sys.exit(1)
    subject = args[0]
    send_mails(subject, options.sender, options.receivers, options.body, options.rich,
               options.attachments)


def test():
    send_mails("邮件主题", None, ['test@baidu.com'],
               '这是邮件详情1234567890-qwertyuiop[]|}{PL:<>+_)(*&^%$#@!')


if __name__ == '__main__':
    test()
