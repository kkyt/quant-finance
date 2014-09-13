#coding: utf8

from kuankr_utils import log, debug, enum
from kuankr_utils.open_struct import DefaultOpenStruct

from .transaction import Transaction

ORDER_STATUS = enum.Enum(
    'OPEN',
    'FILLED',
    'CANCELLED'
)

class InvalidOrder(StandardError):
    
    def __init__(self, id, message=None):
        if message is None:
            message = id
        self.id = id
        #if not id in ['margin_check_failed','price_required', 'cash_not_enough']:
        super(InvalidOrder, self).__init__(message)

class Order(DefaultOpenStruct):
    """
    买卖单子
    """
    defaults = {
        'action': None,
        'symbol': None,
        'amount': 0,
        'cost': 0,
        'commission': 0,
        'price': None,
        'limit_price': None,
        'time': None,
        'status': ORDER_STATUS.OPEN
    }

    def direction(self):
        if self.action=='buy':
            return 1
        else:
            return -1

    def get_price(self):
        for k in ['price', 'limit_price']:
            if k in self:
                return self[k]

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
            'action': self.get('action'),
            'price': self.get_price()
        }
        if 'commission' in self:
            t['commission'] = self['commission']
        return Transaction(t)

    def validate(self):
        if self.get_price() is None:
            raise InvalidOrder("price_required")

    def remainder(self):
        return self.amount - self.filled

    def cancel(self):
        self.status = ORDER_STATUS.CANCELLED
        
    def is_canceled(self):
        return self.status == ORDER_STATUS.CANCELLED

    def is_open(self):
        if self.status == ORDER_STATUS.CANCELLED:
            return False

        if self.remainder() != 0:
            self.status = ORDER_STATUS.OPEN
        else:
            self.status = ORDER_STATUS.FILLED

        return self.status == ORDER_STATUS.OPEN

    def triggered(self):
        """
        For a market order, True.
        For a stop order, True IFF stop_reached.
        For a limit order, True IFF limit_reached.
        For a stop-limit order, True IFF (stop_reached AND limit_reached)
        """
        if self.get('stop_price') is not None and not self.stop_reached:
            return False

        if self.get('limit_price') is not None and not self.limit_reached:
            return False

        return True

    def check_triggers(self, price):
        """
        Given an order and a trade event, return a tuple of
        (stop_reached, limit_reached).
        For market orders, will return (False, False).
        For stop orders, limit_reached will always be False.
        For limit orders, stop_reached will always be False.

        Orders that have been triggered already (price targets reached),
        the order's current values are returned.
        """
        if self.triggered():
            return True
        
        triggered = False

        if self.get('stop_price') is not None:
            if (self.direction() * (price - self.stop_price) <= 0):
                self.stop_reached = True
                triggered = True

        if self.get('limit_price') is not None:
            if (self.direction() * (price - self.limit_price) <= 0):
                self.limit_reached = True
                triggered = True

        return triggered

    def handle_transaction(self, transaction):
        self.filled += transaction.amount
        self.time = transaction.time
        if abs(self.filled)>abs(self.amount):
            raise Exception("Order.filled>amount: %s" % self)

