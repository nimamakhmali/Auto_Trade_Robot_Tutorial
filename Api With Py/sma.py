import MetaTrader5 as mt5
import pandas as pd
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')




# Connect to MetaTrader 5
def connect_mt5():
    if not mt5.initialize():
        print("❌ Failed to connect!")
        return False
    print("✅ Connected to MetaTrader 5!")
    return True

# Fetch historical data
def get_data(symbol, timeframe, bars=500):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    if rates is None:
        print(f"❌ Failed to get market data for {symbol}")
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert time to readable format
    return df

# Calculate SMAs
def calculate_sma(df, short_period=50, long_period=200):
    df['SMA_50'] = df['close'].rolling(window=short_period).mean()
    df['SMA_200'] = df['close'].rolling(window=long_period).mean()
    return df

# Check trading conditions
def check_trade_signal(df):
    if df['SMA_50'].iloc[-2] < df['SMA_200'].iloc[-2] and df['SMA_50'].iloc[-1] > df['SMA_200'].iloc[-1]:
        return "BUY"  # Golden Cross (Buy Signal)
    elif df['SMA_50'].iloc[-2] > df['SMA_200'].iloc[-2] and df['SMA_50'].iloc[-1] < df['SMA_200'].iloc[-1]:
        return "SELL"  # Death Cross (Sell Signal)
    return None

# Get open positions
def get_open_positions(symbol):
    positions = mt5.positions_get(symbol=symbol)
    return positions if positions else []

# Close opposite trades
def close_opposite_trade(symbol, trade_type):
    positions = get_open_positions(symbol)
    for pos in positions:
        if (trade_type == "BUY" and pos.type == mt5.ORDER_TYPE_SELL) or (trade_type == "SELL" and pos.type == mt5.ORDER_TYPE_BUY):
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": pos.volume,
                "type": mt5.ORDER_TYPE_BUY if pos.type == mt5.ORDER_TYPE_SELL else mt5.ORDER_TYPE_SELL,
                "position": pos.ticket,
                "price": mt5.symbol_info_tick(symbol).bid if pos.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask,
                "deviation": 10,
                "magic": 123456,
                "comment": "Closing opposite order",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            order = mt5.order_send(request)
            if order.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"❌ Failed to close {pos.ticket}. Error: {order.retcode}")
            else:
                print(f"✅ Closed order {pos.ticket}")

# Open new trade
def open_trade(symbol, trade_type, volume=0.1):
    price = mt5.symbol_info_tick(symbol).ask if trade_type == "BUY" else mt5.symbol_info_tick(symbol).bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY if trade_type == "BUY" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": f"Python {trade_type} Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    order = mt5.order_send(request)
    if order.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Failed to open {trade_type} order. Error: {order.retcode}")
    else:
        print(f"✅ {trade_type} order placed successfully!")

# Main trading loop
def run_trading_bot(symbol="EURUSD", timeframe=mt5.TIMEFRAME_H1):
    if not connect_mt5():
        return

    while True:
        df = get_data(symbol, timeframe)
        if df is not None:
            df = calculate_sma(df)
            trade_signal = check_trade_signal(df)
            if trade_signal:
                close_opposite_trade(symbol, trade_signal)
                open_trade(symbol, trade_signal)
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    run_trading_bot()
