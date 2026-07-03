import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ------------------------------
# 1. Parameter & Seed
# ------------------------------
n_rows = 500_000
np.random.seed(42)

regions = ["Jabodetabek", "Jawa Barat", "Jawa Tengah", "Jawa Timur", "Luar Jawa"]
service_types = ["SPX Sameday", "SPX Standard", "SPX Hemat"]
hubs = [
    "Hub Jakarta DC",
    "Hub Bandung DC",
    "Hub Semarang DC",
    "Hub Surabaya DC",
    "Hub Medan DC",
]
delivery_status = ["Delivered On-Time", "Delivered Late", "Returned to Seller"]

print(f"Sedang meng-generate {n_rows:,} data pengiriman SPX Express...")

# ------------------------------
# 2. Generate data kategorikal
# ------------------------------
selected_regions = np.random.choice(regions, n_rows, p=[0.45, 0.20, 0.15, 0.12, 0.08])
selected_services = np.random.choice(
    service_types, n_rows, p=[0.10, 0.70, 0.20]
)
selected_hubs = np.random.choice(hubs, n_rows)
selected_status = np.random.choice(
    delivery_status, n_rows, p=[0.88, 0.09, 0.03]
)

# Generate ID Resi (format: SPXID2026xxxxxxx)
# Lebih cepat dengan list comprehension
awb_ids = [f"SPXID2026{i:07d}" for i in range(1, n_rows + 1)]

# (Opsional) Generate tanggal pengiriman acak dalam 30 hari terakhir
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
random_days = np.random.randint(0, 30, n_rows)
delivery_dates = [end_date - timedelta(days=int(d)) for d in random_days]

# ------------------------------
# 3. Pemodelan Finansial (Revenue & Cost)
# ------------------------------
# Revenue dasar per tipe layanan
revenue_map = {"SPX Sameday": 25000, "SPX Standard": 15000, "SPX Hemat": 9000}
base_revenue = np.array([revenue_map[s] for s in selected_services])

# Faktor regional (Luar Jawa lebih mahal)
regional_multiplier = np.where(selected_regions == "Luar Jawa", 2.2, 1.0)
actual_revenue = np.round(base_revenue * regional_multiplier, -2).astype(int)  # integer Rupiah

# First Mile & Mid Mile Cost (30-38% dari revenue)
first_mid_mile = np.round(actual_revenue * np.random.uniform(0.30, 0.38, n_rows), -2).astype(int)

# Last Mile Cost (insentif kurir) – lebih tinggi untuk Sameday atau Luar Jawa
last_mile_multiplier = np.where(
    (selected_services == "SPX Sameday") | (selected_regions == "Luar Jawa"),
    np.random.uniform(0.35, 0.45, n_rows),
    np.random.uniform(0.22, 0.28, n_rows),
)
last_mile = np.round(actual_revenue * last_mile_multiplier, -2).astype(int)

# Hub Operational Cost (12-16% dari revenue)
hub_operational = np.round(actual_revenue * np.random.uniform(0.12, 0.16, n_rows), -2).astype(int)

# Total Cost & Profit
total_cost = first_mid_mile + last_mile + hub_operational
profit = actual_revenue - total_cost

# (Opsional) Pastikan tidak ada biaya negatif – sudah terjamin karena multiplier > 0

# ------------------------------
# 4. Bentuk DataFrame
# ------------------------------
df_spx = pd.DataFrame({
    "AWB_Number": awb_ids,
    "Delivery_Date": delivery_dates,        # opsional
    "Region": pd.Categorical(selected_regions, categories=regions),
    "Service_Type": pd.Categorical(selected_services, categories=service_types),
    "Sorting_Hub": pd.Categorical(selected_hubs, categories=hubs),
    "Delivery_Status": pd.Categorical(selected_status, categories=delivery_status),
    "Revenue_Collected": actual_revenue,
    "First_Mid_Mile_Cost": first_mid_mile,
    "Last_Mile_Cost": last_mile,
    "Hub_Operational_Cost": hub_operational,
    "Total_Cost": total_cost,
    "Profit": profit,
})

# ------------------------------
# 5. Simpan & Ringkasan
# ------------------------------
df_spx.to_csv("spx_large_delivery_data.csv", index=False)
print(f"Sukses! File 'spx_large_delivery_data.csv' dengan {n_rows:,} baris data.")

print("\n--- Ringkasan Statistik ---")
print(df_spx[["Revenue_Collected", "Total_Cost", "Profit"]].describe())
print("\nDistribusi Status Pengiriman:")
print(df_spx["Delivery_Status"].value_counts(normalize=True))
