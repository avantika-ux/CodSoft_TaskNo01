"""
Task 2 - Exploratory Data Analysis (EDA)
InAmigos Foundation Internship

Dataset: ecommerce_orders_cleaned.csv

This script:
1. Loads the dataset and examines features using descriptive statistics
2. Identifies trends, distributions, and relationships between variables
3. Detects outliers and unusual patterns
4. Uses summary statistics to answer key business questions
5. Saves charts used in the accompanying report (README.md)
"""

import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

# ---------------------------------------------------------
# 1. Load data and basic overview
# ---------------------------------------------------------
df = pd.read_csv('ecommerce_orders_cleaned.csv')

print("Shape:", df.shape)
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n", df.isnull().sum())
print("\nDescriptive statistics (numeric):\n", df.describe())
print("\nDescriptive statistics (categorical):\n", df.describe(include='object'))

# ---------------------------------------------------------
# 2. Trends, distributions, relationships
# ---------------------------------------------------------
category_summary = (
    df.groupby('Category')
      .agg(orders=('OrderID', 'count'),
           revenue=('TotalAmount', 'sum'),
           avg_order_value=('TotalAmount', 'mean'))
      .sort_values('revenue', ascending=False)
)
print("\nRevenue by category:\n", category_summary)

city_summary = (
    df.groupby('City')
      .agg(orders=('OrderID', 'count'), revenue=('TotalAmount', 'sum'))
      .sort_values('revenue', ascending=False)
)
print("\nRevenue by city:\n", city_summary)

payment_summary = df.groupby('PaymentMode')['TotalAmount'].agg(['count', 'mean'])
print("\nPayment mode summary:\n", payment_summary)

date_summary = (
    df.groupby('OrderDate')
      .agg(orders=('OrderID', 'count'), revenue=('TotalAmount', 'sum'))
)
print("\nRevenue trend by date:\n", date_summary)

customer_summary = (
    df.groupby('CustomerName')
      .agg(orders=('OrderID', 'count'), spend=('TotalAmount', 'sum'))
      .sort_values('spend', ascending=False)
)
print("\nTop customers by spend:\n", customer_summary)

correlation = df[['Quantity', 'Price', 'TotalAmount']].corr()
print("\nCorrelation matrix:\n", correlation)

# ---------------------------------------------------------
# 3. Outlier detection (IQR method on TotalAmount)
# ---------------------------------------------------------
q1 = df['TotalAmount'].quantile(0.25)
q3 = df['TotalAmount'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = df[(df['TotalAmount'] < lower_bound) | (df['TotalAmount'] > upper_bound)]
print(f"\nIQR bounds: ({lower_bound:.2f}, {upper_bound:.2f})")
print("Outlier orders:\n", outliers[['OrderID', 'CustomerName', 'Category', 'Quantity', 'Price', 'TotalAmount']])

# ---------------------------------------------------------
# 4. Data quality check
# ---------------------------------------------------------
unknown_category_count = (df['Category'] == 'Unknown').sum()
print(f"\nOrders with 'Unknown' category: {unknown_category_count} "
      f"({unknown_category_count / len(df):.0%} of all orders)")

mismatch = df[abs(df['Quantity'] * df['Price'] - df['TotalAmount']) > 0.01]
print(f"Rows where Quantity x Price != TotalAmount: {len(mismatch)}")

# ---------------------------------------------------------
# 5. Charts
# ---------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid')

# Revenue by category
fig, ax = plt.subplots(figsize=(8, 5))
category_summary['revenue'].plot(kind='bar', ax=ax, color='#2c7fb8')
ax.set_title('Revenue by Category')
ax.set_ylabel('Revenue (INR)')
ax.set_xlabel('Category')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('charts/revenue_by_category.png', dpi=150)
plt.close()

# Revenue trend by date
fig, ax = plt.subplots(figsize=(7, 5))
date_summary['revenue'].plot(kind='line', marker='o', ax=ax, color='#e34a33')
ax.set_title('Revenue Trend by Order Date')
ax.set_ylabel('Revenue (INR)')
ax.set_xlabel('Order Date')
plt.tight_layout()
plt.savefig('charts/revenue_trend.png', dpi=150)
plt.close()

# Distribution of order value
fig, ax = plt.subplots(figsize=(7, 5))
df['TotalAmount'].plot(kind='hist', bins=10, ax=ax, color='#31a354', edgecolor='white')
ax.set_title('Distribution of Order Value')
ax.set_xlabel('Total Amount (INR)')
plt.tight_layout()
plt.savefig('charts/order_value_distribution.png', dpi=150)
plt.close()

# Revenue by city
fig, ax = plt.subplots(figsize=(7, 5))
city_summary['revenue'].plot(kind='bar', ax=ax, color='#756bb1')
ax.set_title('Revenue by City')
ax.set_ylabel('Revenue (INR)')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('charts/revenue_by_city.png', dpi=150)
plt.close()

print("\nCharts saved to /charts")
print("EDA complete.")
