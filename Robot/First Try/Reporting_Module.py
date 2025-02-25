import MetaTrader5 as mt5
import pandas as pd

class TradeReporter:
    def __init__(self, magic_number=234000, filename="trade_report.csv"):
        self.magic_number = magic_number
        self.filename = filename
        self.connection = self.connect_to_mt5()

    def connect_to_mt5(self):
        """اتصال به متاتریدر ۵"""
        if not mt5.initialize():
            print("Failed to initialize MetaTrader 5")
            return None
        else:
            print("MetaTrader 5 Initialized successfully")
            return True

    def close_connection(self):
        """بستن اتصال به متاتریدر ۵"""
        mt5.shutdown()

    def fetch_trades(self):
        """دریافت تاریخچه معاملات بسته‌شده و معاملات باز"""
        trade_data = []

        # دریافت تاریخچه معاملات بسته‌شده
        from datetime import datetime, timedelta
        end_time = datetime.now()
        start_time = end_time - timedelta(days=30)  # دریافت تاریخچه ۳۰ روز گذشته

        history = mt5.history_deals_get(start_time, end_time)
        
        if history is None or len(history) == 0:
            print("No trade history found.")
        else:
            for deal in history:
                if deal.magic == self.magic_number:  # فیلتر کردن معاملات ربات
                    trade_data.append({
                        "Ticket": deal.ticket,
                        "Time": pd.to_datetime(deal.time, unit='s'),
                        "Symbol": deal.symbol,
                        "Type": "Buy" if deal.type == mt5.ORDER_TYPE_BUY else "Sell",
                        "Volume": deal.volume,
                        "Price": deal.price,
                        "Profit": deal.profit
                    })

        # دریافت معاملات باز
        positions = mt5.positions_get()
        if positions is not None:
            for position in positions:
                if position.magic == self.magic_number:
                    trade_data.append({
                        "Ticket": position.ticket,
                        "Time": pd.to_datetime(position.time, unit='s'),
                        "Symbol": position.symbol,
                        "Type": "Buy" if position.type == mt5.ORDER_TYPE_BUY else "Sell",
                        "Volume": position.volume,
                        "Price": position.price,
                        "Profit": position.profit
                    })

        if len(trade_data) == 0:
            print("No trades related to this bot.")
            return None

        df = pd.DataFrame(trade_data)
        return df

    def save_to_csv(self):
        """ذخیره تاریخچه معاملات در فایل CSV"""
        df = self.fetch_trades()
        if df is not None:
            df.to_csv(self.filename, index=False)
            print(f"Trade report saved to {self.filename}")
        else:
            print("No trades to save.")

    def show_report(self):
        """نمایش خلاصه گزارش معاملات"""
        df = self.fetch_trades()
        if df is not None:
            print("Recent Trades:")
            print(df.tail(10))  # نمایش ۱۰ معامله آخر
        else:
            print("No trades to report.")

# **مثال استفاده**
if __name__ == "__main__":
    reporter = TradeReporter()
    
    # نمایش گزارش
    reporter.show_report()
    
    # ذخیره در فایل CSV
    reporter.save_to_csv()

    # بستن اتصال به متاتریدر ۵
    reporter.close_connection()
