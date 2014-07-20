
class Performance(object):
    def __call__(self, portfolio):
        pass

class MaxInvest(Performance):
    def __call__(self, p):
        return p.max_invest()

class Returns(Performance):
    def __call__(self, p):
        return p.returns()

class TotalValue(Performance):
    def __call__(self, p):
        return p.total_value()
