import logging
from optparse import OptionParser
import sys
from pylog4all.search import tail_log
from pylog4all.client import Log4allClient
from pylog4all import config
from pylog4all.util import add_common_parser_options

__author__ = 'Igor Maculan <n3wtron@gmail.com>'

def main():
    usage = "usage: %prog [options] [log_text|search_query]"
    parser = OptionParser(usage=usage, )
    add_common_parser_options(parser)

    parser.add_option("--full", dest="full_log", action="store_true", help="log with stacktrace")
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

        if server.strip() == '':
            print ('server is mandatory')
            parser.print_help()
            exit(-2)

        cl = Log4allClient(server)
        tail_log(cl,args,options.full_log)

if __name__ == '__main__':
    main()