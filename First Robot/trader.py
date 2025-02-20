import MetaTrader5 as mt5

def open_trade(symbol, volume, trade_type):
    price = mt5.symbol_info_tick(symbol).ask if trade_type == "buy" else mt5.symbol_info_tick(symbol).bid
    sl = price - 20 * 0.0001 if trade_type == "buy" else price + 20 * 0.0001
    tp = price + 40 * 0.0001 if trade_type == "buy" else price - 40 * 0.0001

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY if trade_type == "buy" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "magic": 123456,
        "comment": "Price Action Trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    return result
