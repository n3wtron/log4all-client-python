from optparse import OptionParser, OptionGroup
import sys
import logging

from client import Log4allClient
from add import add_log
from pylog4all import config
from pylog4all.util import add_common_parser_options


def main():
    usage = "usage: %prog [options] [log_text]"
    parser = OptionParser(usage=usage, )
    add_common_parser_options(parser)

    parser.add_option("-l", "--log-file", dest="log_file", action="store", help="log4 file to add")

    # LEVELS
    option_level_group = OptionGroup(parser, 'Log Levels', '')
    option_level_group.add_option('-d', '--debug', dest='level', action='store_const', const='DEBUG')
    option_level_group.add_option('-i', '--info', dest='level', action='store_const', const='INFO')
    option_level_group.add_option('-w', '--warn', dest='level', action='store_const', const='WARN')
    option_level_group.add_option('-e', '--error', dest='level', action='store_const', const='ERROR')
    option_level_group.add_option('-f', '--fatal', dest='level', action='store_const', const='FATAL')
    parser.add_option_group(option_level_group)

    (options, args) = parser.parse_args(sys.argv[1:])
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    if options.user_setup:
        config.user_setup()
    else:
        user_conf = config.get_user_conf()
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

        cl = Log4allClient(server)

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


if __name__ == '__main__':
    main()
