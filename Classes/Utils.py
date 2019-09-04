# -*- coding: utf-8 -*-

import os
import sys
import requests


class Utils:

    def __init__(self):
        pass
            
    @staticmethod
    def get_workdir():
        workdir = os.path.dirname(sys.argv[0])
        if workdir == '':
            workdir = os.getcwd()
        return workdir
    