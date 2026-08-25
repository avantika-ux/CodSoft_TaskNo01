"""
Task 1: Data Cleaning & Preprocessing
--------------------------------------
- Import a dataset and inspect its structure.
- Identify missing values, duplicate records, and inconsistent data entries.
- Clean the dataset (nulls, duplicates, data types).
- Prepare the data for further analysis with Pandas.
- Bonus: Save the cleaned dataset as a new CSV file.
"""

import pandas as pd
import numpy as np

# ---------------------------------------------------------
# 1. Import the dataset and inspect its structure
# ---------------------------------------------------------
df = pd.read_csv("ecommerce_orders_raw.csv")

print("Shape of dataset:", df.shape)
print("\nColumn info:")
print(df.info())
print("\nFirst 5 rows:")
print(df.head())

# ---------------------------------------------------------
# 2. Identify missing values, duplicates, inconsistent entries
# ---------------------------------------------------------
print("\nMissing values per column:")
print(df.isnull().sum())

print("\nNumber of fully duplicate rows:", df.duplicated().sum())

print("\nUnique values in 'City' (inconsistent casing/spacing visible here):")
print(df["City"].unique())

print("\nUnique values in 'PaymentMode' (inconsistent labels visible here):")
print(df["PaymentMode"].unique())

# ---------------------------------------------------------
# 3. Clean the dataset
# ---------------------------------------------------------

# 3a. Drop rows that are completely empty (all columns null)
df = df.dropna(how="all")

# 3b. Drop exact duplicate rows
df = df.drop_duplicates()

# 3c. Drop rows with no OrderID (can't identify the record)
df = df.dropna(subset=["OrderID"])

# 3d. Standardize text columns: trim whitespace, fix casing
df["CustomerName"] = df["CustomerName"].str.strip()
df["City"] = df["City"].str.strip().str.title()
df["City"] = df["City"].replace({"Bengaluru": "Bangalore"})  # merge synonyms

df["PaymentMode"] = df["PaymentMode"].str.strip().str.title()
df["PaymentMode"] = df["PaymentMode"].replace({"Cod": "Cash On Delivery"})

# 3e. Fix Category: fill missing with "Unknown"
df["Category"] = df["Category"].fillna("Unknown")

# 3f. Fix Price: remove commas, convert to numeric, coerce bad values to NaN
df["Price"] = df["Price"].astype(str).str.replace(",", "", regex=False)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# 3g. Fix Quantity: remove invalid (negative) values, convert to numeric
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df.loc[df["Quantity"] <= 0, "Quantity"] = np.nan

# 3h. Fill remaining numeric nulls with column median
df["Price"] = df["Price"].fillna(df["Price"].median())
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())
df["Quantity"] = df["Quantity"].astype(int)

# 3i. Fix OrderDate: parse multiple formats, invalid dates become NaT
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce", format="mixed")

# Drop rows where date could not be parsed at all (optional — keep if you'd rather flag them)
df = df.dropna(subset=["OrderDate"])

# 3j. Add a useful derived column for later analysis
df["TotalAmount"] = df["Price"] * df["Quantity"]

# ---------------------------------------------------------
# 4. Final check
# ---------------------------------------------------------
print("\nCleaned dataset shape:", df.shape)
print("\nMissing values after cleaning:")
print(df.isnull().sum())
print("\nData types after cleaning:")
print(df.dtypes)
print("\nSample of cleaned data:")
print(df.head(10))

# ---------------------------------------------------------
# 5. Bonus: Save the cleaned dataset
# ---------------------------------------------------------
df.to_csv("ecommerce_orders_cleaned.csv", index=False)
print("\nSaved cleaned dataset to ecommerce_orders_cleaned.csv")
