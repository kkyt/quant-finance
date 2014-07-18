from kuankr_utils import log, debug

from quant_finance import order, transaction, position

class Account(object):
    def __init__(self, portfolio=None, commission=None, margin=None, lotter=None):
        self.portfolio = portfolio
        self.commission = commission
        self.margin = margin
        self.lotter = lotter

    def handle_transaction(self, txn):
        if txn.get('amount'):
            #calc commission only if commission is not provided
            if not 'commission' in txn:
                txn['commission'] = self.commission(txn)
            self.portfolio.handle_transaction(txn)

    def normalize_order(self, odr):
        p = self.portfolio
        if not 'amount' in odr:
            if odr['direction'] > 0:
                price = order.get_price(odr)
                #TODO: commission
                odr['amount'] = p.available_cash() / price
            else:
                #TODO when current amount < 0?
                odr['amount'] = -positions.available_amount(odr['symbol'])

    def validate_order(self, odr):
        odr['commission'] = order.required_commission(odr, self.commission)
        if not self.margin.check(odr, self.portfolio):
            raise order.InvalidOrder("margin check failed")

    def handle_order(self, odr):
        self.normalize_order(odr)
        self.validate_order(odr)

        odr = self.lotter(odr)
        order.validate(odr)

        self.portfolio.handle_order(odr)
        return odr

