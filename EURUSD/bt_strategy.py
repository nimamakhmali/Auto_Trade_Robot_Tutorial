import backtrader as bt
import pandas as pd
from datetime import datetime


# Load data from the CSV file
data = bt.feeds.GenericCSVData(
    dataname='eurusd_m15.csv',  # Path to your CSV file
    fromdate=datetime(2024, 1, 1),  # Start date
    todate=datetime(2025, 1, 1),  # End date
    nullvalue=0.0,
    dtformat=('%Y-%m-%d %H:%M:%S'),  # Adjust based on your CSV file's date format
    timeframe=bt.TimeFrame.Minutes,  # Timeframe is 15 minutes
    compression=15,  # 15-minute data
    historical=True
)

# Create a Cerebro engine
cerebro = bt.Cerebro()
cerebro.adddata(data)  # Add data to the engine

# Set the initial cash for trading
cerebro.broker.set_cash(10000)

# Set the commission (optional)
cerebro.broker.setcommission(commission=0.001)


# Set the position size (optional)
cerebro.addsizer(bt.sizers.FixedSize, stake=10)

# Print starting portfolio value
print(f"Starting Portfolio Value: {cerebro.broker.getvalue()}")

# Run the backtest
cerebro.run()

# Print ending portfolio value
print(f"Ending Portfolio Value: {cerebro.broker.getvalue()}")



class PinBarStrategy(bt.Strategy):
    # Define the indicators
    def __init__(self):
        self.highest = bt.indicators.Highest(self.data.high, period=20)  # Resistance (highest high in last 20 bars)
        self.lowest = bt.indicators.Lowest(self.data.low, period=20)  # Support (lowest low in last 20 bars)

    def next(self):
        # Check for a Pin Bar pattern
        if self.data.close[0] > self.data.open[0]:  # Bullish Pin Bar (close > open)
            if self.data.low[0] <= self.lowest[0]:  # Support level is tested
                if self.data.close[0] > self.data.open[0]:
                    self.buy()  # Buy signal
        elif self.data.close[0] < self.data.open[0]:  # Bearish Pin Bar (close < open)
            if self.data.high[0] >= self.highest[0]:  # Resistance level is tested
                if self.data.close[0] < self.data.open[0]:
                    self.sell()  # Sell signal

# Create a Cerebro engine
cerebro = bt.Cerebro()
cerebro.adddata(data)  # Add data to the engine
cerebro.addstrategy(PinBarStrategy)  # Add the strategy

# Set the initial cash for trading
cerebro.broker.set_cash(10000)

# Set the commission (optional)
cerebro.broker.setcommission(commission=0.001)

# Set the position size (optional)
cerebro.addsizer(bt.sizers.FixedSize, stake=10)

# Print starting portfolio value
print(f"Starting Portfolio Value: {cerebro.broker.getvalue()}")

# Run the backtest
cerebro.run()

# Print ending portfolio value
print(f"Ending Portfolio Value: {cerebro.broker.getvalue()}")
