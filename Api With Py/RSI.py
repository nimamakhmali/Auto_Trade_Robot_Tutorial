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
def get_data(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M1, num_candles=200):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    if rates is None or len(rates) == 0:
        print("❌ Failed to get candlestick data!")
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# Calculate RSI Indicator
def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()

    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    return df

# Detect Buy/Sell Signals
def detect_signals(df, rsi_overbought=70, rsi_oversold=30):
    latest = df.iloc[-1]
    previous = df.iloc[-2]

    buy_signal = (previous['rsi'] < rsi_oversold) and (latest['rsi'] > rsi_oversold)
    sell_signal = (previous['rsi'] > rsi_overbought) and (latest['rsi'] < rsi_overbought)

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
        "comment": "RSI Buy Order",
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
        "comment": "RSI Sell Order",
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
    symbol = "EURUSD"  
    data = get_data(symbol)
    
    if data is not None:
        data = calculate_rsi(data)
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
