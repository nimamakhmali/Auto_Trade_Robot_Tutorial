
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

# Get data for the specified symbol and timeframe
def get_data(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M1, num_candles=200):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    if rates is None or len(rates) == 0:
        print("❌ Failed to get data!")
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# Calculate moving averages and generate signals
def calculate_signals(df):
    df['SMA5'] = df['close'].rolling(window=5).mean()  # 5-period Simple Moving Average
    df['SMA20'] = df['close'].rolling(window=20).mean()  # 20-period Simple Moving Average
    df['Signal'] = 0  # Initialize the signal column with 0

    # Generate buy signal when SMA5 crosses above SMA20
    df['Signal'][df['SMA5'] > df['SMA20']] = 1

    # Generate sell signal when SMA5 crosses below SMA20
    df['Signal'][df['SMA5'] < df['SMA20']] = -1

    return df

# Place a buy order
def place_buy_order(symbol, lot=0.1):
    price = mt5.symbol_info_tick(symbol).ask
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 0.0002,  # Stop Loss
        "tp": price + 0.0004,  # Take Profit
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

# Place a sell order
def place_sell_order(symbol, lot=0.1):
    price = mt5.symbol_info_tick(symbol).bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price + 0.0002,  # Stop Loss
        "tp": price - 0.0004,  # Take Profit
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

# Main trading logic
def run_trading():
    symbol = "EURUSD"  # Symbol for trading
    data = get_data(symbol)
    
    if data is not None:
        data = calculate_signals(data)
        
        # Get the last signal
        last_signal = data['Signal'].iloc[-1]
        
        # Check if a buy or sell signal is generated
        if last_signal == 1:
            print("🔹 Buy signal detected!")
            place_buy_order(symbol)
        elif last_signal == -1:
            print("🔹 Sell signal detected!")
            place_sell_order(symbol)

# Run the trading bot
if __name__ == "__main__":
    if connect_mt5():
        while True:
            run_trading()
            time.sleep(60)  # Wait for the next minute
        mt5.shutdown()




