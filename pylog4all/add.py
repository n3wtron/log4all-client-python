__author__ = 'Igor Maculan <n3wtron@gmail.com>'
import sys


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


def add_log_line(log4all_client, application, level, log_file_lines):
    log_stack = None
    log_level = level
    log_message = None
    for log_file_line in log_file_lines:
        if log_file_line[0] != '\t':
            # new log line
            if log_message is not None:
                success, error = log4all_client.add_log(application, log_level, log_message, log_stack)
                if not success:
                    sys.stderr.write("Log not added:" + error + '\n')
            log_message = log_file_line
            log_level = get_level_from_string(log_file_line)
            if log_level is None:
                log_level = level
            log_stack = None
        else:
            # probable stack trace
            if log_stack is None:
                log_stack = log_file_line
            else:
                log_stack += log_file_line

    if log_message is not None:
        success, error = log4all_client.add_log(application, log_level, log_message, log_stack)
        if not success:
            sys.stderr.write("Log not added:" + error + '\n')


def add_log(cl, application, level, log, log_file=None):
    if log is None and log_file is None:
        sys.stderr.write("Log message is mandatory \n")
        sys.exit(-1)
    success, error = False, ''
    # check if is piped
    if not sys.stdin.isatty():
        stack = sys.stdin.read()
        success, error = cl.add_log(application, level, log, stack)
        if not success:
            sys.stderr.write("Log not added:" + error + '\n')
            sys.exit(-1)
    else:
        if log_file is not None:
            log_file = open(log_file)
            log_file_lines = log_file.readlines()
            try:
                add_log_line(cl, application, level, log_file_lines)
            finally:
                log_file.close()
        else:
            success, error = cl.add_log(application, level, log, None)
            if not success:
                sys.stderr.write("Log not added:" + error + '\n')
                sys.exit(-1)