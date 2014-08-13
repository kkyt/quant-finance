#coding: utf8

from kuankr_utils import log, debug
from kuankr_utils.open_struct import DefaultOpenStruct

class InvalidPosition(StandardError):
    pass

class Position(DefaultOpenStruct):
    """
    部位(仓位)
    """

    defaults = {
        'symbol': None,
        'amount': 0,
        'cost': 0,
        'history_cost': 0,
        'reserved': 0,
        'commission': 0,
        'price': None,
        'time': None
    }

    def is_closed(self):
        return abs(self.amount) < 1e-8

    def validate(self):
        res = self.reserved
        if res < 0 or res > self.amount:
            raise InvalidPosition('invalid reserved')
                
    def available_amount(self):
        return self.amount - self.reserved

    '''
    def cost_basis(self):
        #cost per share
        m = self.amount
        if not m:
            return None
        else:
            return self.cost / m
    '''

    def market_value(self):
        p = self.price
        if p is None:
            return None
        else:
            return p * self.amount

    def paper_profit(self):
        mv = self.market_value()
        if mv is None:
            return None
        else:
            return mv - self.cost

    def _validate_action(self, act):
        if(self.symbol != act.symbol):
            raise Exception('symbol not match')

        amount = act.required_amount()
        if amount > self.available_amount():
            raise Exception('not enough position amount: %s %s' % (self, act))

    def handle_order(self, odr):
        self._validate_action(odr)

        self.reserved += odr.required_amount()

    def handle_transaction(self, txn):
        #don't validate_action for transaction

        self.amount += txn.amount
        self.commission += txn.commission
        c = txn.total_cost()
        self.cost += c
        self.history_cost += c
        self.reserved -= txn.required_amount()
        self.price = txn.price

        #we're covering a short or closing a position
        if(self.amount == 0):
            self.cost = 0

