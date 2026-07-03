# 📦 Express Logistics Cost Optimization & Strategic FP&A Pipeline

## 📌 Project Overview
This repository contains an enterprise-grade data analytics and financial modeling pipeline designed for **SPX Express (Shopee Xpress)**. The system is engineered to handle large-scale e-commerce logistics data (**500,000 delivery records**) to extract actionable financial insights, optimize the **Last-Mile Driver Expense Framework**, and conduct peer benchmarking against industry competitors.

The core objective of this tool is to empower the CFO and Senior Management with data-driven recommendations that enhance cost efficiency and protect regional profit margins.

---

## 🛠️ Data Architecture & Governance Framework

### 1. Operational Assumptions (FY2026)
* **Scale:** 500,000 unique Airway Bills (AWB) simulated with realistic e-commerce volume distribution (70% Standard, 20% Hemat, 10% Sameday).
* **Regional Multipliers:** Logistics to remote locations (e.g., Luar Jawa) incur a **2.2x tariff and opex scaling** due to geographical complexity.
* **Financial Unit:** All financial figures in the raw logs are processed in Indonesian Rupiah (IDR).

### 2. Financial Governance Rules
* **Cost Per Order (CPO) Formula:**
  $$\text{Total CPO} = \text{First \& Mid Mile Cost} + \text{Last Mile (Rider) Cost} + \text{Hub Operational Cost}$$
* **Net Profit Margin:**
  $$\text{Net Profit Margin (\%)} = \left( \frac{\text{Revenue} - \text{Total CPO}}{\text{Revenue}} \right) \times 100\%$$

---

## 📂 Repository Structure

```text
📁 spx-fpa-optimization/
│
├── 📄 README.md                 # Project documentation and executive summary
├── 📄 spx_large_delivery_data.csv # Generated data (500k rows - gitignored/auto-generated)
│
└── 📁 scripts/
    ├── 📄 spx_generator.py      # Generates 500,000 logistics rows with vector logic
    └── 📄 spx_analytics.py      # Strategic financial modeling & benchmarking engine
