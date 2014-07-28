from optparse import OptionGroup

__author__ = 'Igor Maculan <n3wtron@gmail.com>'
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


def add_common_parser_options(parser):
    parser.add_option("--user-setup", dest="user_setup", action="store_true", help="Setup user configuration")
    settings_group = OptionGroup(parser,'Settings',
                                 '**OPTIONAL** if user configuration is setted (--user-setup option )')
    settings_group.add_option("-s", "--log4all-server", dest="server", action="store",
                      help="log4all server url (mandatory if it's not configured by --user-setup)")
    settings_group.add_option("-a", "--application", dest="application", action="store",
                      help="log4all application (mandatory if it's not configured by --user-setup)")
    parser.add_option_group(settings_group)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="show debug information")