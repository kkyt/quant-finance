
#TODO

def handle_dividend(pos, dividend):
    """
    先分红再送股
    """
    log.info("Position.handle_dividend: %s" % dividend)
    pos.validate_action(dividend)
    dm = 0
    cash_flow = 0.0
    time = pos.time

    if dividend.mghl:
        div = dividend.mghl * pos.amount * (1.0 - DIVIDEND_TAX)
        log.debug("dividend for %s at %s[%s] cash %s" % (pos.symbol, pos.amount, time, div))
        cash_flow += div
        pos.cost -= div
        
    if dividend.mgsg:
        dm = int_floor(pos.amount * dividend.mgsg)
        log.debug("dividend for %s at %s[%s] stock %s" % (pos.symbol, pos.amount, time, dm))

    if dividend.mgpg:
        dm = int_floor(pos.amount * dividend.mgpg)
        log.debug("dividend for %s at %s[%s] peigu %s" % (pos.symbol, pos.amount, time, dm))
        dc = dividend.pgjg * dm
        cash_flow -= dc
        pos.cost += dc

    pos.amount += dm
    return cash_flow

DIVIDEND_TAX = 0.1
