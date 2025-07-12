import pandas as pd
import os
import glob

print("Current working directory:", os.getcwd())

# Only load .csv once
files = glob.glob("sales_*.csv")
print("Found files:", files)

if not files:
    print("⚠️ No sales CSV files found.")
    exit()

df_list = []

for file in files:
    try:
        df = pd.read_csv(file, usecols=["DATE", "EVENT", "INSIDE SALE'S"])
    except ValueError:
        print(f"⚠️ Skipping {file} — missing expected columns.")
        continue

    df = df.dropna(subset=["DATE"])  # Skip blank rows
    df["Month"] = file.replace("sales_", "").replace(".csv", "").title()
    df.rename(columns={"INSIDE SALE'S": "INSIDE_SALES"}, inplace=True)

    # Remove $ and commas
    df["INSIDE_SALES"] = df["INSIDE_SALES"].replace('[\\$,]', '', regex=True).astype(float)

    df_list.append(df)

if not df_list:
    print("⚠️ No valid data found in any files.")
    exit()

data = pd.concat(df_list, ignore_index=True)

print("\n=== Total Inside Sales by Month ===")
print(data.groupby("Month")["INSIDE_SALES"].sum().sort_index())

print("\n=== Total Inside Sales Across All Months ===")
print(f"${data['INSIDE_SALES'].sum():,.2f}")
