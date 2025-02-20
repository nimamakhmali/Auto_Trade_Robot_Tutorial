import yfinance as yf
import backtrader as bt
from datetime import datetime

                                                                                # دریافت داده‌های تاریخی از Yahoo Finance با yfinance
ticker = "AAPL"
data = yf.download(ticker, start="2023-01-01", end="2024-01-01")

                                                                                  # ذخیره داده‌ها در فایل CSV
csv_file = f"{ticker}.csv"
data.to_csv(csv_file)

                                                                          # حالا فایل CSV را در Backtrader استفاده می‌کنیم
data_feed = bt.feeds.GenericCSVData(
    dataname=csv_file,
    dtformat="%Y-%m-%d",
    timeframe=bt.TimeFrame.Days,
    compression=1,
    openinterest=-1
)

                                                                          # تعریف یک استراتژی ساده
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt}: {txt}")

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(period=10)

    def next(self):
        self.log(f"Close: {self.data.close[0]}")

                                                                                    # اجرای استراتژی
cerebro = bt.Cerebro()
cerebro.addstrategy(TestStrategy)
cerebro.adddata(data_feed)
cerebro.run()
cerebro.plot()
