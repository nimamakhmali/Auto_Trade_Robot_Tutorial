import pandas as pd
import numpy as np
from data_fetcher import DataFetcher  # استفاده از ماژول دریافت داده

class MarketAnalyzer:
    def __init__(self, data):
        self.data = data
    
    def calculate_sma(self, window):
        """محاسبه میانگین متحرک ساده (SMA)"""
        return self.data['close'].rolling(window=window).mean()

    def calculate_ema(self, window):
        """محاسبه میانگین متحرک نمایی (EMA)"""
        return self.data['close'].ewm(span=window, adjust=False).mean()

    def calculate_rsi(self, period=14):
        """محاسبه شاخص قدرت نسبی (RSI)"""
        delta = self.data['close'].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        avg_gain = pd.Series(gain).rolling(window=period).mean()
        avg_loss = pd.Series(loss).rolling(window=period).mean()

        rs = avg_gain / (avg_loss + 1e-10)  # جلوگیری از تقسیم بر صفر
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def add_indicators(self):
        """اضافه کردن اندیکاتورها به دیتافریم"""
        self.data['SMA_10'] = self.calculate_sma(10)
        self.data['SMA_50'] = self.calculate_sma(50)
        self.data['EMA_10'] = self.calculate_ema(10)
        self.data['EMA_50'] = self.calculate_ema(50)
        self.data['RSI'] = self.calculate_rsi(14)
        
        return self.data

    def generate_signals(self):
        """تولید سیگنال خرید و فروش بر اساس کراس میانگین متحرک"""
        self.data['Signal'] = 0  # مقدار پیش‌فرض: بدون سیگنال
        self.data.loc[self.data['SMA_10'] > self.data['SMA_50'], 'Signal'] = 1  # خرید
        self.data.loc[self.data['SMA_10'] < self.data['SMA_50'], 'Signal'] = -1  # فروش
        
        return self.data
  
    def save_to_csv(self, filename):
        """ذخیره داده‌ها به فایل CSV"""
        self.data.to_csv(filename, index=False)

# **مثال استفاده**
if __name__ == "__main__":
    fetcher = DataFetcher()
    data = fetcher.get_data()
    fetcher.close_connection()

    analyzer = MarketAnalyzer(data)
    data_with_indicators = analyzer.add_indicators()
    data_with_signals = analyzer.generate_signals()

    # ذخیره داده‌ها به فایل CSV
    analyzer.save_to_csv('market_data_with_signals.csv')

    print(data_with_signals[['time', 'close', 'SMA_10', 'SMA_50', 'EMA_10', 'EMA_50', 'RSI', 'Signal']].tail(10))  # نمایش ۱۰ کندل آخر
