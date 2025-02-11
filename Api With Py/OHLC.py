import MetaTrader5 as mt5
import pandas as pd
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 🟢 Connect to MetaTrader 5
def connect_mt5():
    if not mt5.initialize():
        print("❌ Failed to connect to MetaTrader 5!")
        print(mt5.last_error())
        return False
    print("✅ Successfully connected to MetaTrader 5!")
    return True

# 🟢 Get OHLC data
def get_data(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M5, num_candles=100):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    if rates is None:
        print("❌ Failed to retrieve data!")
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# 🟢 Place a buy order
def place_buy_order(symbol, lot=0.1, stop_loss=50, take_profit=100):
    price = mt5.symbol_info_tick(symbol).ask
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - stop_loss * 0.0001,
        "tp": price + take_profit * 0.0001,
        "deviation": 10,
        "magic": 123456,
        "comment": "Python Buy Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    order = mt5.order_send(request)
    if order.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Buy order failed! Error code: {order.retcode}")
    else:
        print(f"✅ Buy order placed successfully! Order ID: {order.order}")

# 🟢 Place a sell order
def place_sell_order(symbol, lot=0.1, stop_loss=50, take_profit=100):
    price = mt5.symbol_info_tick(symbol).bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": price + stop_loss * 0.0001,
        "tp": price - take_profit * 0.0001,
        "deviation": 10,
        "magic": 123456,
        "comment": "Python Sell Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    order = mt5.order_send(request)
    if order.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Sell order failed! Error code: {order.retcode}")
    else:
        print(f"✅ Sell order placed successfully! Order ID: {order.order}")

# 🟢 Main execution
if __name__ == "__main__":
    if connect_mt5():
        symbol = "EURUSD"
        data = get_data(symbol=symbol)
        if data is not None:
            print(data.tail(5))  # Display the last 5 candles
        # Place a test buy order
        place_buy_order(symbol)
        time.sleep(2)  # Wait a bit
        # Place a test sell order
        place_sell_order(symbol)
        mt5.shutdown()
