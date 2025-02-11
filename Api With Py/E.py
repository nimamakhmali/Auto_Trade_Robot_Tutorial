import MetaTrader5 as mt5
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Connect to MetaTrader 5
def connect_mt5():
    if not mt5.initialize():
        print("❌ Failed to connect!")
        return False
    return True

# Close all open positions
def close_all_positions():
    positions = mt5.positions_get()
    if positions is None or len(positions) == 0:
        print("❌ No open positions to close!")
        return

    for pos in positions:
        price = mt5.symbol_info_tick(pos.symbol).bid if pos.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(pos.symbol).ask
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            "position": pos.ticket,  # 🟢 مهم: اضافه کردن position
            "price": price,
            "deviation": 10,
            "magic": 123456,
            "comment": "Closing order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        order = mt5.order_send(request)
        if order.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"❌ Failed to close order {pos.ticket}. Error: {order.retcode}")
        else:
            print(f"✅ Order {pos.ticket} closed successfully!")

# Run
if __name__ == "__main__":
    if connect_mt5():
        close_all_positions()
        mt5.shutdown()
