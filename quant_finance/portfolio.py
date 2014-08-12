#coding: utf8

from kuankr_utils import log, debug

from .transaction import Transaction
from .positions import Positions
from .order import Order, InvalidOrder

class Portfolio(object):
    def __init__(self, cash=0.0):
        self.starting_cash = cash
        self.cash = cash
        #提交订单后,有部分钱会被冻结
        self.reserved_cash = 0.0

        # symbol => position object
        self.positions = Positions()

    def available_cash(self):
        return self.cash - self.reserved_cash

    def available_amount(self, symbol):
        p = self.positions.get(symbol)
        if p is None:
            return 0
        else:
            return p.available_amount()

    def position_amount(self, symbol, default=None):
        p = self.positions.get(symbol)
        if p is None:
            return default
        else:
            return p['amount']

    def max_invest(self):
        return self.starting_cash

    def position_value(self):
        return self.positions.market_value()

    def total_value(self):
        return self.cash + self.position_value()

    def paper_profit(self):
        return self.positions.paper_profit()

    #TODO
    """
    def profit(self):
        return self.total_value() - self.max_invest()
    """

    def returns(self):
        return self.total_value() / self.max_invest() - 1.0

    def change_cash(self, d):
        self.cash += d

    def handle_bar(self, bar):
        s = bar['symbol']
        p = bar['close']
        if p is not None and s in self.positions:
            self.positions[s].price = p
            self.positions[s].time = bar.get('time')

    def handle_transaction(self, txn):
        self.positions.handle_transaction(txn)
        self.reserved_cash -= txn.required_cash()
        cost = txn.total_cost()
        self.change_cash(-cost)

    def handle_dividend(self, div):
        cash_flow = self.positions.handle_dividend(div)
        self.change_cash(cash_flow)
   
    #TODO: cancel order
    def handle_order(self, order):
        self.validate_order(order)
        self.positions.handle_order(order)
        cash = order.required_cash()
        self.reserved_cash += cash

    def validate_order(self, order):
        #validate cash and amount using margin
        """
        cash = order.required_cash()
        if cash > self.available_cash():
            raise InvalidOrder('not_enough_cash')
        """
        return True

    def commission(self):
        return self.positions.commission()

