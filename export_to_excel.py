import pandas as pd
import glob

# Find all sales files
files = glob.glob("sales_*.csv")
print("Found files:", files)

if not files:
    print("⚠️ No sales files found.")
    exit()

# Create Excel writer object
with pd.ExcelWriter("Sales_Report.xlsx", engine="xlsxwriter") as writer:
    summary_data = []

    for file in files:
        try:
            # Read the file and clean it
            df = pd.read_csv(file, usecols=["DATE", "EVENT", "INSIDE SALE'S"])
            df = df.dropna(subset=["DATE"])
            df.rename(columns={"INSIDE SALE'S": "INSIDE_SALES"}, inplace=True)
            df["INSIDE_SALES"] = df["INSIDE_SALES"].replace('[\\$,]', '', regex=True).astype(float)

            # Extract month from filename for sheet name
            sheet_name = file.replace("sales_", "").replace(".csv", "").title()

            # Save to that sheet in Excel
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Save summary info
            summary_data.append({
                "Month": sheet_name,
                "Total Sales": df["INSIDE_SALES"].sum()
            })

        except Exception as e:
            print(f"❌ Skipping {file} due to error: {e}")

    # Optional: create a summary sheet
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        print("✅ Summary sheet created.")

print("📁 Sales_Report.xlsx has been created.")
