# Task 4: Customer Data Analysis

Internship task — analyzing customer-level purchasing behavior, segmenting customers, and
proposing marketing strategies based on the findings.

## Objective
- Analyze customer information to understand purchasing behavior.
- Segment customers based on age, location, or buying patterns.
- Identify the most valuable customer groups.
- Create visual reports to summarize customer insights.
- Bonus: Suggest marketing strategies based on the analysis.

## Input
`ecommerce_orders_with_age.csv` — the cleaned dataset from [Task 1](../Task1_Data_Cleaning),
extended with a `CustomerAge` field. The original dataset didn't capture customer age, so this
was added to enable age-based segmentation as required by this task.

## Approach
1. **Customer-level summary** — aggregated order-level data into one row per customer:
   total orders, total spend, average order value, primary city, and favorite category
   (excluding the "Unknown" placeholder from Task 1's missing-data handling, so the insight
   reflects a real preference rather than a data gap).
2. **Segmentation**
   - By **age group** (19-25, 26-35, 36-45, 46-59) — compared average spend across groups.
   - By **spend/value** (Regular, High Value, Top Value, using spend quartiles) — to identify
     the customers contributing disproportionately to revenue.
   - By **city** — compared average customer spend across locations.
3. **Most valuable customers** — ranked customers by total spend and pulled out the top 3.
4. **Visual reports** — 4 charts covering spend by customer, spend by age group, value segment
   split, and spend by city.
5. **Bonus: marketing strategies** — translated the segmentation results into concrete,
   segment-specific marketing suggestions (see `customer_analysis_report.txt`).

## Key findings
- The dataset covers 10 unique customers with a combined spend of ₹164,982.
- The 26-35 age group had the highest average spend.
- Mumbai customers had the highest average spend by city.
- The top 20% of customers by spend ("Top Value" segment) account for a disproportionate
  share of total revenue — a classic 80/20 pattern worth acting on.

## A note on the dataset size
This is a small practice dataset (10 unique customers), so segment sizes here are meant to
demonstrate the method, not to be statistically significant on their own. The same grouping,
segmentation, and reporting logic applies directly to a larger, real customer dataset.

## Files
| File | Description |
|---|---|
| `ecommerce_orders_with_age.csv` | Input dataset (Task 1 output + CustomerAge) |
| `customer_analysis.py` | Python/Pandas/Matplotlib/Seaborn script performing the full analysis |
| `customer_summary.csv` | One row per customer with spend, orders, segment, and favorite category |
| `customer_analysis_report.txt` | Key insights and suggested marketing strategies |
| `chart1_spend_by_customer.png` | Total spend per customer, colored by value segment |
| `chart2_spend_by_age_group.png` | Average spend by age group |
| `chart3_value_segments.png` | Customer value segment split (pie chart) |
| `chart4_spend_by_city.png` | Average customer spend by city |

## Tools used
Python, Pandas, NumPy, Matplotlib, Seaborn
