#coding: utf8

from __future__ import absolute_import, unicode_literals

from kuankr_utils import log, debug, date_time

"""
涨跌幅限制
上海、深圳证券交易所自1996年12月16日起，分别对上市交易的股票（含A、B股）、基金类证券的交易实行价格涨跌幅限制，即在一个交易日内，除首日上市的证券外，上述证券的交易价格相对于上一个交易日收盘价格的涨跌幅度不得超过10%。计算公式为：上一个交易日的收盘价×（1±10%）。计算结果四舍五入至0．01元，超过涨跌幅限制的委托为无效委托，交易所作自动撤单处理。例如：深发展（0001）上一个交易日收盘价为17．81元，则其今日涨跌幅限制为：跌停板17．8×0．9=16．029，四舍五入后为16．03元；涨停板17．81×1．1=19．591，四舍五入后为19．59元；在16．03元－19．59元之间的委托均为有效委托，而低于16．03元和高于19．59元的委托则为无效委托。
自1998年4月起，中国证监会对部分上市公司的股票实行特别处理，即ST，其股票涨跌幅限制为5%。计算公式为：上一个交易日的收盘价×（1±5%），计算方法同上。
另外，对于PT类的股票，其涨幅限制为5%，跌幅则没有限制。
对于两市原有的老基金和各地证交中心挂牌交易的基金经过清理规范后上市的证券投资基金，在其上市首日，涨跌幅限制为其上市时每份基金单位资产净值的30%，即每份基金单位资产净值×（1±30%），次日起涨跌幅限制为前个交易日收盘价的10%。
"""

def hit_limit_price(action, bar, last_close, guess=False):
    if last_close is None or bar is None:
        return False
        
    t0 = date_time.to_datetime('1996-12-16')
    t1 = date_time.to_datetime(bar['time'])
    if t1<t0:
        return False

    eps = 1e-8

    close = bar['close']
    high = bar['high']
    low = bar['low']

    if action=='buy' and close<=last_close or action=='sell' and close>=last_close:
        return False

    limit_pct = 10
    delta = 0.5
    price_eps = max(0.01, 0.002 * last_close)
    limit = (limit_pct-delta)/100.0
    
    rise = close/last_close

    #一字板特判
    if abs(high-low)<=price_eps and abs(rise-1) >= 0.045:
        return True

    #rise
    if close > last_close:
        if abs(high-close)>=price_eps:
            return False
        return rise-1 >= limit
    #fall
    else:
        if abs(low-close)>=price_eps:
            return False
        return 1-rise >= limit


def check_limit_price(direction, price, last_close, time=None, symbol=None, allow_equal=False):
    if time is not None:
        t0 = date_time.to_datetime('1996-12-16')
        if time<t0:
            return True

    eps = 1e-8
    if direction>0:
        limit = last_close * 1.1
        if allow_equal:
            limit += eps
        else:
            limit -= eps
        return price <= limit
    else:
        limit = last_close * 0.9
        if allow_equal:
            limit -= eps
        else:
            limit += eps
        return price >= limit


