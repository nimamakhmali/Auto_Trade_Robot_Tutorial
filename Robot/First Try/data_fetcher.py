import MetaTrader5 as mt5
import pandas as pd

class DataFetcher:
    def __init__(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_H1, num_bars=200):
        self.symbol = symbol
        self.timeframe = timeframe
        self.num_bars = num_bars
        
        # اتصال به MT5
        if not mt5.initialize():
            raise Exception("Failed to connect to MetaTrader 5")
    
    def get_data(self):
        """دریافت داده‌های قیمت و تبدیل به DataFrame"""
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, self.num_bars)
        if rates is None:
            raise Exception("Failed to retrieve data from MT5")
        
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')  # تبدیل زمان به فرمت خوانا
        return df

    def close_connection(self):
        """بستن اتصال به MT5"""
        mt5.shutdown()

# **مثال استفاده**
if __name__ == "__main__":
    fetcher = DataFetcher()
    data = fetcher.get_data()
    print(data.head())  # نمایش ۵ کندل اول
    fetcher.close_connection()
