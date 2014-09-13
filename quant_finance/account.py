from kuankr_utils import log, debug

from .order import InvalidOrder

class Account(object):
    def __init__(self, portfolio=None, commission=None, margin=None, lotter=None):
        self.portfolio = portfolio
        self.commission = commission
        self.margin = margin
        self.lotter = lotter

    def handle_transaction(self, txn):
        if txn.amount:
            #calc commission only if commission is not provided
            if not 'commission' in txn:
                txn.commission = self.commission(txn)
            self.portfolio.handle_transaction(txn)

    def normalize_order(self, odr):
        p = self.portfolio
        if not 'amount' in odr:
            if odr.direction() > 0:
                price = odr.get_price()
                #TODO: commission
                cash = p.available_cash()
                if 'position' in odr:
                    cash = min(cash, p.total_value() * odr.position)
                odr.amount = cash / price
            else:
                #TODO when current amount < 0?
                m = p.positions.available_amount(odr.symbol)
                if 'position' in odr:
                    m = m * odr.position
                odr.amount = -m
        if not odr.action:
            if odr.amount > 0:
                odr.action = 'buy'
            else:
                odr.action = 'sell'

    def validate_order(self, odr):
        if odr.amount == 0:
            raise InvalidOrder("amount==0")

        odr.commission = self.commission(odr.to_transaction())
        if not self.margin(odr, self.portfolio):
            raise InvalidOrder("margin_check_failed")

    def handle_order(self, odr):
        self.normalize_order(odr)
        self.lotter(odr)

        self.validate_order(odr)
        odr.validate()

        self.portfolio.handle_order(odr)
        return odr

    def handle_data(self, data):
        if 'bars' in data:
            bars = data['bars']
        else:
            bars = [data]
        for bar in bars:
            self.handle_bar(bar)

    def handle_bar(self, bar):
        self.portfolio.handle_bar(bar)

