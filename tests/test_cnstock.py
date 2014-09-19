#coding:utf8

from quant_finance.markets.cn.name import *
from quant_finance.markets.cn.symbol import *

def test_name():
    assert normalize_name('ＡＢ c')=='ABC'
    assert normalize_name('万科 Ｂ')=='万科B'

def test_symbol():
    assert not is_symbol(1)
    assert not is_symbol('sh600')
    assert is_symbol('SH600000')
    assert not is_symbol('Sh600000')
    assert is_symbol(normalize_symbol('Sh600000'))
    #assert name_to_symbol('pfyh')=='SH600000'



