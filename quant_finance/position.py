#coding: utf8

from kuankr_utils import log, debug

from quant_finance import order

class InvalidPosition(StandardError):
    pass

class Position(dict):
    """
    部位(仓位)
        symbol
        amount
        cost
        reserved
        commission
        price
        time
    """
    pass

def validate(pos):
    for f in ['symbol', 'amount']:
        if not f in pos:
            raise InvalidPosition('%s missing' % f)

    if 'reserved' in pos:
        res = pos['reserved']
        if res < 0 or res > pos['amount']:
            raise InvalidPosition('invalid reserved')
            
def available_amount(pos):
    return pos['amount'] - pos.get('reserved', 0)

def is_closed(pos):
    return abs(pos['amount']) < 1e-8

def cost_basis(pos):
    #cost per share
    if not pos['amount']:
        return None
    else:
        return pos['cost'] / pos['amount']

def market_value(pos):
    p = pos.get('price')
    a = pos.get('amount')
    if p is None or a is None:
        return None
    else:
        return p * a

def profit(pos):
    mv = pos.market_value()
    if mv is None:
        return None
    else:
        return mv - pos.cost

def validate_action(pos, act):
    if(pos['symbol'] != act['symbol']):
        raise Exception('symbol not match')

def handle_order(pos, odr):
    validate_action(pos, odr)

    amount = order.required_amount(odr)
    if amount > available_amount(pos):
        raise Exception('not enough position amount: %s %s' % (pos, odr))

    pos['reserved'] = pos.get('reserved', 0) + amount

def handle_transaction(pos, txn):
    validate_action(pos, txn)

    amount = transaction.required_amount(txn)
    if amount > pos.available_amount():
        raise Exception('not enough position amount: %s %s' % (pos, txn))

    pos['amount'] = pos.get('amount', 0) + txn['amount']

    if 'commission' in pos:
        pos['commission'] += txn.get('commission', 0)

    if 'cost' in pos:
        pos['cost'] += transaction.total_cost(txn)

    if 'reserved' in pos:
        pos['reserved'] -= amount

    #TODO:?
    #we're covering a short or closing a position
    #if(pos.amount + txn.amount == 0):
    #    pos.cost = 0.0

