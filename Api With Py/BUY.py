import MetaTrader5 as mt5
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Connect to MetaTrader 5
def connect_mt5():
    if not mt5.initialize():
        print("❌ Failed to connect!")
        return False
    return True

# Place Buy Order
def place_buy_order(symbol="GBPUSD", lot=0.1, stop_loss=50, take_profit=100):
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

# Run
if __name__ == "__main__":
    if connect_mt5():
        place_buy_order("GBPUSD")
        mt5.shutdown()
