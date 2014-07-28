import json
import os
from os.path import expanduser

__author__ = 'Igor Maculan <n3wtron@gmail.com>'

def get_conf_folder_path():
    home_dir = expanduser("~")
    return home_dir + os.sep + '.log4all'


def get_conf_file_path():
    return get_conf_folder_path() + os.sep + '/log4all.conf'


def get_user_conf():
    log4all_user_conf = get_conf_file_path()
    if os.path.exists(log4all_user_conf):
        conf_file = open(log4all_user_conf, 'r')
        conf = json.load(conf_file)
        conf_file.close()
        return conf
    else:
        return dict(server='', application='')


def write_user_conf(conf):
    if not os.path.exists(get_conf_folder_path()):
        os.makedirs(get_conf_folder_path())

    log4all_user_conf = get_conf_file_path()
    conf_file = open(log4all_user_conf, 'w')
    json.dump(conf, conf_file, indent=True)
    conf_file.close()


def user_setup():
    conf = get_user_conf()
    input_server = raw_input("Log4all server(" + conf['server'] + "): ")
    if input_server.strip() != '':
        conf['server'] = input_server
    input_application = raw_input("Log4all application(" + conf['application'] + "): ")
    if input_application.strip() != '':
        conf['application'] = input_application
    write_user_conf(conf)