#coding: utf8

from kuankr_utils import log, debug
from kuankr_utils.open_struct import DefaultOpenStruct

from .transaction import Transaction

class InvalidOrder(StandardError):
    pass

class Order(DefaultOpenStruct):
    """
    买卖单子
    """
    defaults = {
        'symbol': None,
        'amount': 0,
        'cost': 0,
        'commission': 0,
        'price': None,
        'direction': 1,
        'limit_price': None,
        'time': None
    }

    def get_price(self):
        if 'price' in self:
            return self['price']
        else:
            return self.get('limit_price')

    def transaction_cash(self):
        return self.get_price() * self.amount

    def required_cash(self):
        tc = self.transaction_cash()
        c = self.commission
        return max(tc + c, 0)

    def required_amount(self):
        if self.amount > 0:
            #buy
            return 0
        else:
            #sell
            return -self.amount

    def to_transaction(self):
        t = {
            'symbol': self.get('symbol'),
            'amount': self.get('amount'),
            'price': self.get_price()
        }
        if 'commission' in self:
            t['commission'] = self['commission']
        return Transaction(t)

    def validate(self):
        if self.get_price() is None:
            raise InvalidOrder("price required")
