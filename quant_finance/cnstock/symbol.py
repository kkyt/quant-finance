#coding: utf8

import re

from kuankr_utils import log, debug

PATTERN_STOCK  = 'SH600...|SH601...|SH603...|SH900...|SZ000...|SZ001...|SZ002...|SZ300...|SZ200...' #股票
PATTERN_FUND   = 'SH18....|SH5000..|SH500180|SH510...|SH000300|SZ18....|SZ159...' #基金
PATTERN_INDEX  = 'SH000...|SZ399...'   #指数
PATTERN_WARRANT= 'SH0310...|SZ5800...' #权证

PATTERN_ALL = '|'.join([PATTERN_STOCK, PATTERN_FUND, PATTERN_INDEX, PATTERN_WARRANT])


def is_index(symbol):
    """
    desc: symbol是否是指数
    example:
    -   args: ["SH000001"]
        ret : true
    """
    if not isinstance(symbol, basestring):
        return False
    return bool(re.match(PATTERN_INDEX, symbol))

def is_symbol(symbol):
    if not isinstance(symbol, basestring):
        return False
    return len(symbol)==8 and symbol[:2] in ['SH', 'SZ']

def is_stock(symbol):
    """
    desc: symbol是否是个股
    example:
    -   args: ["SH000001"]
        ret : false
    """
    return re.match(PATTERN_STOCK, symbol)

def normalize_symbol(s):
    """
    desc: 600690=>SH600690  InvalidSymbol=>None
    example:
    -   args: ["600690"]
        ret : SH600690
    """
    s = s.upper()
    if len(s)==len('SH600690'):
        if not is_symbol(s):
            return None
        else:
            return s
    elif len(s)==len('600690'):
        if s[0] in ['6']:
            return 'SH'+s
        else:
            return 'SZ'+s
    else:
        return s


