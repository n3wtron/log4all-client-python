import logging
from optparse import OptionParser
import sys
from pylog4all.search import search_log
from pylog4all.client import Log4allClient
from pylog4all import config
from pylog4all.util import add_common_parser_options
from dateutil import parser as dtparser

__author__ = 'Igor Maculan <n3wtron@gmail.com>'


def main():
    usage = "usage: %prog add [options] log_text"
    parser = OptionParser(usage=usage, )
    add_common_parser_options(parser)

    # SEARCH
    parser.add_option("-q", "--query", dest="action", action="store_const", const='search',
                                help="log4all search query")
    parser.add_option("--since", dest="since", action="store", help="search since")
    parser.add_option("--to", dest="to", action="store", help="search to")
    parser.add_option("--full", dest="full_log", action="store_true", help="log with stacktrace")
    parser.add_option("--num", dest="search_query_num", action="store",
                                help="number of results", default="10")

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
        if options.since is None or options.to is None:
            print ('--since and --to are mandatory in search')
            parser.print_help()
            exit(-2)
        search_log(cl, dtparser.parse(options.since), dtparser.parse(options.to), args, options.full_log)

if __name__ == '__main__':
    main()