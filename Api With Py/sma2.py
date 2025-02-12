import MetaTrader5 as mt5
import pandas as pd
import time
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Connect to MetaTrader 5
def connect_mt5():
    if not mt5.initialize():
        print("❌ Failed to connect!")
        return False
    print("✅ Successfully connected to MetaTrader 5!")
    return True

# Get historical data (1 minute candles)
def get_data(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M1, num_candles=100):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    if rates is None:
        print("❌ Failed to get data!")
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# Calculate Simple Moving Averages (SMA)
def calculate_sma(data, period):
    return data['close'].rolling(window=period).mean()

# Execute buy order
def place_buy_order(symbol, lot=0.1):
    price = mt5.symbol_info_tick(symbol).ask
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": "Python Buy Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    order = mt5.order_send(request)
    if order.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Failed to place buy order! Error code: {order.retcode}")
    else:
        print(f"✅ Buy order placed successfully! Order ID: {order.order}")

# Execute sell order
def place_sell_order(symbol, lot=0.1):
    price = mt5.symbol_info_tick(symbol).bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": "Python Sell Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    order = mt5.order_send(request)
    if order.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Failed to place sell order! Error code: {order.retcode}")
    else:
        print(f"✅ Sell order placed successfully! Order ID: {order.order}")

# Trading strategy (based on moving averages)
def strategy(symbol="EURUSD"):
    data = get_data(symbol=symbol)
    if data is not None:
        sma_20 = calculate_sma(data, 20)
        sma_50 = calculate_sma(data, 50)
        last_price = data['close'].iloc[-1]

        print(f"SMA_20: {sma_20.iloc[-1]}, SMA_50: {sma_50.iloc[-1]}, Last Price: {last_price}")

        # Check for buy signal (SMA crossover)
        if sma_20.iloc[-1] > sma_50.iloc[-1] and last_price > sma_20.iloc[-1]:
            print("✅ Buy signal detected!")
            place_buy_order(symbol)
        else:
            print("❌ No buy signal.")

        # Check for sell signal (SMA crossover)
        if sma_20.iloc[-1] < sma_50.iloc[-1] and last_price < sma_20.iloc[-1]:
            print("✅ Sell signal detected!")
            place_sell_order(symbol)
        else:
            print("❌ No sell signal.")

# Run the strategy every minute
if __name__ == "__main__":
    if connect_mt5():
        while True:
            strategy(symbol="EURUSD")
            time.sleep(60)  # Wait for the next minute before checking again
        mt5.shutdown()
