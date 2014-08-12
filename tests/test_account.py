import pytest

from kuankr_utils import log, debug

from quant_finance.order import Order, InvalidOrder
from quant_finance.lotter import DefaultLotter
from quant_finance.margin import Margin
from quant_finance.account import Account
from quant_finance.portfolio import Portfolio
from quant_finance.commission import Proportional
from quant_finance.transaction import Transaction

def test_simple():
    p = Portfolio(cash=10000)
    m = Margin()
    c = Proportional(0.001)
    l = DefaultLotter(min_lot=100)
    a = Account(portfolio=p, commission=c, margin=m, lotter=l)

    o = Order(symbol='s1', price=100, amount=100)
    with pytest.raises(InvalidOrder) as e:
        a.handle_order(o)

    p.change_cash(1000)
    a.handle_order(o)

    t = o.to_transaction()
    a.handle_transaction(t)

    assert p.total_value()==10990
    assert p.position_value()==10000

    assert p.positions['s1'].cost==10010

    bar = { 'symbol': 's1', 'close': 110}
    p.handle_bar(bar)

    assert p.total_value()==11990

    o['action'] = 'sell'
    o['amount'] = -o['amount']
    o['price'] = 90
    #NOTE: MUST handle_order before handle_transaction
    a.handle_order(o)

    t = o.to_transaction()
    a.handle_transaction(t)
    pos = p.positions['s1']
    assert pos.cost==1019 and pos.reserved==0


