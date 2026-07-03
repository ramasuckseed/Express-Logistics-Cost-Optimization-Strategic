import pandas as pd

# --- CASE 1: LOGISTICS SPECIFIC REVENUE & DRIVER EXPENSE (Data Dummy 500k Paket) ---
# Mengasumsikan kita menganalisis 500,000 paket pengiriman SPX Express
print("Memproses 500,000 Data Resi Pengiriman SPX Express...")

# Representasi Data Agregat untuk Simulasi Struktur Biaya Last-Mile
delivery_data = {
    "Region": [
        "Jabodetabek",
        "Jawa Barat",
        "Jawa Tengah",
        "Jawa Timur",
        "Luar Jawa",
    ],
    "Total_Parcels": [200000, 90000, 70000, 80000, 60000],
    "Actual_Revenue_IDR_Mn": [2000, 990, 770, 880, 960],
    "Driver_Incentive_IDR_Mn": [600, 315, 245, 280, 420],  # Driver Expense
    "Hub_Operational_IDR_Mn": [400, 200, 160, 180, 240],
}
df_spx = pd.DataFrame(delivery_data)

# Hitung Cost Per Order (CPO) untuk Komponen Kurir/Driver
df_spx["Total_Cost_IDR_Mn"] = (
    df_spx["Driver_Incentive_IDR_Mn"] + df_spx["Hub_Operational_IDR_Mn"]
)
df_spx["Driver_Cost_Per_Parcel_IDR"] = (
    (df_spx["Driver_Incentive_IDR_Mn"] / df_spx["Total_Parcels"]) * 1000000
).round(0)
df_spx["Total_CPO_IDR"] = (
    (df_spx["Total_Cost_IDR_Mn"] / df_spx["Total_Parcels"]) * 1000000
).round(0)
df_spx["Profit_Margin_%"] = (
    (df_spx["Actual_Revenue_IDR_Mn"] - df_spx["Total_Cost_IDR_Mn"])
    / df_spx["Actual_Revenue_IDR_Mn"]
) * 100

print("\n=== SPX LAST-MILE COST PER PARCEL ANALYSIS ===")
print(
    df_spx[
        [
            "Region",
            "Total_Parcels",
            "Driver_Cost_Per_Parcel_IDR",
            "Total_CPO_IDR",
            "Profit_Margin_%",
        ]
    ].to_string(index=False)
)


# --- CASE 2: PEER BENCHMARKING (COMPETITOR ANALYSIS) ---
# Sesuai JD: "Conduct detailed peer benchmarking and analyze competitor annual reports"
print("\n" + "=" * 60)
print("     PEER BENCHMARKING MATRIX (SPX vs J&T vs JNE vs NinjaXpress)     ")
print("=" * 60)

benchmarking_data = {
    "Metric (FY2025/2026)": [
        "Market Share (%)",
        "Average CPO (IDR)",
        "Automation Rate (%)",
        "SLA Delivery Speed (Hours)",
    ],
    "SPX Express (In-house)": [28.0, 7200, 85.0, 32.0],
    "J&T Express (Peer A)": [32.0, 7500, 90.0, 28.0],
    "JNE (Peer B)": [22.0, 8100, 45.0, 42.0],
    "Ninja Xpress (Peer C)": [12.0, 7800, 70.0, 36.0],
}
df_bench = pd.DataFrame(benchmarking_data)
print(df_bench.to_string(index=False))

import pandas as pd

# Load 500k data
df = pd.read_csv("spx_large_delivery_data.csv")

# 1. Hitung Total CPO dan Profit Margin
df["Total_CPO"] = (
    df["First_Mid_Mile_Cost"] + df["Last_Mile_Cost"] + df["Hub_Operational_Cost"]
)
df["Net_Profit"] = df["Revenue_Collected"] - df["Total_CPO"]

# 2. Analisis Agregasi Makro untuk Direksi
regional_analysis = (
    df.groupby("Region")[
        [
            "Revenue_Collected",
            "Total_CPO",
            "Last_Mile_Cost",
            "Net_Profit",
        ]
    ]
    .sum()
    / 1000000
).round(2)  # Konversi ke Jutaan Rupiah

regional_analysis["Rider_Expense_Contribution_%"] = (
    (regional_analysis["Last_Mile_Cost"] / regional_analysis["Total_CPO"]) * 100
).round(2)
regional_analysis["Profit_Margin_%"] = (
    (regional_analysis["Net_Profit"] / regional_analysis["Revenue_Collected"]) * 100
).round(2)

print("=======================================================================")
print("             SPX EXPRESS - REGIONAL COST OPTIMIZATION REPORT           ")
print("=======================================================================")
print(
    regional_analysis[
        ["Total_CPO", "Rider_Expense_Contribution_%", "Profit_Margin_%"]
    ]
)

# 3. Deteksi Kebocoran Biaya pada Paket Gagal / Retur (Returned to Seller)
# Paket gagal biasanya memakan biaya Last Mile ganda tanpa menghasilkan revenue baru
failed_delivery_cost = (
    df[df["Delivery_Status"] == "Returned to Seller"]["Total_CPO"].sum() / 1000000
)
print("\n" + "=" * 60)
print(
    f"⚠️ ESTIMASI KERUGIAN OPERASIONAL DARI PAKET RETUR: IDR {failed_delivery_cost:,.2f} Juta"
)
print("=" * 60)
