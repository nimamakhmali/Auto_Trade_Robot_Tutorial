from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
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

# جدا کردن ویژگی‌ها و برچسب‌ها
X = df.drop(columns=['target'])  # ویژگی‌ها
y = df['target']  # برچسب‌ها

# تقسیم داده‌ها به آموزش و آزمون (80% آموزش، 20% آزمون)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ساخت مدل KNN با 3 همسایه
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)  # آموزش مدل

# پیش‌بینی بر روی داده‌های تست
y_pred = knn.predict(X_test)

# محاسبه دقت مدل
accuracy = accuracy_score(y_test, y_pred)
print(f"دقت مدل: {accuracy:.2f}")
