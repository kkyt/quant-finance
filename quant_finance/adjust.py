#coding: utf8

"""
stock dividend 
"""

from kuankr_utils import log, debug

def adjust_factor(old_price, mgsg=None, mgpg=None, pgjg=None, mghl=None):
    if old_price is None:
        return None

    if mgsg is None: mgsg = 0
    if mgpg is None: mgpg = 0
    if pgjg is None: pgjg = 0
    if mghl is None: mghl = 0

    new_gb = 1.0 + mgsg + mgpg
    new_v = (old_price - mghl) + pgjg*mgpg
    new_price = new_v/new_gb
    x = new_price/old_price
    if x<=0:
        log.warn("xrate <=0!!: %s %s %s %s %s %s" % (x, old_price, mgsg, mgpg, pgjg, mghl))
        return None
    return x

