import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import os
import backtrader as bt

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
