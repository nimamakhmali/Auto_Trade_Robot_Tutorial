import pandas as pd

# مسیر فایل CSV
file_path = file_path = "C:/Users/TickNovin/Desktop/market_data.csv"


# خواندن داده‌ها از فایل CSV
df = pd.read_csv(file_path, names=["Bid", "Ask", "Timestamp"])

# نمایش اطلاعات
print(df)
