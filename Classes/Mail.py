# -*- coding: utf-8 -*-

import smtplib
import sys

try:
    smtp = smtplib.SMTP('localhost', 25)
    smtp.ehlo()

    sender = ''
    receiver = ''
    frm = 'From: <{}>'.format(sender)
    to = 'To: <{}>'.format(receiver)
    subject = 'Subject: '
    msg = ''

    smtp.sendmail(sender, receiver, '{}\n{}\n{}\n{}'.format(frm, to, subject, msg))
    smtp.quit()
except Exception as e:
    print("Error[{}]".format(e))
    sys.exit(1)

print('Enviado')
sys.exit(0)