import datetime
import backtrader as bt
from strategies.stop_profit import StopProfitStrategy


exchange = 'binance'
pair = 'BTC/USDT'
start_date = datetime.datetime.utcnow() - datetime.timedelta(days=10)
stop_date = datetime.datetime.utcnow() - datetime.timedelta(hours=1)

cash = 1000
commission = -0.0005

if __name__ == '__main__':
    data = bt.feeds.CCXT(
        exchange=exchange,
        symbol=pair,
        timeframe=bt.TimeFrame.Minutes,
        fromdate=start_date,
        todate=stop_date,
        compression=1
    )

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(StopProfitStrategy, profit_rate=0.1, loss_rate=0.1, order_size=1000)

    # Add data
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(cash)

    # Set commission of exchange
    cerebro.broker.setcommission(commission=commission)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Draw a graph
    cerebro.plot()
