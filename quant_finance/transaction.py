#coding: utf8

from kuankr_utils import log, debug
from kuankr_utils.open_struct import DefaultOpenStruct

class InvalidTransaction(StandardError):
    pass

class Transaction(DefaultOpenStruct):
    """
    交易
    """

    defaults = {
        'action': None,
        'symbol': None,
        'amount': 0,
        'commission': 0,
        'price': None,
        'time': None
    }

    def validate(self):
        if not self.action in ['buy', 'sell', 'change_cash']:
            raise InvalidTransaction('invalid action: %s' % self.action)
        if not self.amount:
            raise InvalidTransaction('invalid amount: %s' % self.amount)

    def cost(self):
        c = float(self.commission)/abs(self.amount)
        return self.price + c

    def transaction_cash(self):
        return self.price * self.amount

    def total_cost(self):
        if self.action=='change_cash':
            return -self.price
        else:
            return self.commission + self.transaction_cash()

    def required_cash(self):
        #TODO: 和 Order.required_cash 一起改成默认计交易费用的模式(在部分成交的情况下比较复杂)
        #执行该交易需要帐户里有多少钱
        #不计交易费用
        tc = self.transaction_cash()
        c = self.commission
        return max(tc + c, 0)

    def required_amount(self):
        #执行该交易需要帐户里有多少券
        #TODO: 做空
        if self.amount > 0:
            #buy
            return 0
        else:
            #sell
            return -self.amount

