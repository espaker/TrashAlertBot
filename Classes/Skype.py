# -*- coding: utf-8 -*-

import skpy


class Skype:

    def __init__(self, username, password):
        self.sk = skpy.Skype(username, password)

    def get_user(self):
        return self.sk.user

    def get_contact(self):
        return self.sk.contacts["Id": "espaker666"]