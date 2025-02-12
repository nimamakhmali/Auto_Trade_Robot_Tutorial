import MetaTrader5 as mt5
import sys
sys.stdout.reconfigure(encoding='utf-8')

def connect_mt5():
    if not mt5.initialize():
        print("❌ Failed to connect to MetaTrader 5!")
        return False
    print("✅ Successfully connected to MetaTrader 5!")
    return True

def open_trade(symbol="EURUSD", lot=0.1, order_type="buy"):
    if not connect_mt5():
        return
    
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"❌ Failed to get price for {symbol}!")
        mt5.shutdown()
        return

    if order_type.lower() == "buy":
        trade_type = mt5.ORDER_TYPE_BUY
        price = tick.ask
    elif order_type.lower() == "sell":
        trade_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
    else:
        print("❌ Invalid order type!")
        mt5.shutdown()
        return

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": "Python Trade Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,  # Changed to FOK
        "sl": 0.0,  # Removed SL for testing
        "tp": 0.0   # Removed TP for testing
    }

    print("🔹 Trade Request:", request)
    order = mt5.order_send(request)
    print("🔹 Order Response:", order)

    if order.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Trade failed! Error code: {order.retcode}")
    else:
        print(f"✅ Trade opened successfully! Order ID: {order.order}")

    mt5.shutdown()

if __name__ == "__main__":
    open_trade(symbol="EURUSD", lot=0.1, order_type="buy")
