import backtrader as bt
import datetime


class SMAStrategy(bt.Strategy):
    params = (
        ("sma_short", 50),
        ("sma_long", 200),
        ("macd_fast", 12),
        ("macd_slow", 26),
        ("macd_signal", 9),
    )

    def __init__(self):
        self.sma_short = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_short)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_long)
        self.macd = bt.indicators.MACD(self.data.close, 
                                       period_me1=self.params.macd_fast, 
                                       period_me2=self.params.macd_slow, 
                                       period_signal=self.params.macd_signal)

    def next(self):
        if self.sma_short > self.sma_long:
            if self.macd.macd > self.macd.signal:
                if not self.position:
                    self.buy()
        elif self.sma_short < self.sma_long:
            if self.macd.macd < self.macd.signal:
                if self.position:
                    self.sell()

# تنظیم داده‌ها
data = bt.feeds.YahooFinanceData(dataname='AAPL.csv', fromdate=datetime.datetime(2023, 1, 1), todate=datetime.datetime(202, 1, 1))

cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
# استراتژی دوم: خرید و فروش بر اساس RSI
class RSIStrategy(bt.Strategy):
    # تعریف پارامترها
    params = (
        ('rsi_period', 14),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30)
    )

    def __init__(self):
        # ایجاد RSI
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)

    def next(self):
        # شرایط خرید
        if self.rsi < self.params.rsi_oversold:
            if not self.position:
                self.buy()
        # شرایط فروش
        elif self.rsi > self.params.rsi_overbought:
            if self.position:
                self.sell()

# استراتژی سوم: خرید و فروش بر اساس MACD
class MACDStrategy(bt.Strategy):
    # تعریف پارامترها
    params = (
        ('macd_fast', 12),
        ('macd_slow', 26),
        ('macd_signal', 9)
    )

    def __init__(self):
        # ایجاد MACD
        self.macd = bt.indicators.MACD(self.data.close, 
                                period_me1=self.params.macd_fast, 
                                period_me2=self.params.macd_slow, 
                                period_signal=self.params.macd_signal)

    def next(self):
        # شرایط خرید
        if self.macd > self.macd.signal:
            if not self.position:
                self.buy()
        # شرایط فروش
        elif self.macd < self.macd.signal:
            if self.position:
                self.sell()

# تنظیمات cerebro
cerebro = bt.Cerebro()

# اضافه کردن استراتژی‌ها
cerebro.addstrategy(SMAStrategy)
cerebro.addstrategy(RSIStrategy)
cerebro.addstrategy(MACDStrategy)

# بارگذاری داده‌های تاریخی (مثال استفاده از داده‌های CSV)
data = bt.feeds.YahooFinanceData(dataname='AAPL.csv', fromdate=datetime.datetime(2015, 1, 1),
                                 todate=datetime.datetime(2020, 1, 1))

# اضافه کردن داده به cerebro
cerebro.adddata(data)

# تنظیم سرمایه اولیه
cerebro.broker.set_cash(10000)

# تنظیم هزینه‌ها
cerebro.broker.setcommission(commission=0.001)

# نمایش مقدار سرمایه قبل از شروع
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# اجرای استراتژی‌ها
cerebro.run()

# نمایش مقدار سرمایه بعد از پایان
print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

# نمایش نمودار
cerebro.plot()
