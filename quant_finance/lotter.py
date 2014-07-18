class Lotter(object):
    def __call__(self, order):
        return order


class DefaultLotter(Lotter):
    def __init__(self, min_lot=100):
        self.min_lot = min_lot

    def __call__(self, amount):
        if amount>0:
            #buy at a minimum lot
            return int(amount)/self.min_lot * self.min_lot
        else:
            #sell no restriction
            return int(amount)

