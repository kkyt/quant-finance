

class Matcher(object):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.match(*args, **kwargs)

    # return transactions
    def match(self, *args, **kwargs):
        raise NotImplementedError()


class ExchangeMatcher(Matcher):
    def match(self, orders, exchange):
        return exchange.match(orders)

class EventMatcher(Matcher):
    def __init__(self, slippage):
        self.slippage = slippage

    def match(self, orders, event):
        return self.slippage(orders, event)


