import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets

# بارگذاری دیتاست iris
iris = datasets.load_iris()

# تبدیل به DataFrame برای بررسی راحت‌تر
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['target'] = iris.target  # افزودن برچسب‌های دسته‌بندی

# نمایش 5 سطر اول داده‌ها
print(df.head())

# رسم یک نمودار ساده برای بررسی توزیع داده‌ها
sns.pairplot(df, hue="target", diag_kind="kde")
plt.show()
