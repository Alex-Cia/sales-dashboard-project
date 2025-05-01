import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Config ---
DATA_PATH = os.path.join('data', 'CloudNova_Sales_Data_2015_2024.csv')
OUTPUT_DIR = 'analysis'
DEBUG_MODE = True  # False to disable print() and chart popups

# --- Brand Color Palette ---
COLOR_CATEGORY = '#BB38DE'  # Purple
COLOR_REGION = '#00A88E'    # Teal
COLOR_CHANNEL = '#AE905F'   # Sand
COLOR_MONTHLY = '#00539F'   # Blue
COLOR_GRID = '#F2F2F2'
COLOR_TEXT = '#333333'

# --- Chart Styling ---
plt.rcParams['axes.facecolor'] = COLOR_GRID          # Plot background
plt.rcParams['figure.facecolor'] = COLOR_GRID        # Figure background
plt.rcParams['savefig.facecolor'] = COLOR_GRID       # Saved image background

# --- Text and Label Colors ---
plt.rcParams['text.color'] = COLOR_TEXT
plt.rcParams['axes.labelcolor'] = COLOR_TEXT
plt.rcParams['xtick.color'] = COLOR_TEXT
plt.rcParams['ytick.color'] = COLOR_TEXT
plt.rcParams['axes.titlecolor'] = COLOR_TEXT

# --- Helper Function: Chart Styling & Saving ---
def format_and_save_chart(xlabel, ylabel, filename):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    if DEBUG_MODE:
        plt.show()
    else:
        plt.close()


# --- Step 1: Load Dataset ---
df = pd.read_csv(DATA_PATH)
if DEBUG_MODE:
    print("📄 Preview of the dataset:")
    print(df.head())

# --- Step 2: Check for Missing Values ---
if DEBUG_MODE:
    print("\n🧹 Missing values in each column:")
    print(df.isnull().sum())

# --- Step 3: Core KPIs ---
total_sales = df['sales'].sum()
total_profit = df['profit'].sum()
average_sales = df['sales'].mean()
average_profit = df['profit'].mean()

if DEBUG_MODE:
    print("\n📊 Key Business Metrics:")
    print(f"Total Sales (2015–2024): ${total_sales:,.0f}")
    print(f"Total Profit (2015–2024): ${total_profit:,.0f}")
    print(f"Average Monthly Sales: ${average_sales:,.2f}")
    print(f"Average Monthly Profit: ${average_profit:,.2f}")

# --- Step 4: Profit by Product Category ---
category_profit = df.groupby('product_category')['profit'].sum().sort_values(ascending=False)
top_category = category_profit.idxmax()

if DEBUG_MODE:
    print("\n💡 Total Profit by Product Category:")
    print(category_profit)
    print(f"\n🏆 Most Profitable Category: {top_category} with ${category_profit.max():,.0f}")

category_profit.plot(kind='bar', color=COLOR_CATEGORY, title='Profit by Product Category')
format_and_save_chart('Product Category', 'Total Profit', 'profit_by_category.png')
category_profit.to_csv(os.path.join(OUTPUT_DIR, 'category_profit.csv'))

# --- Step 5: Profit by Region ---
region_profit = df.groupby('region')['profit'].sum().sort_values(ascending=False)
top_region = region_profit.idxmax()

if DEBUG_MODE:
    print("\n🌍 Total Profit by Region:")
    print(region_profit)
    print(f"\n🏅 Most Profitable Region: {top_region} with ${region_profit.max():,.0f}")

region_profit.plot(kind='bar', color=COLOR_REGION, title='Profit by Region')
format_and_save_chart('Region', 'Total Profit', 'profit_by_region.png')
region_profit.to_csv(os.path.join(OUTPUT_DIR, 'region_profit.csv'))

# --- Step 6: Profit by Sales Channel ---
channel_profit = df.groupby('channel')['profit'].sum().sort_values(ascending=False)
top_channel = channel_profit.idxmax()

if DEBUG_MODE:
    print("\n🛒 Total Profit by Sales Channel:")
    print(channel_profit)
    print(f"\n💻 Top Channel: {top_channel} with ${channel_profit.max():,.0f}")

channel_profit.plot(kind='bar', color=COLOR_CHANNEL, title='Profit by Sales Channel')
format_and_save_chart('Channel', 'Total Profit', 'profit_by_channel.png')
channel_profit.to_csv(os.path.join(OUTPUT_DIR, 'channel_profit.csv'))

# --- Step 7: Seasonal Profit by Month ---
month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
               'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
monthly_profit = df.groupby('month')['profit'].sum().reindex(month_order)
best_month = monthly_profit.idxmax()
worst_month = monthly_profit.idxmin()

if DEBUG_MODE:
    print("\n📆 Total Profit by Month:")
    print(monthly_profit)
    print(f"\n🌟 Best Month: {best_month.capitalize()}")
    print(f"🔻 Worst Month: {worst_month.capitalize()}")

monthly_profit.plot(kind='bar', color=COLOR_MONTHLY, title='Total Profit by Month')
format_and_save_chart('Month', 'Total Profit', 'profit_by_month.png')
monthly_profit.to_csv(os.path.join(OUTPUT_DIR, 'monthly_profit.csv'))

# --- Step 8: Save KPI Summary ---
summary_data = {
    "Total Sales": [total_sales],
    "Total Profit": [total_profit],
    "Average Monthly Sales": [average_sales],
    "Average Monthly Profit": [average_profit],
    "Top Category": [top_category],
    "Top Region": [top_region],
    "Top Channel": [top_channel],
    "Best Month": [best_month],
    "Worst Month": [worst_month]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(os.path.join(OUTPUT_DIR, 'summary.csv'), index=False)

if DEBUG_MODE:
    print("\n✅ Summary saved to analysis/summary.csv")
