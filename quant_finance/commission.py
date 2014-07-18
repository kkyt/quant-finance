from quant_finance import transaction

class Commission(object):
    def __call__(self, txn):
        return 0

class Proportional(Commission):
    def __init__(self, ratio=0.001):
        self.ratio = ratio

    def __call__(self, txn):
        return abs(transaction.transaction_cash(txn) * self.ratio)

class PerShare(Commission):
    """
    Calculates a commission for a txn based on a per
    share cost.
    """
    def __init__(self, cost=0.03):
        """
        Cost parameter is the cost of a trade per-share. $0.03
        means three cents per share, which is a very conservative
        (quite high) for per share costs.
        """
        self.cost = float(cost)

    def __call__(self, txn):
        return abs(txn['amount'] * self.cost)


class PerTrade(Commission):
    """
    Calculates a commission for a txn based on a per
    trade cost.
    """
    def __init__(self, cost=5.0):
        """
        Cost parameter is the cost of a trade, regardless of
        share count. $5.00 per trade is fairly typical of
        discount brokers.
        """
        self.cost = float(cost)

    def calculate(self, txn):
        if txn['amount'] == 0:
            return 0.0
        return self.cost

