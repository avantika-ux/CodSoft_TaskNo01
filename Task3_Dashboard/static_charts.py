"""
Task 3: Data Visualization Dashboard (Part 1 - Static Charts)
----------------------------------------------------------------
- Create meaningful visualizations using Matplotlib and Seaborn.
- Design bar charts, line charts, pie charts, histograms, and scatter plots.
- Customize charts with titles, labels, legends, and color schemes.
- Present insights through clear, easy-to-understand visualizations.

Input: ecommerce_orders_cleaned.csv (from Task 1)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.autolayout"] = True
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.titleweight"] = "bold"

df = pd.read_csv("ecommerce_orders_cleaned.csv", parse_dates=["OrderDate"])

# ---------------------------------------------------------
# 1. Bar chart - Revenue by category
# ---------------------------------------------------------
category_revenue = df.groupby("Category")["TotalAmount"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(x=category_revenue.index, y=category_revenue.values, hue=category_revenue.index,
            palette="crest", legend=False)
plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=30)
plt.savefig("chart1_bar_revenue_by_category.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# 2. Line chart - Revenue trend over time
# ---------------------------------------------------------
daily_revenue = df.groupby(df["OrderDate"].dt.date)["TotalAmount"].sum().sort_index()

plt.figure(figsize=(9, 5))
plt.plot(daily_revenue.index, daily_revenue.values, marker="o", color="#2A6F97", linewidth=2,
         label="Daily Revenue")
plt.title("Revenue Trend Over Time")
plt.xlabel("Order Date")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=45)
plt.legend()
plt.savefig("chart2_line_revenue_trend.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# 3. Pie chart - Payment mode share
# ---------------------------------------------------------
payment_counts = df["PaymentMode"].value_counts()

plt.figure(figsize=(6, 6))
colors = sns.color_palette("crest", len(payment_counts))
plt.pie(payment_counts.values, labels=payment_counts.index, autopct="%1.0f%%",
        colors=colors, startangle=90, wedgeprops={"edgecolor": "white"})
plt.title("Payment Mode Share")
plt.savefig("chart3_pie_payment_mode.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# 4. Histogram - Distribution of order value
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))
sns.histplot(df["TotalAmount"], bins=15, color="#3E7CB1", edgecolor="white", kde=True)
plt.title("Distribution of Order Value")
plt.xlabel("Order Value (INR)")
plt.ylabel("Number of Orders")
plt.savefig("chart4_histogram_order_value.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# 5. Scatter plot - Quantity vs Total Amount, colored by category
# ---------------------------------------------------------
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="Quantity", y="TotalAmount", hue="Category", palette="crest", s=90)
plt.title("Quantity vs Order Value by Category")
plt.xlabel("Quantity")
plt.ylabel("Order Value (INR)")
plt.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.savefig("chart5_scatter_quantity_vs_value.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# 6. Bar chart - Orders by city
# ---------------------------------------------------------
city_orders = df["City"].value_counts()

plt.figure(figsize=(8, 5))
sns.barplot(x=city_orders.index, y=city_orders.values, hue=city_orders.index,
            palette="mako", legend=False)
plt.title("Number of Orders by City")
plt.xlabel("City")
plt.ylabel("Order Count")
plt.xticks(rotation=30)
plt.savefig("chart6_bar_orders_by_city.png", dpi=150)
plt.close()

print("Saved 6 static charts (bar x2, line, pie, histogram, scatter).")
