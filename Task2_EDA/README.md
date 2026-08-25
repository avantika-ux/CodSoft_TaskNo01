# Task 2 — Exploratory Data Analysis (EDA)

**InAmigos Foundation Internship**

## Objective
- Load a dataset and examine its features using descriptive statistics
- Identify trends, distributions, and relationships between variables
- Detect outliers and unusual patterns within the data
- Use summary statistics to answer key business questions
- (Bonus) Short report highlighting findings

## Dataset
`ecommerce_orders_cleaned.csv` — 40 e-commerce orders with 9 columns: `OrderID`, `CustomerName`, `City`, `Category`, `Quantity`, `Price`, `PaymentMode`, `OrderDate`, `TotalAmount`.

## How to run
```bash
pip install pandas matplotlib
python eda_analysis.py
```
Charts are saved to the `charts/` folder.

## Key Findings

### 1. Overview
- 40 orders, no missing values, and `TotalAmount` correctly equals `Quantity × Price` for every row (0 mismatches) — the data is clean and consistent.
- Average order value: **₹4,125** (median ₹2,998), ranging from ₹398 to ₹14,995.

### 2. Revenue by category
![Revenue by category](charts/revenue_by_category.png)

"Unknown" is the top category by revenue (₹48,965 from 10 orders — 25% of all orders), followed closely by Books (₹44,475) and Electronics (₹36,077). Furniture, Clothing, and Groceries trail well behind.

**Business question — which categories drive revenue?** Books and Electronics are the strongest *known* categories. However, a quarter of all orders have no valid category label, which limits how much we can trust category-level reporting until this is fixed at the source.

### 3. Revenue trend over time
![Revenue trend](charts/revenue_trend.png)

Revenue drops sharply across the three order dates in the dataset: ₹90,934 (Jan 15) → ₹45,468 (Feb 20) → ₹28,580 (Mar 5). This is worth investigating further — it may reflect a real decline, a seasonal effect, or simply that Jan 15 includes a batch of large orders (see outliers below) that skew the comparison.

### 4. Revenue by city
![Revenue by city](charts/revenue_by_city.png)

Pune (₹43,965) and Mumbai (₹42,976) are the top two cities by revenue. Chennai has only 2 orders but ₹18,991 in revenue — driven by high-value orders rather than order volume.

### 5. Order value distribution & outliers
![Order value distribution](charts/order_value_distribution.png)

Using the IQR method on `TotalAmount` (bounds: -₹3,560 to ₹9,931), **3 orders are flagged as outliers**, all placed by the same customer, **Aman Verma**:

| OrderID | Category | Quantity | Price | TotalAmount |
|---|---|---|---|---|
| ORD1052 | Unknown | 5 | ₹2,999 | ₹14,995 |
| ORD1055 | Books | 5 | ₹2,999 | ₹14,995 |
| ORD1043 | Unknown | 5 | ₹1,999 | ₹9,995 |

These aren't data errors — each is a legitimate bulk purchase (quantity × price checks out). Aman Verma is also the top customer overall by total spend (₹71,466 across 9 orders), more than double the next highest customer.

### 6. Payment mode
UPI orders have the highest average value (₹5,278), followed by Cash on Delivery (₹4,187), Credit Card (₹3,728), and Debit Card (₹2,764) — even though Credit Card is used most often (13 orders).

### 7. Relationships between variables
`TotalAmount` correlates more strongly with `Price` (r = 0.75) than with `Quantity` (r = 0.54) — order value is driven more by the price of items purchased than by how many are bought.

## Data quality note
25% of orders (10 of 40) have `Category = "Unknown"`. Since this affects category-level analysis significantly, resolving this at the source (or via product-ID lookup) should be a priority before this dataset is used for business decisions.

## Summary
- Revenue is concentrated: Pune/Mumbai lead by city, Books/Electronics lead by known category, and one customer (Aman Verma) accounts for ~15% of total revenue.
- Revenue is declining across the three order dates in the dataset — worth deeper investigation.
- Data is clean and internally consistent, but the "Unknown" category gap should be addressed.
