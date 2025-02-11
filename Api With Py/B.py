import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Connect to MetaTrader 5
def connect_mt5():
    if not mt5.initialize():
        print("❌ Failed to connect!")
        return False
    return True

# Get OHLC data
def get_ohlc(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M5, num_candles=100):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    if rates is None:
        print("❌ Failed to get data!")
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# Plot candlestick chart
def plot_candlestick(data):
    if data is not None:
        mpf.plot(data, type="candle", style="charles", volume=False, title="Candlestick Chart")

# Run
if __name__ == "__main__":
    if connect_mt5():
        data = get_ohlc("EURUSD", mt5.TIMEFRAME_M15, 50)
        plot_candlestick(data)
        mt5.shutdown()
