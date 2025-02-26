import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize connection to MetaTrader 5
if not mt5.initialize():
    print("Failed to connect to MetaTrader 5")
    mt5.shutdown()

# Set parameters for getting EUR/USD data in M15 timeframe
symbol = "EURUSD"  # Symbol for EUR/USD
timeframe = mt5.TIMEFRAME_M15  # Timeframe for 15 minute candles
bars = 1000  # Number of bars (can be changed)
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

    # Convert timestamp to datetime
    data['time'] = pd.to_datetime(data['time'], unit='s')

    # Set time as index
    data.set_index('time', inplace=True)

    # Print first few rows to check
    print(data.head())

    # Plot the closing price
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['close'], label='Close Price', color='blue')
    plt.title(f'{symbol} Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.grid(True)
    plt.legend()
    plt.show()

# Close connection to MetaTrader 5
mt5.shutdown()
