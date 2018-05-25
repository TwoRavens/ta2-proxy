"""Convenience print methods"""
from datetime import datetime

def msg(message):
    """print a string to the screen"""
    print(message)

def dashes():
    msg('-' * 40)

def msgt(message):
    """Print a string, separated by dashes before and after"""
    dashes()
    msg(message)
    dashes()

def msgd(message):
    """Print a string, separated by dashes before and after"""
    time_str = '\n(%s)' % \
               (datetime.now().strftime('%H:%M:%S.%f on %Y/%m/%d'))

    msgt('%s%s' % (message, time_str))
