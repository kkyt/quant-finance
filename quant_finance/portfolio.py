#coding: utf8

from kuankr_utils import log, debug

from quant_finance import positions, order, transaction

class Portfolio(object):
    def __init__(self, cash=0.0, additional_cash=0.0, overdraw=0.0):
        """
        additional_cash: 
            用于当cash为负时用于随时补充资金的金额,None表示缺多少补多少, 
            例如在导入历史交易时, 并不知道初始资金多少,
            这时,将 additional_cash设为None表示缺多少补多少
            见 Portfolio.change_cash

        overdraw:
            允许透支的金额, 和 additional_cash不同的时,透支的钱是要还的
            None表示可无限透支

        TODO
            透支的利息计算
        """

        self.max_invest = cash

        self.cash = cash
        #提交订单后,有部分钱会被冻结
        self.reserved_cash = 0.0

        self.starting_cash = cash
        self.additional_cash = additional_cash

        self.overdraw = overdraw

        # symbol => position object
        self.positions = positions.Positions()

        self.cash_flow = 0.0

        self.max_cash_flow = 0.0

    def available_cash(self):
        #TODO: additional_cash?
        return self.cash - self.reserved_cash

    def available_amount(self, symbol):
        p = self.positions.get(symbol)
        if p is None:
            return 0
        else:
            position.available_amount(p)

    def position_amount(self, symbol, default=None):
        p = self.positions.get(symbol)
        if p is None:
            return default
        else:
            return p['amount']

    def performance(self):
        return {
            'market_value': self.market_value(),
            'paper_profit': self.paper_profit(),
            'profit': self.profit(),
            'returns': self.returns()
        }

    def position_value(self):
        return self.positions.market_value()

    def market_value(self):
        return self.cash + self.position_value()

    def paper_profit(self):
        return self.positions.profit()

    def profit(self):
        return self.market_value() - self.max_invest

    def returns(self):
        return self.market_value()/self.max_invest-1.0

    def change_cash(self, d):
        self.cash += d

        #先用 additional_cash 补齐
        if self.cash < 0:
            ac = self.additional_cash
            if ac is None:
                m = -self.cash
                self.cash = 0
                self.max_invest += m
            else:
                m = min(ac, -self.cash)
                self.cash += m
                self.max_invest += m
                self.additional_cash -= m
                
        #再检查 overdraw 透支额度
        if self.cash < -self.overdraw:
            raise Exception('Portfolio.cash %s < overdraw %s after recharge from additional_cash' %\
                self.cash, self.overdraw)

        self.cash_flow += d
        if abs(self.cash_flow) > self.max_cash_flow:
            self.max_cash_flow = self.cash_flow

    def handle_ticks(self, event):
        for tick in event['ticks']:
            s = tick['symbol']
            p = tick['close']
            if s in self.positions and p is not None:
                self.positions[s].price = p
                self.positions[s].time = tick['time']

    def handle_transaction(self, txn):
        self.positions.handle_transaction(txn)
        self.reserved_cash -= txn.required_cash()
        cost = txn.total_cost()
        self.change_cash(-cost)

    def handle_dividend(self, div):
        cash_flow = self.positions.handle_dividend(div)
        self.change_cash(cash_flow)
   
    def handle_order(self, order):
        self.validate_order(order)
        self.positions.handle_order(order)
        cash = order.required_cash()
        self.reserved_cash += cash

    def validate_order(self, order):
        if order.symbol is None:
            return InvalidOrder("symbol is missing")

        cash = order.required_cash()
        if cash > self.available_cash():
            raise InvalidOrder('not enough cash: %s < %s' % (self.available_cash, cash))

    def commission(self):
        return positions.commission(self.positions)

