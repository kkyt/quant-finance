#coding: utf8

from kuankr_utils import log, debug
from kuankr_utils.open_struct import DefaultOpenStruct

from .position import Position

class Positions(DefaultOpenStruct):
    def cleanup(self):
        for x,p in self.items():
            if p.is_closed():
                del self[x]
        
    def market_value(self):
        s = 0
        for p in self.values():
            s += p.market_value() or 0.0
        return s

    def paper_profit(self):
        s = 0
        for p in self.values():
            s += p.paper_profit() or 0.0
        return s

    def commission(self):
        s = 0
        for p in self.values():
            s += p.commission
        return s

    def available_amount(self, symbol):
        p = self.get(symbol)
        if p is None:
            return 0
        else:
            return p.available_amount()

    def open_positions(self):
        return [p for p in self.values() if not p.is_closed()]

    def is_closed(self):
        for p in self.values():
            if not p.is_closed():
                return False
        return True

    def ensure(self, symbol, **kwargs):
        if not symbol in self:
            self[symbol] = Position(symbol=symbol, **kwargs)
        return self[symbol]
            
    def handle_transaction(self, txn):
        #NOTE: MUST handle_order before handle_transaction
        p = self[txn.symbol]
        return p.handle_transaction(txn)

    def handle_order(self, odr):
        p = self.ensure(odr.symbol, time=odr.time)
        return p.handle_order(odr)

    def handle_dividend(self, div):
        p = self[div.symbol]
        return p.handle_dividend(div)

    def handle_bar(self, bar):
        p = self.get(bar['symbol'])
        if p is not None:
            p.handle_bar(bar)

