import MetaTrader5 as mt5
import pandas as pd

class OrderExecutor:
    def __init__(self, symbol="EURUSD", lot_size=0.1, slippage=100):
        self.symbol = symbol
        self.lot_size = lot_size
        self.slippage = slippage
        self.connection = self.connect_to_mt5()

    def connect_to_mt5(self):
        """اتصال به متاتریدر ۵"""
        if not mt5.initialize():
            print("Fail to initialize MetaTrader 5")
            return None
        else:
            print("MetaTrader 5 Initialized successfully")
            return True

    def close_connection(self):
        """بستن اتصال به متاتریدر ۵"""
        mt5.shutdown()

    def open_buy_order(self):
        """ارسال سفارش خرید"""
        price = mt5.symbol_info_tick(self.symbol).ask
        deviation = self.slippage
        order = mt5.ORDER_TYPE_BUY
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot_size,
            "type": order,
            "price": price,
            "slippage": deviation,
            "magic": 234000,
            "comment": "Buy order",
            "type_filling": mt5.ORDER_FILLING_IOC,
            "type_time": mt5.ORDER_TIME_GTC
        }
        result = mt5.order_send(request)
        print(result)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Buy order failed:", result.comment)
        else:
            print(f"Buy order executed successfully at {price}")

    def open_sell_order(self):
        """ارسال سفارش فروش"""
        price = mt5.symbol_info_tick(self.symbol).bid
        deviation = self.slippage
        order = mt5.ORDER_TYPE_SELL
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot_size,
            "type": order,
            "price": price,
            "slippage": deviation,
            "magic": 234000,
            "comment": "Sell order",
            "type_filling": mt5.ORDER_FILLING_IOC,
            "type_time": mt5.ORDER_TIME_GTC
        }
        result = mt5.order_send(request)
        print(result)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Sell order failed:", result.comment)
        else:
            print(f"Sell order executed successfully at {price}")

    def execute_trade(self, signal):
        """اجرای سفارش خرید یا فروش بر اساس سیگنال"""
        if signal == 1:  # سیگنال خرید
            self.open_buy_order()
        elif signal == -1:  # سیگنال فروش
            self.open_sell_order()
        else:
            print("No trade signal generated")

    def execute_trades_from_csv(self, csv_filename):
        """خواندن سیگنال‌ها از فایل CSV و اجرای سفارش‌ها"""
        data = pd.read_csv(csv_filename)  # خواندن فایل CSV
        for index, row in data.iterrows():
            signal = row['Signal']
            self.execute_trade(signal)  # اجرای معامله بر اساس سیگنال

# **مثال استفاده**
if __name__ == "__main__":
    # اتصال به متاتریدر ۵
    executor = OrderExecutor()
    
    # خواندن سیگنال‌ها از فایل CSV و اجرای معامله‌ها
    executor.execute_trades_from_csv('market_data_with_signals.csv')
    
    # بستن اتصال به متاتریدر ۵
    executor.close_connection()
