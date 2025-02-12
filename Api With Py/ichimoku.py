import MetaTrader5 as mt5
import pandas as pd
import time
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# Connect to MetaTrader 5
def connect_mt5():
    if not mt5.initialize():
        print("❌ Failed to connect to MetaTrader 5!")
        return False
    print("✅ Connected to MetaTrader 5!")
    return True

# Get candlestick data
def get_data(symbol="USDCHF", timeframe=mt5.TIMEFRAME_M1, num_candles=200):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    if rates is None or len(rates) == 0:
        print("❌ Failed to get candlestick data!")
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# Calculate Ichimoku Indicator
def calculate_ichimoku(df):
    df['tenkan_sen'] = (df['high'].rolling(window=9).max() + df['low'].rolling(window=9).min()) / 2
    df['kijun_sen'] = (df['high'].rolling(window=26).max() + df['low'].rolling(window=26).min()) / 2
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)
    df['senkou_span_b'] = ((df['high'].rolling(window=52).max() + df['low'].rolling(window=52).min()) / 2).shift(26)
    df['chikou_span'] = df['close'].shift(-26)
    return df

# Detect Buy/Sell Signals
def detect_signals(df):
    latest = df.iloc[-1]
    previous = df.iloc[-2]

    buy_signal = (
        latest['close'] > latest['senkou_span_a'] and latest['close'] > latest['senkou_span_b'] and
        previous['tenkan_sen'] < previous['kijun_sen'] and latest['tenkan_sen'] > latest['kijun_sen'] and
        latest['chikou_span'] > latest['close']
    )

    sell_signal = (
        latest['close'] < latest['senkou_span_a'] and latest['close'] < latest['senkou_span_b'] and
        previous['tenkan_sen'] > previous['kijun_sen'] and latest['tenkan_sen'] < latest['kijun_sen'] and
        latest['chikou_span'] < latest['close']
    )

    if buy_signal:
        return "BUY"
    elif sell_signal:
        return "SELL"
    else:
        return None

# Place a Buy Order
def place_buy_order(symbol, lot=0.1):
    price = mt5.symbol_info_tick(symbol).ask
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 0.0003,  # Stop Loss
        "tp": price + 0.0006,  # Take Profit
        "deviation": 10,
        "magic": 123456,
        "comment": "Ichimoku Buy Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    order = mt5.order_send(request)
    if order.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Buy order failed! Error: {order.retcode}")
    else:
        print(f"✅ Buy order executed! Order ID: {order.order}")

# Place a Sell Order
def place_sell_order(symbol, lot=0.1):
    price = mt5.symbol_info_tick(symbol).bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price + 0.0003,  # Stop Loss
        "tp": price - 0.0006,  # Take Profit
        "deviation": 10,
        "magic": 123456,
        "comment": "Ichimoku Sell Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    order = mt5.order_send(request)
    if order.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Sell order failed! Error: {order.retcode}")
    else:
        print(f"✅ Sell order executed! Order ID: {order.order}")

# Run the trading bot
def run_trading():
    symbol = "USDCHF"  
    data = get_data(symbol)
    
    if data is not None:
        data = calculate_ichimoku(data)
        signal = detect_signals(data)
        
        if signal == "BUY":
            print("🔹 Buy signal detected!")
            place_buy_order(symbol)
        elif signal == "SELL":
            print("🔹 Sell signal detected!")
            place_sell_order(symbol)
        else:
            print("🔸 No signals detected.")

# Execute the bot every 1 minute
if __name__ == "__main__":
    if connect_mt5():
        while True:
            run_trading()
            time.sleep(60)  # Wait for the next candlestick
        mt5.shutdown()
