#TODO

from quant_finance import position, order, transaction

class Positions(dict):
    pass

def cleanup(pos):
    for x,p in pos.items():
        if position.is_closed(p):
            del pos[x]
    
def market_value(pos):
    s = 0
    for p in pos.values():
        s += position.market_value(p) or 0.0
    return s

def profit(pos):
    s = 0
    for p in pos.values():
        s += position.profit(p) or 0.0
    return s

def commission(pos):
    s = 0
    for p in pos.values():
        s += p.get('commission', 0)
    return s

def available_amount(pos):
    return pos['amount'] - pos.get('reserved', 0)

def open_positions(pos):
    return [p for p in pos.values() if not position.is_closed(p)]

def handle_transaction(pos, txn):
    p = pos[txn['symbol']]
    return position.handle_transaction(p, txn)

def handle_order(pos, odr):
    p = pos[odr['symbol']]
    return position.handle_order(p, odr)

def handle_dividend(pos, div):
    p = pos[div['symbol']]
    return position.handle_dividend(p, div)

