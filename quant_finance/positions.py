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

    def profit(self):
        s = 0
        for p in self.values():
            s += p.profit() or 0.0
        return s

    def commission(self):
        s = 0
        for p in self.values():
            s += p.commission
        return s

    def open_positions(self):
        return [p for p in self.values() if not p.is_closed()]

    def handle_transaction(self, txn):
        p = self[txn.symbol]
        return p.handle_transaction(txn)

    def handle_order(self, odr):
        if not odr.symbol in self:
            self[odr.symbol] = Position(symbol=odr.symbol, time=odr.time)
        p = self[odr.symbol]
        return p.handle_order(odr)

    def handle_dividend(self, div):
        p = self[div.symbol]
        return p.handle_dividend(div)

