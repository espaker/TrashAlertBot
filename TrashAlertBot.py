#!/usr/bin/python3
# -*- coding: utf-8 -*-

#######################################
########### Trash Alert Bot ###########
#######################################
#                _._                  #
#            __.{,_.).__              #
#         .-"           "-.           #
#       .'  __.........__  '.         #
#      /.-'`___.......___`'-.\        #
#     /_.-'` /   \ /   \ `'-._\       #
#     |     |   '/ \'   |     |       #
#     |      '-'     '-'      |       #
#     ;                       ;       #
#     _\         ___         /_       #
#    /  '.'-.__  ___  __.-'.'  \      #
#  _/_    `'-..._____...-'`    _\_    #
# /   \           .           /   \   #
# \____)         .           (____/   #
#     \___________.___________/       #
#       \___________________/         #
#      (_____________________)        #
#                                     #
# - Desenvolvido por Espaker Kaminski #
#######################################

import os
import sys
import logging
import signal
import threading
import time
import pprint

from logging.handlers import RotatingFileHandler
from flask import Flask, request, Response, send_file
from flask_cors import CORS

from Classes.Utils import Utils
from Classes.Skype import Skype
from Classes.Parser import Parser
from Classes.Mail import Mail
from Classes.RequestFormater import RequestFormatter

app_version = '1.0.1'
app = Flask(__name__)
CORS(app)

mail = None
skype = None

def monitoring():
    print("Loop inicio")
    time.sleep(5)
    print("Loop fim")

def initiate():
    log_main.info('Iniciando o TrashAlertBot versão: {}'.format(app_version))

    signal.signal(signal.SIGTERM, finalize)
    signal.signal(signal.SIGINT, finalize)

    global mail, skype

    try:
        usr = conf.get('Skype', 'User', fallback='')
        pwd = conf.get('Skype', 'Pass', fallback='')
        skype = Skype(usr, pwd)
        pprint(skype.get_contact())
    except Exception as e:
        log_main.exception('Erro ao inicializar conexão com o Skype: {}'.format(e))
        

    try:
        usr = conf.get('Mail', 'User', fallback='')
        pwd = conf.get('Mail', 'Pass', fallback='')
        host = conf.get('Mail', 'host', fallback='') 
        port = conf.getint('Mail', 'port', fallback='')
        security = conf.get('Mail', 'security', fallback='')
        mail = Mail(host, port, security, usr, pwd)
    except Exception as e:
        log_main.exception('Erro ao inicializar instanciar e-mail: {}'.format(e))
        
    # x = threading.Thread(target=monitoring)
    # x.start() 
        
def finalize(signum, desc):
    global execute, server
    log_main.info('Recebi o sinal [{}] Desc [{}], finalizando...'.format(signum, desc))

    log_main.warning('Limpando Cache Control ...')
    cache_control.clear()

    if server is not None:
        log_main.warning('Parando Serviço ...')
        server.stop()
    if execute:
        execute = False
    else:
        sys.exit(2)

if __name__ == '__main__':
    execute = True
    workdir = Utils.get_workdir()
    conf = Parser(os.path.join(workdir, 'config.ini')).conf_get()
    _level = conf.getint('Debug', 'Level', fallback=3)
    debug_dir = os.path.join(workdir, 'debug')
    log_file_path = os.path.join(debug_dir, 'TrashAlert.log')
    if not os.path.exists(debug_dir):
        os.mkdir(debug_dir, 0o775)
    log_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024 * 10, backupCount=10)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(RequestFormatter(
        '[%(asctime)s] | %(levelname)s | %(name)s | %(remote_addr)s | %(method)s | %(url)s | %(message)s'))
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(log_handler)
    log_main = logging.getLogger('TrashAlert:' + str(os.getpid()))
    app.logger.addHandler(log_handler)
    app.debug = True

    initiate()