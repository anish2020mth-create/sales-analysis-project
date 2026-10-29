"""
Sales Data Analysis - PGDM (Business Analytics) College Project
Author: Anish Raj

What this script does:
1. Loads the sales data
2. Cleans it
3. Answers simple business questions
4. Saves charts in the 'images' folder
"""

import os

import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("images", exist_ok=True)

# ---------- 1. LOAD DATA ----------
df = pd.read_csv("data/sales_data.csv")
print("First 5 rows:")
print(df.head(), "\n")

# ---------- 2. CLEAN DATA ----------
df["Date"] = pd.to_datetime(df["Date"])      # make Date a real date
df = df.drop_duplicates()                    # remove repeated rows
df = df.dropna()                             # remove empty rows
df["Month"] = df["Date"].dt.month_name()     # new column: month name
df["Month_No"] = df["Date"].dt.month         # for correct ordering

# ---------- 3. KEY NUMBERS (KPIs) ----------
total_revenue = df["Revenue"].sum()
total_orders = df["Order_ID"].count()
avg_order_value = df["Revenue"].mean()

print("========== KEY NUMBERS ==========")
print(f"Total Revenue       : Rs {total_revenue:,.0f}")
print(f"Total Orders        : {total_orders}")
print(f"Average Order Value : Rs {avg_order_value:,.0f}\n")

# ---------- 4. BUSINESS QUESTIONS ----------
# Q1. Which product earns the most?
product_sales = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
print("Revenue by Product:\n", product_sales, "\n")

# Q2. Which region sells the most?
region_sales = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
print("Revenue by Region:\n", region_sales, "\n")

# Q3. How does revenue change month by month?
monthly_sales = df.groupby(["Month_No", "Month"])["Revenue"].sum().reset_index()
best_month = monthly_sales.loc[monthly_sales["Revenue"].idxmax(), "Month"]
print("Best month:", best_month, "\n")

# ---------- 5. CHARTS ----------
# Chart 1: Revenue by product
plt.figure(figsize=(8, 5))
product_sales.plot(kind="bar", color="steelblue")
plt.title("Total Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (Rs)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("images/revenue_by_product.png")
plt.close()

# Chart 2: Revenue by region
plt.figure(figsize=(6, 6))
region_sales.plot(kind="pie", autopct="%1.1f%%")
plt.title("Revenue Share by Region")
plt.ylabel("")
plt.tight_layout()
plt.savefig("images/revenue_by_region.png")
plt.close()

# Chart 3: Monthly trend
plt.figure(figsize=(10, 5))
plt.plot(monthly_sales["Month"].str[:3], monthly_sales["Revenue"],
         marker="o", color="green")
plt.title("Monthly Revenue Trend (2025)")
plt.xlabel("Month")
plt.ylabel("Revenue (Rs)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("images/monthly_trend.png")
plt.close()

print("Charts saved in the 'images' folder.")

# ---------- 6. SAVE SUMMARY ----------
with open("summary.txt", "w") as f:
    f.write("SALES ANALYSIS SUMMARY\n")
    f.write("======================\n")
    f.write(f"Total Revenue       : Rs {total_revenue:,.0f}\n")
    f.write(f"Total Orders        : {total_orders}\n")
    f.write(f"Average Order Value : Rs {avg_order_value:,.0f}\n")
    f.write(f"Top Product         : {product_sales.index[0]}\n")
    f.write(f"Top Region          : {region_sales.index[0]}\n")
    f.write(f"Best Month          : {best_month}\n")
print("Summary saved in summary.txt")
