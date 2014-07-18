#coding: utf8

class InvalidTransaction(StandardError):
    pass

class Transaction(dict):
    pass

def validate(txn):
    for f in ['action', 'symbol']:
        if not f in txn:
            raise InvalidTransaction("%s is missing" % f)

def cost(txn):
    c = txn.get('commission', 0)
    per_share = c * 1.0 / abs(txn['amount'])
    return txn['price'] + per_share

def transaction_cash(txn):
    return txn['price'] * txn['amount']

def total_cost(txn):
    if txn.get('action')=='change_cash':
        return -txn['price']
    else:
        return txn.get('commission',0) + transaction_cash(txn)

def required_cash_with_commission(txn):
    #执行该交易需要帐户里有多少钱
    #计交易费用
    tc = transaction_cash(txn)
    c = txn.get('commission', 0)
    #tc 可能 < 0
    return max(tc + c, 0)

def required_cash(txn):
    #TODO: 和 Order.required_cash 一起改成默认计交易费用的模式(在部分成交的情况下比较复杂)
    #执行该交易需要帐户里有多少钱
    #不计交易费用
    tc = transaction_cash(txn)
    return max(tc, 0)

def required_amount(txn):
    #执行该交易需要帐户里有多少券
    #TODO: 做空
    if txn['amount'] > 0:
        #buy
        return 0
    else:
        #sell
        return -txn['amount']

