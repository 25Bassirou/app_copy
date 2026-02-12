# scripts/forecast_engine.py

import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os

# -----------------------------
# 1️⃣ Configuration
# -----------------------------

FORECAST_END_YEAR = 2035

MODEL_SELECTION = {
    "coal": "prophet",
    "solar": "prophet",
    "wind": "naive",
    "hydro": "linear",
    "nuclear": "naive",
    "oil": "naive",
    "gas": "naive",
    "bioenergy": "naive"
}

# -----------------------------
# 2️⃣ Load cleaned data
# -----------------------------

df = pd.read_csv("result/cleaned_generation_data.csv")

if "entity" in df.columns:
    df = df.drop(columns=["entity"])

sources = list(MODEL_SELECTION.keys())

last_year = df["year"].max()
n_future = FORECAST_END_YEAR - last_year

os.makedirs("result/forecasts", exist_ok=True)

# -----------------------------
# 3️⃣ Helper: Naive forecast
# -----------------------------

def naive_forecast(last_value, steps):
    return np.repeat(last_value, steps)

# -----------------------------
# 4️⃣ Forecast each source
# -----------------------------

for source in sources:
    print(f"\n🔮 Forecasting {source.capitalize()} using {MODEL_SELECTION[source].upper()} model")

    data = df[["year", source]].dropna()
    years = data["year"].values
    values = data[source].values

    future_years = np.arange(last_year + 1, FORECAST_END_YEAR + 1)

    model_type = MODEL_SELECTION[source]

    # ---------- NAIVE ----------
    if model_type == "naive":
        future_pred = naive_forecast(values[-1], len(future_years))

        forecast_df = pd.DataFrame({
            "ds": pd.to_datetime(np.concatenate([years, future_years]), format="%Y"),
            "yhat": np.concatenate([values, future_pred])
        })

    # ---------- LINEAR ----------
    elif model_type == "linear":
        model = LinearRegression()
        model.fit(years.reshape(-1, 1), values)

        future_pred = model.predict(future_years.reshape(-1, 1))

        forecast_df = pd.DataFrame({
            "ds": pd.to_datetime(np.concatenate([years, future_years]), format="%Y"),
            "yhat": np.concatenate([values, future_pred])
        })

    # ---------- PROPHET ----------
    elif model_type == "prophet":
        prophet_df = pd.DataFrame({
            "ds": pd.to_datetime(years, format="%Y"),
            "y": values
        })

        model = Prophet(
            yearly_seasonality=False,
            changepoint_prior_scale=0.2
        )
        model.fit(prophet_df)

        future = model.make_future_dataframe(periods=n_future, freq="Y")
        forecast = model.predict(future)

        forecast_df = forecast[["ds", "yhat"]]

    # -----------------------------
    # 5️⃣ Post-processing
    # -----------------------------

    # No negative generation allowed
    forecast_df["yhat"] = forecast_df["yhat"].clip(lower=0)

    # -----------------------------
    # 6️⃣ Save forecast
    # -----------------------------

    out_file = f"result/forecasts/{source}_forecast.csv"
    forecast_df.to_csv(out_file, index=False)
    print(f"✅ Saved forecast: {out_file}")

    # -----------------------------
    # 7️⃣ Quick visual check
    # -----------------------------

    plt.figure(figsize=(7, 4))
    plt.plot(pd.to_datetime(years, format="%Y"), values, "bo-", label="Actual")
    plt.plot(forecast_df["ds"], forecast_df["yhat"], "r--", label="Forecast")
    plt.title(f"{source.capitalize()} Generation Forecast (TWh)")
    plt.xlabel("Year")
    plt.ylabel("Generation (TWh)")
    plt.legend()
    plt.tight_layout()
    plt.show()

print("\n🎉 All forecasts completed using validated models!")
