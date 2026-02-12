# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI-Powered Carbon Emission Forecast Dashboard",
    layout="wide",
    page_icon="🌍"
)

st.title("🌍 AI-Powered Carbon Emission Forecast Dashboard")
st.markdown("""
### 🔋 India’s Electricity Generation & Carbon Emission Outlook (1985–2035)

This dashboard is built using **validated forecasting models**,  
**scientific emission factors**, and **policy-grade metrics**.
""")

# -----------------------------
# LOAD DATA
# -----------------------------
if not os.path.exists("result/total_emission_forecast.csv"):
    st.error("Run emission_calculator.py first.")
    st.stop()

if not os.path.exists("result/emissions_by_source_forecast.csv"):
    st.error("Run emission_calculator.py first.")
    st.stop()

total_df = pd.read_csv("result/total_emission_forecast.csv")
source_df = pd.read_csv("result/emissions_by_source_forecast.csv")

# -----------------------------
# LOAD EMISSION FACTORS
# -----------------------------
ef_df = pd.read_csv("data/emission_factors.csv")
ef_df.columns = [c.strip().lower() for c in ef_df.columns]
ef_df["fuel"] = ef_df["source"].str.lower()

# kgCO2/MWh → MtCO2/TWh
ef_df["mtco2_per_twh"] = ef_df["kgco2_per_mwh"] * 1_000_000 / 1e9

EMISSION_FACTORS = dict(
    zip(ef_df["fuel"], ef_df["mtco2_per_twh"])
)

# -----------------------------
# KPI SECTION
# -----------------------------
st.markdown("## 📊 Key Indicators (2035 Projection)")
st.caption("These indicators summarize India's projected electricity and emission profile for the year 2035.")

latest = total_df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🔋 Total Electricity",
        f"{latest['total_generation_twh']:.0f} TWh"
    )
    st.caption(
        "Total electricity expected to be generated in 2035 from all energy sources."
    )

with col2:
    st.metric(
        "🏭 Total Emissions",
        f"{latest['total_emission_mtco2']:.0f} MtCO₂"
    )
    st.caption(
        "Total carbon dioxide emissions from electricity generation in 2035."
    )

with col3:
    st.metric(
        "⚖️ Emission Intensity",
        f"{latest['emission_intensity_kgco2_per_mwh']:.0f} kgCO₂/MWh"
    )
    st.caption(
        "Average CO₂ emitted to produce one megawatt-hour of electricity."
    )

with col4:
    renewables = ["solar", "wind", "hydro", "bioenergy"]
    ren_2035 = source_df[
        (source_df["year"] == latest["year"]) &
        (source_df["fuel"].isin(renewables))
    ]["generation_twh"].sum()

    share = (ren_2035 / latest["total_generation_twh"]) * 100

    st.metric("🌱 Renewable Share", f"{share:.1f}%")
    st.caption(
        "Share of electricity generated from renewable energy sources in 2035."
    )


st.markdown("---")

# -----------------------------
# SIDEBAR NAV
# -----------------------------
st.sidebar.header("📌 Navigation")
section = st.sidebar.radio(
    "Select View",
    ["Energy Forecast", "Emission Trends"]
)

# =====================================================
# ENERGY FORECAST
# =====================================================
if section == "Energy Forecast":
    st.subheader("📈 Electricity Generation by Source")

    selected = st.multiselect(
        "Select energy sources",
        source_df["fuel"].unique().tolist(),
        default=["coal", "solar", "wind"]
    )

    fig = go.Figure()

    for src in selected:
        temp = source_df[source_df["fuel"] == src]
        fig.add_trace(go.Scatter(
            x=temp["year"],
            y=temp["generation_twh"],
            mode="lines",
            name=src.capitalize()
        ))

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Generation (TWh)",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# EMISSION TRENDS
# =====================================================
else:
    st.subheader("🌍 Carbon Emission Trajectory")

    st.markdown("""
    **What this shows:**  
    This chart illustrates the trend of total carbon dioxide (CO₂) emissions
    from India’s electricity sector over time, including future projections up to 2035.

    **Why it matters:**  
    It helps assess whether overall emissions are increasing or decreasing
    and highlights the long-term climate impact of electricity generation.
    """)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=total_df["year"],
        y=total_df["total_emission_mtco2"],
        mode="lines+markers",
        name="Total Emissions"
    ))

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="MtCO₂",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("⚖️ Emission Intensity Trend")

    st.markdown("""
    **What this shows:**  
    This chart represents the amount of CO₂ emitted per unit of electricity generated
    over time.

    **Why it matters:**  
    Emission intensity reflects how clean the electricity system is.
    A decreasing trend indicates improved efficiency and a shift toward cleaner energy sources,
    even if total electricity generation continues to grow.
    """)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=total_df["year"],
        y=total_df["emission_intensity_kgco2_per_mwh"],
        mode="lines",
        name="Emission Intensity"
    ))

    fig2.update_layout(
        xaxis_title="Year",
        yaxis_title="kgCO₂ per MWh",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)
