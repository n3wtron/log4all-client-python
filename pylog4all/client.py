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


def get_level_from_string(log_file_line):
    if 'DEBUG' in log_file_line:
        return 'DEBUG'
    if 'INFO' in log_file_line:
        return 'INFO'
    if 'WARN' in log_file_line:
        return 'WARN'
    if 'ERROR' in log_file_line:
        return 'ERROR'
    if 'FATAL' in log_file_line:
        return 'FATAL'
    return None


def add_log_line(log4all_client,application, log_file_line):
    global options
    log_stack = None
    log_level = options.level
    log_line = None
    if log_file_line[0] != '\t':
        # new log line
        log_line = log_file_line
        log_level = get_level_from_string(log_file_line)
        if log_level is None:
            log_level = options.level
        log_stack = None
    else:
        # probable stack trace
        if log_stack is None:
            log_stack = [log_file_line]
        else:
            log_stack.append(log_file_line)
    success, error = log4all_client.add_log(application, log_level, log_line, log_stack)
    if not success:
        if options.verbose:
            print("Log not added:" + error)


def main():
    usage = "usage: %prog [options] log_text "
    parser = OptionParser(usage=usage)
    parser.add_option("--user-setup", dest="user_setup", action="store_true", help="Setup user configuration")
    parser.add_option("-s", "--log4all-server", dest="server", action="store", help="log4all server url")
    parser.add_option("-a", "--application", dest="application", action="store", help="log4all application")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="show debug information")
    parser.add_option("-l", "--log-file", dest="log_file", action="store", help="log4 file to add")
    option_level_group = OptionGroup(parser, 'Levels(*)', 'Level is mandatory')
    option_level_group.add_option('-d', '--debug', dest='level', action='store_const', const='DEBUG')
    option_level_group.add_option('-i', '--info', dest='level', action='store_const', const='INFO')
    option_level_group.add_option('-w', '--warn', dest='level', action='store_const', const='WARN')
    option_level_group.add_option('-e', '--error', dest='level', action='store_const', const='ERROR')
    option_level_group.add_option('-f', '--fatal', dest='level', action='store_const', const='FATAL')
    parser.add_option_group(option_level_group)
    global options
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
            parser.print_help()
            exit(-2)

        if application.strip() == '':
            print ('application is mandatory')
            parser.print_help()
            exit(-2)

        if options.level is None:
            print ('level is mandatory')
            parser.print_help()
            exit(-2)

        if options.log_file is not None and not sys.stdin.isatty():
            print ('--log_file options is not compatible with pipe')
            parser.print_help()
            exit(-2)

        cl = Log4allClient(server)
        # check if is piped
        success, error = False, ''
        if not sys.stdin.isatty():
            stdin_lines = sys.stdin.readlines()
            stack = [line.rstrip() for line in stdin_lines]
            success, error = cl.add_log(application, options.level, args[1], stack)
            if not success:
                if options.verbose:
                    print("Log not added:" + error)
                sys.exit(-1)
        else:
            if options.log_file is not None:
                log_file = open(options.log_file)
                log_file_lines = log_file.readlines()
                try:
                    for log_file_line in log_file_lines:
                        add_log_line(cl, application, log_file_line)
                finally:
                    log_file.close()
            else:
                success, error = cl.add_log(application, options.level, args[1], None)
                if not success:
                    if options.verbose:
                        print("Log not added:" + error)
                    sys.exit(-1)


if __name__ == '__main__':
    main()
