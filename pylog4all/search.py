__author__ = 'Igor Maculan <n3wtron@gmail.com>'
from datetime import datetime
import time

from util import getch


def print_log_result(log_result, full_log):
    for log in log_result['logs']:
        print (str(datetime.fromtimestamp(log['date'])) + " : " +
               log['application'] + " : " +
               log['level'].ljust(5) + " : " +
               log['message'])
        if full_log and 'stacktrace' in log:
            print(log['stacktrace'])


def search_log(cl, since, to, query='', full_log=False, result_per_page=10):
    page = 0
    ch = 'n'

    while page == 0 or (page * result_per_page < log_result['n_rows'] and ch == 'n'):
        log_result = cl.search_log(query, since, to, page=page, result_per_page=result_per_page, full=full_log)
        max_page = int(log_result['n_rows']) / result_per_page
        print_log_result(log_result, full_log)
        if page < max_page:
            print ('page ' + str(page + 1) + ' of ' + str() + str(max_page + 1) + ' press n to next page')
            ch = getch()
        page += 1


def tail_log(cl, query='', full_log=False):
    since = datetime.now()
    while True:
        try:
            log_result = cl.tail_log(query, since, full=full_log)
            since = datetime.now()
            print_log_result(log_result, full_log)
            time.sleep(1)
        except KeyboardInterrupt:
            break