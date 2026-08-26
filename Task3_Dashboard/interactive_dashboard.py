"""
Task 3: Data Visualization Dashboard (Bonus - Interactive Dashboard)
------------------------------------------------------------------------
Builds a single-page interactive HTML dashboard using Plotly, combining
multiple chart types into one view - a lightweight alternative to
Power BI / Tableau that runs entirely from Python.

Input: ecommerce_orders_cleaned.csv (from Task 1)
Output: interactive_dashboard.html (open in any browser)
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("ecommerce_orders_cleaned.csv", parse_dates=["OrderDate"])

category_revenue = df.groupby("Category")["TotalAmount"].sum().sort_values(ascending=False)
daily_revenue = df.groupby(df["OrderDate"].dt.date)["TotalAmount"].sum().sort_index()
payment_counts = df["PaymentMode"].value_counts()
city_orders = df["City"].value_counts()

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Revenue by Category", "Revenue Trend Over Time",
        "Payment Mode Share", "Orders by City"
    ),
    specs=[[{"type": "bar"}, {"type": "scatter"}],
           [{"type": "pie"}, {"type": "bar"}]],
    vertical_spacing=0.15, horizontal_spacing=0.12
)

# Bar: revenue by category
fig.add_trace(go.Bar(
    x=category_revenue.index, y=category_revenue.values,
    marker_color="#2A6F97", name="Revenue by Category",
    hovertemplate="%{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>"
), row=1, col=1)

# Line: revenue trend
fig.add_trace(go.Scatter(
    x=[str(d) for d in daily_revenue.index], y=daily_revenue.values,
    mode="lines+markers", line=dict(color="#3E7CB1", width=3),
    name="Daily Revenue",
    hovertemplate="%{x}<br>Revenue: ₹%{y:,.0f}<extra></extra>"
), row=1, col=2)

# Pie: payment mode
fig.add_trace(go.Pie(
    labels=payment_counts.index, values=payment_counts.values,
    hole=0.35, name="Payment Mode",
    hovertemplate="%{label}<br>%{value} orders (%{percent})<extra></extra>"
), row=2, col=1)

# Bar: orders by city
fig.add_trace(go.Bar(
    x=city_orders.index, y=city_orders.values,
    marker_color="#5FA8D3", name="Orders by City",
    hovertemplate="%{x}<br>%{y} orders<extra></extra>"
), row=2, col=2)

fig.update_layout(
    title_text="E-Commerce Orders — Interactive Dashboard",
    title_font_size=22,
    showlegend=False,
    height=800,
    template="plotly_white",
    margin=dict(t=100)
)

fig.write_html("interactive_dashboard.html")
print("Saved interactive_dashboard.html — open this file in any browser.")
