# -*- coding: utf-8 -*-

import smtplib


class Mail:

    def __init__(self, host, port, security, username, password):
        self.smtp = smtplib.SMTP(host, port)
        self.security = security
        self.username = username
        if self.security:
            self.smtp.starttls()
            self.smtp.login(username, password)
        else:
            self.smtp.ehlo()

    def send_mail(self, subject, msg, receiver, sender=None):
        if self.security and sender:
            sender = self.username
        else:
            sender = 'john@doe.com'
        frm = 'From: <{}>'.format(sender)
        to = 'To: <{}>'.format(receiver)



        self.smtp.sendmail(sender, receiver, '{}\n{}\nSubject: {}\n{}'.format(frm, to, subject, msg))

    def end_connection(self):
        smtp.quit()