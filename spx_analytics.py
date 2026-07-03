import pandas as pd
from typing import List

# ====================================================================
# 1. FUNGSI INSIGHT EKSEKUTIF (YANG SUDAH DIPERBAIKI)
# ====================================================================
def generate_executive_insights(
    df_regional: pd.DataFrame,
    rts_loss: float,  # dalam jutaan IDR
    margin_threshold: float = 15.0,
    rider_contrib_threshold: float = 45.0,
    rts_loss_threshold: float = 50.0,
) -> str:
    """
    Menghasilkan ringkasan insight strategis eksekutif berdasarkan data regional.

    Parameters
    ----------
    df_regional : pd.DataFrame
        Harus memiliki kolom: 'Region', 'Profit_Margin_%', 'Rider_Expense_Contribution_%'
    rts_loss : float
        Total biaya kegagalan pengiriman (Return to Seller) dalam jutaan IDR.
    margin_threshold : float, default=15.0
        Batas bawah margin keuntungan (%) untuk memicu peringatan.
    rider_contrib_threshold : float, default=45.0
        Batas atas kontribusi biaya kurir (%) untuk memicu rekomendasi optimasi.
    rts_loss_threshold : float, default=50.0
        Ambang kerugian RTS (jutaan IDR) untuk memicu peringatan kebocoran.

    Returns
    -------
    str
        Gabungan insight yang sudah diformat.
    """
    # Validasi input
    if df_regional.empty:
        return "Tidak ada data regional untuk menghasilkan insight."

    required_cols = ['Region', 'Profit_Margin_%', 'Rider_Expense_Contribution_%']
    missing = [col for col in required_cols if col not in df_regional.columns]
    if missing:
        raise ValueError(f"Kolom yang hilang: {missing}")

    if not isinstance(rts_loss, (int, float)):
        raise TypeError("rts_loss harus berupa angka (dalam jutaan IDR).")

    insights: List[str] = []
    insights.append("=== AUTOMATED EXECUTIVE STRATEGIC INSIGHTS ===")
    insights.append("")

    # 1. Evaluasi margin regional
    low_margin = df_regional[df_regional['Profit_Margin_%'] < margin_threshold]
    if not low_margin.empty:
        for _, row in low_margin.iterrows():
            region = row['Region']
            margin = row['Profit_Margin_%']
            insights.append(
                f"🚨 CRITICAL MARGIN SQUEEZE: Region {region} memiliki margin {margin:.1f}% (di bawah {margin_threshold}%). "
                f"Tindakan: Tinjau ulang struktur harga atau konsolidasi rute."
            )
    else:
        insights.append("✅ Semua region memenuhi threshold margin minimum.")

    insights.append("")

    # 2. Evaluasi kontribusi biaya kurir
    high_rider = df_regional[df_regional['Rider_Expense_Contribution_%'] > rider_contrib_threshold]
    if not high_rider.empty:
        for _, row in high_rider.iterrows():
            region = row['Region']
            rider_contrib = row['Rider_Expense_Contribution_%']
            insights.append(
                f"💡 COST OPTIMIZATION MILESTONE: Region {region} memiliki kontribusi biaya kurir {rider_contrib:.1f}% (di atas {rider_contrib_threshold}%). "
                f"Rekomendasi: Beralih dari kontrak kurir tarif tetap ke model insentif berbasis volume."
            )
    else:
        insights.append("✅ Kontribusi biaya kurir masih dalam batas wajar.")

    insights.append("")

    # 3. Evaluasi kebocoran biaya reverse logistics
    if rts_loss > rts_loss_threshold:
        insights.append(
            f"⚠️ REVERSE LOGISTICS LEAKAGE: Gagal kirim (RTS) menyebabkan kebocoran kas sebesar IDR {rts_loss:,.2f} Juta periode ini. "
            f"Strategi: Implementasikan validasi nomor telepon/alamat berbasis AI saat checkout untuk menurunkan kegagalan pertama kali hingga 15%."
        )
    else:
        insights.append("✅ Biaya reverse logistics masih dalam batas wajar.")

    # Insight tambahan: region dengan margin tertinggi
    top_region = df_regional.loc[df_regional['Profit_Margin_%'].idxmax(), 'Region']
    top_margin = df_regional['Profit_Margin_%'].max()
    insights.append("")
    insights.append(f"🏆 Region dengan margin tertinggi: {top_region} ({top_margin:.1f}%).")

    return "\n\n".join(insights)


# ====================================================================
# 2. BAGIAN ANALISIS UTAMA (YANG SUDAH ANDA BUAT)
# ====================================================================
print("Memproses 500,000 Data Resi Pengiriman SPX Express...")

# --- Data dummy agregat (CASE 1) ---
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
    "Driver_Incentive_IDR_Mn": [600, 315, 245, 280, 420],
    "Hub_Operational_IDR_Mn": [400, 200, 160, 180, 240],
}
df_spx = pd.DataFrame(delivery_data)

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

# --- Peer Benchmarking (CASE 2) ---
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

# --- Load data 500k (dari file CSV yang sudah digenerate) ---
df = pd.read_csv("spx_large_delivery_data.csv")

# Hitung Total CPO dan Net Profit
df["Total_CPO"] = (
    df["First_Mid_Mile_Cost"] + df["Last_Mile_Cost"] + df["Hub_Operational_Cost"]
)
df["Net_Profit"] = df["Revenue_Collected"] - df["Total_CPO"]

# Agregasi regional
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
).round(2)  # Konversi ke jutaan Rupiah

regional_analysis["Rider_Expense_Contribution_%"] = (
    (regional_analysis["Last_Mile_Cost"] / regional_analysis["Total_CPO"]) * 100
).round(2)
regional_analysis["Profit_Margin_%"] = (
    (regional_analysis["Net_Profit"] / regional_analysis["Revenue_Collected"]) * 100
).round(2)

print("\n=======================================================================")
print("             SPX EXPRESS - REGIONAL COST OPTIMIZATION REPORT           ")
print("=======================================================================")
print(
    regional_analysis[
        ["Total_CPO", "Rider_Expense_Contribution_%", "Profit_Margin_%"]
    ]
)

# Deteksi biaya retur
failed_delivery_cost = (
    df[df["Delivery_Status"] == "Returned to Seller"]["Total_CPO"].sum() / 1000000
)
print("\n" + "=" * 60)
print(
    f"⚠️ ESTIMASI KERUGIAN OPERASIONAL DARI PAKET RETUR: IDR {failed_delivery_cost:,.2f} Juta"
)
print("=" * 60)


# ====================================================================
# 3. GENERATE EXECUTIVE INSIGHTS (MENGGUNAKAN FUNGSI YANG DIPERBAIKI)
# ====================================================================
# Reset index agar 'Region' menjadi kolom, karena fungsi membutuhkan kolom 'Region'
regional_analysis_with_region = regional_analysis.reset_index()

# Panggil fungsi insight
executive_summary = generate_executive_insights(
    df_regional=regional_analysis_with_region,
    rts_loss=failed_delivery_cost,          # dalam jutaan
    margin_threshold=15.0,                  # bisa diubah sesuai kebutuhan
    rider_contrib_threshold=45.0,
    rts_loss_threshold=50.0,
)

print("\n" + "=" * 60)
print(executive_summary)
print("=" * 60)
