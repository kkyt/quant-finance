from kuankr_utils import log, debug, floats

from .transaction import Transaction

#NOTE: price field is changed to close

class Slippage(object):
    def simulate(self, orders, event, **kwargs):
        raise NotImplementedError()

    def __call__(self, orders, event, **kwargs):
        return self.simulate(orders, event, **kwargs)


class VolumeShareSlippage(Slippage):

    def __init__(self, volume_limit=.25, price_impact=0.1):

        self.volume_limit = volume_limit
        self.price_impact = price_impact

    def simulate(self, orders, event):

        simulated_impact = 0.0
        max_volume = int(self.volume_limit * event['volume'])
        total_volume = 0

        txns = []
        for order in orders:

            open_amount = order.amount - order.filled

            if floats.rel_eq(open_amount, 0):
                continue

            order.check_triggers(event['close'])
            if not order.triggered():
                continue

            # price impact accounts for the total volume of transactions
            # created against the current minute bar
            remaining_volume = max_volume - total_volume
            if (
                remaining_volume <= 0
                or
                floats.rel_eq(remaining_volume, 0)
            ):
                # we can't fill any more transactions
                return txns

            # the current order amount will be the min of the
            # volume available in the bar or the open amount.
            d = order.direction()
            cur_amount = min(remaining_volume, abs(open_amount))
            cur_amount = cur_amount * d
            # tally the current amount into our total amount ordered.
            # total amount will be used to calculate price impact
            total_volume = total_volume + d * cur_amount

            volume_share = min(d * (total_volume) / event['volume'],
                               self.volume_limit)

            simulated_impact = (volume_share) ** 2 \
                * self.price_impact * d * event['close']

            if d * cur_amount > 0:
                txn = Transaction(
                    symbol=order.symbol, 
                    amount=cur_amount,
                    time=event['time'],
                    price=event['close'] + simulated_impact,
                    order_id=order.id,
                    portfolio_id=order.portfolio_id
                )
                order.time = event['time']
                txns.append(txn)

        return txns


class FixedSlippage(Slippage):

    def __init__(self, spread=0.0):
        """
        Use the fixed slippage model, which will just add/subtract
        a specified spread spread/2 will be added on buys and subtracted
        on sells per share
        """
        self.spread = spread

    def simulate(self, orders, event):

        txns = []
        for order in orders:
            # TODO: what if we have 2 orders, one for 100 shares long,
            # and one for 100 shares short
            # such as in a hedging scenario?

            order.check_triggers(event['close'])
            if not order.triggered():
                continue

            remainder = order.remainder()
            if floats.rel_eq(remainder, 0):
                continue

            #NOTE: volume is None means unlimited volume
            if 'volume' in event:
                #transaction.amount = min(order.remainder, event.volume)
                remainder = min(remainder, event['volume'])

            #allow event has no time field
            txn = Transaction(
                symbol=order['symbol'], 
                amount=remainder,
                time=event.get('time'),
                price=event['close'] + (self.spread / 2.0 * order.direction()),
                order_id=order['id'],
            )

            # mark the date of the order to match the transaction
            order['time'] = event.get('time')
            txns.append(txn)
        return txns


