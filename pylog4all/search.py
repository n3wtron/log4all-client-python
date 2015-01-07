__author__ = 'Igor Maculan <n3wtron@gmail.com>'
import time

from datetime import datetime, timedelta
from util import getch


def print_log_result(log_result, full_log):
    for log in log_result:

        str_log = log['date'] + ":"
        str_log += log['application'] + ":"
        str_log += log['level'].ljust(5) + ":"
        str_log += log['message']
        if len(log['tags']) > 0:
            str_log += "## "
            for (k, v) in log['tags'].iteritems():
                str_log += "#" + k + ":" + str(v) + " "
        print str_log
        if full_log and 'stacktrace' in log:
            print(log['stacktrace'])


def search_log(cl, since, to, query='', full_log=False, result_per_page=10):
    page = 0
    ch = 'n'

    while page == 0 or (len(log_result) > 0 and ch == 'n'):
        log_result = cl.search_log(query, since, to, page=page, result_per_page=result_per_page, full=full_log)
        if len(log_result) > 0:
            print_log_result(log_result, full_log)
            print ('page ' + str(page + 1) + ' press n to next page')
            ch = getch()
            page += 1


def tail_log(cl, query='', full_log=False):
    since = datetime.now()
    while True:
        try:
            log_result = cl.tail_log(query, since, full=full_log)
            since = since + timedelta(seconds=1)
            print_log_result(log_result['result'], full_log)
            time.sleep(1)
        except KeyboardInterrupt:
            break