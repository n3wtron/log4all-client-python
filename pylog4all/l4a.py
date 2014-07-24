import json
from optparse import OptionParser, OptionGroup
import os
from os.path import expanduser
import sys
import logging
from dateutil import parser as dtparser

from client import Log4allClient
from add import add_log
from search import search_log, tail_log


logging.basicConfig(level=logging.DEBUG)


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
    usage = "usage: %prog [options] [log_text|search_query]"
    parser = OptionParser(usage=usage, )

    parser.add_option("--user-setup", dest="user_setup", action="store_true", help="Setup user configuration")
    parser.add_option("-s", "--log4all-server", dest="server", action="store",
                      help="log4all server url (mandatory if it's not configured by --user-setup)")
    parser.add_option("-a", "--application", dest="application", action="store",
                      help="log4all application (mandatory if it's not configured by --user-setup)")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="show debug information")

    option_add_group = OptionGroup(parser, 'Add Log')
    option_add_group.add_option("-l", "--log-file", dest="log_file", action="store", help="log4 file to add")

    # SEARCH
    option_search_group = OptionGroup(parser, 'Search Log')
    option_add_group.add_option("-q", "--query", dest="action", action="store_const", const='search',
                                help="log4all search query")
    option_add_group.add_option("--since", dest="since", action="store", help="search since")
    option_add_group.add_option("--to", dest="to", action="store", help="search to")
    option_add_group.add_option("--full", dest="full_log", action="store_true", help="log with stacktrace")
    option_add_group.add_option("--num", dest="search_query_num", action="store",
                                help="number of results", default="10")

    option_add_group.add_option("-t", "--tail", dest="action", action="store_const", const='tail',
                                help="tail on log4all server")

    parser.add_option_group(option_add_group)

    # LEVELS
    option_level_group = OptionGroup(parser, 'Log Levels', '')
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
            parser.print_help()
            exit(-2)

        if application.strip() == '':
            print ('application is mandatory')
            parser.print_help()
            exit(-2)

        if options.action is None:
            options.action = 'add'

        cl = Log4allClient(server)

        if options.action == 'add':
            if options.level is None:
                print ('level is mandatory')
                parser.print_help()
                exit(-2)

            if options.log_file is not None and not sys.stdin.isatty():
                print ('--log_file options is not compatible with pipe')
                parser.print_help()
                exit(-2)
            inline_log = None
            if len(args) == 2:
                inline_log = args[1]
            add_log(cl, application, options.level, inline_log, options.log_file)

        if options.action == 'search':
            if options.since is None or options.to is None:
                print ('--since and --to are mandatory in search')
                parser.print_help()
                exit(-2)
            search_log(cl, dtparser.parse(options.since), dtparser.parse(options.to), args, options.full_log)

        if options.action == 'tail':
            tail_log(cl,args,options.full_log)


if __name__ == '__main__':
    main()
