import backtrader as bt


class StopProfitStrategy(bt.Strategy):
    params = (
        ('profit_rate', 0.1),
        ('loss_rate', 5),
        ('order_size', 500),
        ('verbose', True),
    )

    def __init__(self):
        self.orders = []

        self.order = None
        self.stop_order = None
        self.profit_order = None

        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open

        print('PARAMETERS, Profit rate: %f, Loss rate: %f' % (self.p.profit_rate, self.p.loss_rate))

    def log(self, txt, dt=None, verbose=False):
        dt = dt or self.datas[0].datetime.datetime(0)
        if self.params.verbose or verbose:
            print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            pass

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %f, Size: %f, Cost: %f, Comm %f' %
                         (order.executed.price,
                          order.executed.size,
                          order.executed.value,
                          order.executed.comm))

            elif order.issell():
                self.log('SELL EXECUTED, Price: %f, Size: %f, Cost: %f, Comm %f' %
                         (order.executed.price,
                          order.executed.size,
                          order.executed.value,
                          order.executed.comm))

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            pass

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f, Portfolio: %f' %
                 (trade.pnl, trade.pnlcomm, self.broker.getvalue()))

    def next(self):
        if not self.position:
            size = self.p.order_size / self.dataopen[0]
            self.order = self.buy(exectype=bt.Order.Market, size=size, transmit=False)

            profit_price = self.dataopen[0] / (1.0 - (self.p.profit_rate / 100))
            loss_price = self.dataopen[0] * (1.0 - (self.p.loss_rate / 100))

            self.stop_order = self.sell(
                exectype=bt.Order.Stop,
                price=loss_price,
                size=size,
                transmit=False,
                parent=self.order)

            self.profit_order = self.sell(
                exectype=bt.Order.Limit,
                price=profit_price,
                size=size,
                transmit=True,
                parent=self.order)

            self.orders = [self.order.ref, self.stop_order.ref, self.profit_order.ref]

    def stop(self):
        txt = 'PORTFOLIO VALUE, Profit rate: %f, Loss rate: %f, %f' % \
              (self.p.profit_rate, self.p.loss_rate, self.broker.getvalue())
        self.log(txt, verbose=True)
