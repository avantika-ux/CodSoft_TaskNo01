"""
Task 4: Customer Data Analysis
----------------------------------
- Analyze customer information to understand purchasing behavior.
- Segment customers based on age, location, or buying patterns.
- Identify the most valuable customer groups.
- Create visual reports to summarize customer insights.
- Bonus: Suggest marketing strategies based on the analysis.

Input: ecommerce_orders_with_age.csv (Task 1's cleaned data + a CustomerAge field,
added here since customer age wasn't captured in the original dataset)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.autolayout"] = True

df = pd.read_csv("ecommerce_orders_with_age.csv", parse_dates=["OrderDate"])

# ---------------------------------------------------------
# 1. Build a customer-level summary (one row per customer)
# ---------------------------------------------------------
customer_summary = df.groupby("CustomerName").agg(
    Age=("CustomerAge", "first"),
    City=("City", lambda x: x.mode()[0]),
    TotalOrders=("OrderID", "count"),
    TotalSpend=("TotalAmount", "sum"),
    AvgOrderValue=("TotalAmount", "mean"),
).reset_index().sort_values("TotalSpend", ascending=False)

# Favorite category, excluding "Unknown" (missing-data placeholder from Task 1) where possible
def favorite_known_category(sub_df):
    known = sub_df[sub_df["Category"] != "Unknown"]["Category"]
    if len(known) > 0:
        return known.mode()[0]
    return "Not enough data"

fav_cat = df.groupby("CustomerName").apply(favorite_known_category, include_groups=False)
customer_summary["FavoriteCategory"] = customer_summary["CustomerName"].map(fav_cat)

print("Customer-level summary:")
print(customer_summary)

# ---------------------------------------------------------
# 2. Segment customers by age group
# ---------------------------------------------------------
bins = [18, 25, 35, 45, 60]
labels = ["19-25", "26-35", "36-45", "46-59"]
customer_summary["AgeGroup"] = pd.cut(customer_summary["Age"], bins=bins, labels=labels, right=True)

age_group_summary = customer_summary.groupby("AgeGroup", observed=True).agg(
    Customers=("CustomerName", "count"),
    AvgSpend=("TotalSpend", "mean")
)
print("\nSpend by age group:")
print(age_group_summary)

# ---------------------------------------------------------
# 3. Segment customers by value (using spend quartiles)
# ---------------------------------------------------------
customer_summary["ValueSegment"] = pd.qcut(
    customer_summary["TotalSpend"], q=[0, 0.5, 0.8, 1.0], labels=["Regular", "High Value", "Top Value"]
)

segment_summary = customer_summary.groupby("ValueSegment", observed=True).agg(
    Customers=("CustomerName", "count"),
    AvgSpend=("TotalSpend", "mean")
)
print("\nCustomer value segments:")
print(segment_summary)

# ---------------------------------------------------------
# 4. Segment by location (city)
# ---------------------------------------------------------
city_summary = customer_summary.groupby("City", observed=True).agg(
    Customers=("CustomerName", "count"),
    AvgSpend=("TotalSpend", "mean")
).sort_values("AvgSpend", ascending=False)
print("\nSpend by city:")
print(city_summary)

# ---------------------------------------------------------
# 5. Most valuable customers
# ---------------------------------------------------------
top_customers = customer_summary.head(3)
print("\nTop 3 most valuable customers:")
print(top_customers[["CustomerName", "TotalSpend", "TotalOrders", "FavoriteCategory"]])

# ---------------------------------------------------------
# 6. Visual reports
# ---------------------------------------------------------

# Total spend by customer
plt.figure(figsize=(9, 5))
sns.barplot(data=customer_summary, x="CustomerName", y="TotalSpend", hue="ValueSegment", dodge=False)
plt.title("Total Spend by Customer")
plt.xlabel("Customer")
plt.ylabel("Total Spend (INR)")
plt.xticks(rotation=45)
plt.legend(title="Segment")
plt.savefig("chart1_spend_by_customer.png", dpi=150)
plt.close()

# Average spend by age group
plt.figure(figsize=(7, 5))
sns.barplot(x=age_group_summary.index, y=age_group_summary["AvgSpend"], hue=age_group_summary.index,
            palette="crest", legend=False)
plt.title("Average Spend by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Average Spend (INR)")
plt.savefig("chart2_spend_by_age_group.png", dpi=150)
plt.close()

# Customer value segments (pie)
plt.figure(figsize=(6, 6))
segment_counts = customer_summary["ValueSegment"].value_counts()
plt.pie(segment_counts.values, labels=segment_counts.index, autopct="%1.0f%%",
        colors=sns.color_palette("crest", len(segment_counts)), startangle=90)
plt.title("Customer Value Segments")
plt.savefig("chart3_value_segments.png", dpi=150)
plt.close()

# Spend by city
plt.figure(figsize=(7, 5))
sns.barplot(x=city_summary.index, y=city_summary["AvgSpend"], hue=city_summary.index,
            palette="mako", legend=False)
plt.title("Average Customer Spend by City")
plt.xlabel("City")
plt.ylabel("Average Spend (INR)")
plt.xticks(rotation=30)
plt.savefig("chart4_spend_by_city.png", dpi=150)
plt.close()

print("\nSaved 4 charts.")

# ---------------------------------------------------------
# 7. Save customer summary + bonus marketing report
# ---------------------------------------------------------
customer_summary.to_csv("customer_summary.csv", index=False)

top_age_group = age_group_summary["AvgSpend"].idxmax()
top_city = city_summary.index[0]
top_value_count = segment_counts.get("Top Value", 0)

report = f"""CUSTOMER ANALYSIS & MARKETING STRATEGY REPORT
================================================

Customers analyzed: {len(customer_summary)}
Total revenue: ₹{customer_summary['TotalSpend'].sum():,.0f}

KEY INSIGHTS
------------
1. Highest-spending age group: {top_age_group} years (avg spend ₹{age_group_summary.loc[top_age_group, 'AvgSpend']:,.0f}).
2. Highest average spend by city: {top_city} (avg ₹{city_summary.loc[top_city, 'AvgSpend']:,.0f}).
3. {top_value_count} customer(s) fall into the "Top Value" segment (top 20% by spend),
   contributing disproportionately to total revenue.
4. Top customer: {top_customers.iloc[0]['CustomerName']}, with ₹{top_customers.iloc[0]['TotalSpend']:,.0f}
   spent across {int(top_customers.iloc[0]['TotalOrders'])} order(s), favoring {top_customers.iloc[0]['FavoriteCategory']}.

Note: This dataset is small (10 unique customers), so segment sizes and trends here are
illustrative of the method rather than statistically robust — the same grouping and
segmentation logic scales directly to a larger real dataset.

SUGGESTED MARKETING STRATEGIES
-------------------------------
- Top Value segment: enroll in a loyalty/rewards program and offer early access to new
  products, since retaining them protects a disproportionate share of revenue.
- Regular segment: target with re-engagement offers (e.g. limited-time discounts) to
  increase order frequency and shift them toward the High Value tier.
- {top_age_group} age group: since this group already spends the most on average, tailor
  product recommendations and ad creative toward their apparent favorite categories.
- {top_city}: given the strongest average spend per customer, consider concentrated local
  marketing (city-specific promotions, faster delivery options) to reinforce loyalty there.
- Customers with a clear FavoriteCategory: use category-specific email campaigns
  (e.g. new arrivals in that category) rather than generic blasts, since purchase history
  shows a clear preference.
"""

with open("customer_analysis_report.txt", "w") as f:
    f.write(report)

print("\n" + report)
print("Saved customer_analysis_report.txt")
