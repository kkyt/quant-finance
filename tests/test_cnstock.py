#coding:utf8

from quant_finance.cnstock.name import *
from quant_finance.cnstock.symbol import *
from quant_finance.cnstock.index import *

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

def test_index():
    cases = [ 
        ('1A0001', 'SH000001'), 
        ('1B0001', 'SH000004'),
        ('SZ399001', 'SZ399001'),
        #('399001', 'SZ399001')
    ]
    for old, new in cases:
        assert index_symbol_old_to_new(old)==new
        assert index_symbol_new_to_old(new)==old


