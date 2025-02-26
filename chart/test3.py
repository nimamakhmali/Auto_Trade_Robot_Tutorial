import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import os
import backtrader as bt
import matplotlib.pyplot as plt

# Initialize connection to MetaTrader 5
if not mt5.initialize():
    print("Failed to connect to MetaTrader 5")
    mt5.shutdown()

# Set parameters for getting EUR/USD data in M15 timeframe
symbol = "EURUSD"  # Changed to EUR/USD
timeframe = mt5.TIMEFRAME_M15
bars = 1000  # Number of bars (you can change this)
utc_from = datetime(2024, 1, 1)  # Start date
utc_to = datetime(2025, 1, 1)  # End date

# Get data
rates = mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)

# Check if data is empty
if len(rates) == 0:
    print("No data received. Please check your parameters or connection.")
else:
    # Convert data to DataFrame
    data = pd.DataFrame(rates)

    # Print first few rows to check structure
    print("Data received:")
    print(data.head())  # This will show the first few rows of the data

    # If the time column has a different name, adjust here
    data['time'] = pd.to_datetime(data['time'], unit='s')  # or data['datetime'] depending on the output

    # Set time as index
    data.set_index('time', inplace=True)

    # Automatically create the CSV file in the current directory
    csv_file_path = os.path.join(os.getcwd(), 'eurusd_m15.csv')
    data.to_csv(csv_file_path)

    # Print success message
    print(f"Data successfully saved to {csv_file_path}")

# Close connection to MetaTrader 5
mt5.shutdown()

# Create a Backtrader DataFeed from the DataFrame
class PandasData(bt.feeds.PandasData):
    params = (
        ('datetime', 'time'),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'volume'),
        ('openinterest', None)
    )

# Create a strategy to plot RSI
class PinBarStrategy(bt.Strategy):
    # Define the indicators
    def __init__(self):
        self.highest = bt.indicators.Highest(self.data.high, period=20)  # Resistance (highest high in last 20 bars)
        self.lowest = bt.indicators.Lowest(self.data.low, period=20)  # Support (lowest low in last 20 bars)
        self.rsi = bt.indicators.RelativeStrengthIndex(period=14)  # RSI Indicator

    def next(self):
        # Print RSI value for the current bar
        print(f"RSI: {self.rsi[0]}")

        # Check for a Pin Bar pattern
        if self.data.close[0] > self.data.open[0]:  # Bullish Pin Bar (close > open)
            if self.data.low[0] <= self.lowest[0]:  # Support level is tested
                self.buy()  # Buy signal
        elif self.data.close[0] < self.data.open[0]:  # Bearish Pin Bar (close < open)
            if self.data.high[0] >= self.highest[0]:  # Resistance level is tested
                self.sell()  # Sell signal

# Create a Cerebro engine
cerebro = bt.Cerebro()

# Add data to the engine
data_feed = PandasData(dataname=data)
cerebro.adddata(data_feed)  # Add data to the engine
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

# Plot the results including RSI
cerebro.plot(style='candlestick')
