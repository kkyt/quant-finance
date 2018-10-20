# coding: utf8

class Commission(object):
    def __call__(self, txn):
        return 0

    def calc_avail_cash(self, cash):
        """
        计算在满足交易费用的前提下，最大可用资金。
        例如，如果交易费用为每笔 10 元，当前资金为 10000，那么最大可用资金为 9990。
        """
        return cash

class Proportional(Commission):
    def __init__(self, ratio=0.001):
        self.ratio = ratio

    def __call__(self, txn):
        return abs(txn.transaction_cash() * self.ratio)

    def calc_avail_cash(self, cash):
        return cash / (1 + self.ratio)

class PerShare(Commission):
    def __init__(self, cost=0.03):
        self.cost = float(cost)

    def __call__(self, txn):
        return abs(txn.amount * self.cost)

class PerTrade(Commission):
    def __init__(self, cost=5.0):
        self.cost = float(cost)

    def calculate(self, txn):
        if txn.amount == 0:
            return 0.0
        return self.cost

