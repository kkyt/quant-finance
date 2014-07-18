#coding: utf8

class InvalidOrder(StandardError):
    pass

class Order(dict):
    pass

def required_commission(self, commission):
    txn = self.to_transaction()
    return commission(txn)

def to_transaction(odr):
    return {
        'symbol': odr['symbol'],
        'amount': odr['amount'],
        'price': get_price(odr),
    }

def get_price(odr):
    return odr.get('price') or odr.get('limit_price')

def validate(odr):
    if not 'symbol' in odr:
        raise InvalidOrder("symbol is missing")

    if get_price(odr) is None:
        raise InvalidOrder("price required")

    if not odr.get('amount'):
        raise InvalidOrder("amount is missing or zero")

    return True

