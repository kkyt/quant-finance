from quant_finance import transaction

class Commission(object):
    def __call__(self, txn):
        return 0

class Proportional(Commission):
    def __init__(self, ratio=0.001):
        self.ratio = ratio

    def __call__(self, txn):
        return abs(txn.transaction_cash() * self.ratio)

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

