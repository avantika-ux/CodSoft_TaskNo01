# Task 3: Data Visualization Dashboard

Internship task — creating a set of meaningful, well-labeled visualizations from the cleaned
dataset, plus a bonus interactive dashboard.

## Objective
- Create meaningful visualizations using Matplotlib, Seaborn, or Plotly.
- Design bar charts, line charts, pie charts, histograms, and scatter plots.
- Customize charts with titles, labels, legends, and color schemes.
- Present insights through clear and easy-to-understand visualizations.
- Bonus: Build an interactive dashboard using Power BI or Tableau.

## Input
`ecommerce_orders_cleaned.csv` — the cleaned dataset produced in
[Task 1: Data Cleaning](../Task1_Data_Cleaning).

## Approach
1. **Static charts** (`static_charts.py`) — built with Matplotlib and Seaborn:
   - Bar chart: revenue by product category
   - Line chart: revenue trend over time
   - Pie chart: payment mode share
   - Histogram: distribution of order value
   - Scatter plot: quantity vs order value, colored by category
   - Bar chart: number of orders by city
   Each chart has a clear title, axis labels, a consistent color palette, and a legend where relevant.
2. **Interactive dashboard** (`interactive_dashboard.py`) — combines four of the charts above
   into a single-page interactive HTML dashboard using Plotly, as a lightweight,
   code-based alternative to Power BI/Tableau that needs no extra software to view —
   just a browser.

## Files
| File | Description |
|---|---|
| `ecommerce_orders_cleaned.csv` | Input dataset (from Task 1) |
| `static_charts.py` | Script generating 6 static charts with Matplotlib/Seaborn |
| `interactive_dashboard.py` | Script generating the interactive Plotly dashboard |
| `interactive_dashboard.html` | **Open this in a browser** — the interactive dashboard |
| `chart1_bar_revenue_by_category.png` | Revenue by category |
| `chart2_line_revenue_trend.png` | Revenue trend over time |
| `chart3_pie_payment_mode.png` | Payment mode share |
| `chart4_histogram_order_value.png` | Order value distribution |
| `chart5_scatter_quantity_vs_value.png` | Quantity vs order value |
| `chart6_bar_orders_by_city.png` | Orders by city |

## Tools used
Python, Pandas, Matplotlib, Seaborn, Plotly
