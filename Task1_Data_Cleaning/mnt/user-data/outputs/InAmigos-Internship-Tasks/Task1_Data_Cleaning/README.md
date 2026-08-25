# Task 1: Data Cleaning & Preprocessing

Internship task for **InAmigos Foundation** — cleaning and preparing a raw dataset for analysis using Python and Pandas.

## Objective
- Import a dataset using Python and inspect its structure.
- Identify missing values, duplicate records, and inconsistent data entries.
- Clean the dataset by handling null values, removing duplicates, and correcting data types.
- Prepare the data for further analysis using Pandas.
- Bonus: Save the cleaned dataset as a new CSV file.

## Dataset
`ecommerce_orders_raw.csv` — a sample e-commerce orders dataset (68 rows) containing common
real-world data quality issues:
- Missing values across multiple columns
- Fully duplicate rows
- Inconsistent text formatting (e.g. `mumbai` vs `Mumbai` vs `MUMBAI`, `COD` vs `Cash on Delivery`)
- Invalid values (negative quantities)
- Numbers stored as text (e.g. `"1,999"`)
- Mixed and invalid date formats

## Approach
1. **Inspect** — loaded the CSV with `pandas.read_csv`, checked shape, dtypes, and null counts with `.info()` and `.isnull().sum()`.
2. **Identify issues** — checked `.duplicated().sum()` for repeated rows and `.unique()` on categorical columns to surface inconsistent labels.
3. **Clean**
   - Dropped fully empty rows and rows missing a unique `OrderID`.
   - Removed exact duplicate rows.
   - Standardized text fields (trimmed whitespace, unified casing, merged synonyms like `Bengaluru` → `Bangalore`).
   - Converted `Price` and `Quantity` to numeric types, coercing invalid entries (e.g. negative quantities, comma-formatted prices) to null.
   - Filled remaining numeric gaps with the column median.
   - Parsed `OrderDate` into proper datetime format, dropping rows with unparseable dates.
4. **Prepare for analysis** — added a derived `TotalAmount` column (`Price × Quantity`) for downstream analysis.
5. **Export** — saved the cleaned dataset as `ecommerce_orders_cleaned.csv`.

## Result
The dataset went from 68 raw rows (with nulls, duplicates, and inconsistencies) to 40 clean,
analysis-ready rows with zero missing values and correct data types.

## Files
| File | Description |
|---|---|
| `ecommerce_orders_raw.csv` | Original raw dataset |
| `clean_data.py` | Python/Pandas script performing the full cleaning pipeline |
| `ecommerce_orders_cleaned.csv` | Final cleaned dataset |

## Tools Used
Python, Pandas, NumPy
