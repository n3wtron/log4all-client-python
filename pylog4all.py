#!/usr/bin/env python
import json
from optparse import OptionParser, OptionGroup
import os
from os.path import expanduser
import urllib2
import sys


class Log4allClient:
    def __init__(self, host, proxy={}):
        self.host = host + "/api/logs/add"
        self.proxy = urllib2.ProxyHandler(proxy)
        urllib2.install_opener(urllib2.build_opener(self.proxy))

    def add_log(self, application, level, message, stack=None):
        data = json.dumps(dict(application=application, level=level, log=message, stack=stack))
        req = urllib2.Request(self.host, data, {'Content-Type': 'application/json'})
        res = urllib2.urlopen(req)
        result = json.loads(res.read())
        return result['result'], result['message']


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


def main():
    parser = OptionParser()
    parser.add_option("--user-setup", dest="user_setup", action="store_true", help="Setup user configuration")
    parser.add_option("-s", "--log4all-server", dest="server", action="store", help="log4all server url")
    parser.add_option("-a", "--application", dest="application", action="store", help="log4all application")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="show debug information")
    option_level_group = OptionGroup(parser, 'Levels')
    option_level_group.add_option('-d', '--debug', dest='level', action='store_const', const='DEBUG')
    option_level_group.add_option('-i', '--info', dest='level', action='store_const', const='INFO')
    option_level_group.add_option('-w', '--warn', dest='level', action='store_const', const='WARN')
    option_level_group.add_option('-e', '--error', dest='level', action='store_const', const='ERROR')
    option_level_group.add_option('-f', '--fatal', dest='level', action='store_const', const='FATAL')
    parser.add_option_group(option_level_group)

    (options, args) = parser.parse_args(sys.argv)
    if options.user_setup:
        user_setup()
    else:
        user_conf = get_user_conf()
        if options.server is None:
            server = user_conf['server']
        else:
            server = options.server

        if options.application is None:
            application = user_conf['application']
        else:
            application = options.application

        if server.strip() == '':
            print ('server is mandatory')
            exit(-2)

        if application.strip() == '':
            print ('application is mandatory')
            exit(-2)

        if options.level is None:
            print ('level is mandatory')
            exit(-2)

        cl = Log4allClient(server)

        # check if is piped
        if not sys.stdin.isatty():
            stack = sys.stdin.readlines()
        else:
            stack = None

        success, error = cl.add_log(application, options.level, args[1], stack)
        if success:
            if options.verbose:
                print("Log added")
        else:
            if options.verbose:
                print("Log not added:" + error)
            sys.exit(-1)


if __name__ == '__main__':
    main()
