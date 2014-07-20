import pytest

from kuankr_utils import log, debug

from quant_finance.portfolio import Portfolio
from quant_finance.order import Order
from quant_finance.transaction import Transaction

def test_simple():
    p = Portfolio(cash=1000)

    o = Order(symbol='s1', amount=10, limit_price=1)
    p.handle_order(o)
    assert p.reserved_cash==10 and p.cash==1000 and p.positions['s1'].reserved==0

    t = Transaction(symbol='s1', amount=10, price=1)
    p.handle_transaction(t)
    assert p.reserved_cash==0 and p.cash==990 and p.positions['s1'].reserved==0

    o = Order(symbol='s1', amount=-5, limit_price=1)
    p.handle_order(o)
    assert p.reserved_cash==0 and p.cash==990 and p.positions['s1'].reserved==5

    t = Transaction(symbol='s1', amount=-5, price=1)
    p.handle_transaction(t)
    assert p.reserved_cash==0 and p.cash==995 and p.positions['s1'].reserved==0 and p.positions['s1'].amount==5

    t = Transaction(symbol='s2', amount=-5, price=1)
    with pytest.raises(Exception) as e:
        p.handle_transaction(t)

    o = Order(symbol='s2', amount=-5, price=1)
    with pytest.raises(Exception) as e:
        p.handle_order(t)

    o = Order(symbol='s2', amount=5, price=0.1)
    p.handle_order(o)

    with pytest.raises(Exception) as e:
        o = Order(symbol='s2', amount=50, price=1000)
        p.handle_order(o)

    print p


