#coding: utf8

from kuankr_utils import log, debug


"""
保证金
"""
#TODO: portfolio support

class Margin(object):
    def __call__(self, odr, ptf):
        #TODO: user required_cash and required_amount
        act = odr.action
        amount = odr.amount
        price = odr.get_price()

        cash = ptf.available_cash() - odr.commission
        if cash < 0:
            return False

        if act=='buy':
            return amount <= cash/price

        elif act=='sell':
            return -amount <= ptf.available_amount(odr.symbol)

        else:
            return False

class MarginNoCheck(object):
    def __call__(self, odr, ptf):
        return True
        
class MarginLeverage(object):
    def __init__(self, leverage=1, allow_short=False):
        self.leverage = leverage
        self.allow_short = allow_short

    def max_buy(self, cash, price, pos):
        cash = max(cash, 0)
        return int(cash*self.leverage)/price

    def max_sell(self, cash, price, pos):
        amount = pos.get('amount', 0)
        cash = max(cash, 0)
        if self.allow_short:
            new_cash = amount*price+cash
            return int(new_cash*self.leverage)/price
        else:
            return amount

    def max_amount(self, *args, **kwargs):
        direction = kwargs.pop('direction')
        if direction < 0:
            return -self.max_sell(*args, **kwargs)
        else:
            return self.max_buy(*args, **kwargs)

    def check_amount(self, amount, *args, **kwargs):
        """
        return (is_allowed, max_amount[sell<0, buy>0])
        """
        if amount > 0:
            m = self.max_buy(*args, **kwargs)
            return amount<=m, m
        else:
            m = self.max_sell(*args, **kwargs)
            return -amount<=m, -m

    def is_allowed(self, *args, **kwargs):
        return check_amount(*args, **kwargs)[0]



