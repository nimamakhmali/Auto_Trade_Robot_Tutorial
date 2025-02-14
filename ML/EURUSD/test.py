import MetaTrader5 as mt5
import pandas as pd

# اتصال به MT5
if not mt5.initialize():
    print("oh no")
    quit()

# دریافت داده‌های قیمتی
symbol = "EURUSD"
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 1000)

# تبدیل به DataFrame برای تحلیل راحت‌تر
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')  # تبدیل زمان
print(df.head())

# قطع اتصال از MT5
mt5.shutdown()
