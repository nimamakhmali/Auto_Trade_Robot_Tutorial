import MetaTrader5 as mt5
import pandas as pd
import talib

# Connect to MT5
if not mt5.initialize():
    print("Failed to connect to MT5")
    quit()

# Fetch historical data
symbol = "EURUSD"
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 1000)

# Convert to DataFrame
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')

# Calculate indicators
df['SMA_50'] = talib.SMA(df['close'], timeperiod=50)  # Simple Moving Average
df['RSI_14'] = talib.RSI(df['close'], timeperiod=14)  # RSI
df['MACD'], df['MACD_signal'], _ = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)  # MACD

# Print first rows
print(df[['time', 'close', 'SMA_50', 'RSI_14', 'MACD']].head())

# Shutdown MT5
mt5.shutdown()
