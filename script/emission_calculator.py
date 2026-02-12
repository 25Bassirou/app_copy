# scripts/emission_calculator.py

import pandas as pd
import os

# -----------------------------
# 1️⃣ Load emission factors
# -----------------------------

ef_df = pd.read_csv("data/emission_factors.csv")

# Standardize column names
ef_df.columns = [c.strip().lower() for c in ef_df.columns]

# Expecting: source, kgco2_per_mwh
ef_df.rename(columns={"source": "fuel"}, inplace=True)
ef_df["fuel"] = ef_df["fuel"].str.lower()


# Convert kgCO2/MWh → MtCO2/TWh
# 1 TWh = 1,000,000 MWh
# 1 Mt = 1e9 kg
ef_df["mtco2_per_twh"] = ef_df["kgco2_per_mwh"] * 1_000_000 / 1e9

# Create lookup dictionary
EMISSION_FACTORS = dict(zip(ef_df["fuel"], ef_df["mtco2_per_twh"]))

# -----------------------------
# 2️⃣ Load forecasted generation
# -----------------------------

forecast_folder = "result/forecasts"
all_forecasts = []

for file in os.listdir(forecast_folder):
    if file.endswith("_forecast.csv"):
        fuel = file.replace("_forecast.csv", "").lower()
        df = pd.read_csv(os.path.join(forecast_folder, file))
        df["ds"] = pd.to_datetime(df["ds"])
        df["year"] = df["ds"].dt.year
        df["fuel"] = fuel
        df.rename(columns={"yhat": "generation_twh"}, inplace=True)
        all_forecasts.append(df[["year", "fuel", "generation_twh"]])

generation_df = pd.concat(all_forecasts, ignore_index=True)

# -----------------------------
# 3️⃣ Calculate emissions per source
# -----------------------------

def calculate_emission(row):
    factor = EMISSION_FACTORS.get(row["fuel"], 0)
    return row["generation_twh"] * factor

generation_df["emission_mtco2"] = generation_df.apply(
    calculate_emission, axis=1
)

# -----------------------------
# 4️⃣ Aggregate yearly totals
# -----------------------------

yearly_summary = (
    generation_df
    .groupby("year")
    .agg(
        total_generation_twh=("generation_twh", "sum"),
        total_emission_mtco2=("emission_mtco2", "sum")
    )
    .reset_index()
)

# -----------------------------
# 5️⃣ Emission intensity (policy-grade metric)
# -----------------------------

# Convert MtCO2/TWh → kgCO2/MWh
yearly_summary["emission_intensity_kgco2_per_mwh"] = (
    yearly_summary["total_emission_mtco2"] * 1e9
) / (
    yearly_summary["total_generation_twh"] * 1e6
)

# -----------------------------
# 6️⃣ Save outputs
# -----------------------------

os.makedirs("result", exist_ok=True)

generation_df.to_csv(
    "result/emissions_by_source_forecast.csv",
    index=False
)

yearly_summary.to_csv(
    "result/total_emission_forecast.csv",
    index=False
)

print("✅ Emission calculations completed successfully")
print("\n📊 Last 5 years summary:")
print(yearly_summary.tail())
