import backtrader as bt
from datetime import datetime

# خواندن فایل CSV
data_feed = bt.feeds.GenericCSVData(
    dataname="AAPL.csv",       # آدرس فایل CSV خود را وارد کن
    dtformat="%Y-%m-%d",       # فرمت تاریخ (مطمئن شو که تاریخ‌ها مطابق این فرمت باشند)
    timeframe=bt.TimeFrame.Days,  # انتخاب تایم فریم (در اینجا روزانه)
    compression=1,              # تنظیم این مقدار برای هر داده روزانه
    openinterest=-1,            # چون فایل CSV شما ممکنه ستون openinterest نداشته باشه
    header=1                   # نادیده گرفتن ردیف سرآیند (عنوان ستون‌ها)
)

# تعریف استراتژی ساده
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt}: {txt}")

    def __init__(self):
        # میانگین متحرک ساده با دوره 10
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=10)

    def next(self):
        # اگر قیمت بسته شدن از میانگین متحرک بیشتر بود خرید می‌کنیم
        if self.data.close[0] > self.sma[0]:
            self.log(f"Buy Signal: Close {self.data.close[0]} > SMA {self.sma[0]}")
        # اگر قیمت بسته شدن از میانگین متحرک کمتر بود فروش می‌کنیم
        elif self.data.close[0] < self.sma[0]:
            self.log(f"Sell Signal: Close {self.data.close[0]} < SMA {self.sma[0]}")

# تنظیمات cerebro
cerebro = bt.Cerebro()
cerebro.addstrategy(TestStrategy)
cerebro.adddata(data_feed)  # اضافه کردن داده‌ها
cerebro.run()
cerebro.plot()  # نمایش نمودار
