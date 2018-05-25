"""Convenience print methods"""
from datetime import datetime

def msg(message):
    """print a string to the screen"""
    print(message)

def msgt(message, with_time=True):
    """Print a string, separated by dashes before and after"""
    if with_time:
        time_str = '\n(%s)' % datetime.now().strftime('%H:%M:%S.%f on %Y/%m/%d')
    else:
        time_str = ''

    print('-' * 40)
    msg('%s%s' % (message, time_str))
    print('-' * 40)
