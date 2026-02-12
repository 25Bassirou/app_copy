🌍 AI-Powered Carbon Emission Forecast Dashboard

🔋 Project Overview

This project analyzes and forecasts India’s electricity generation and associated carbon emissions using real historical data from 1985 to 2023.
It predicts future electricity generation for major energy sources — Coal, Solar, Wind, Hydro, Nuclear, Gas, Oil, and Bioenergy — up to the year 2035 and estimates the resulting CO₂ emissions using scientifically accepted emission factors.

The core outcome is an interactive Streamlit dashboard that visualizes energy forecasts, carbon emission trends, emission intensity, and key sustainability indicators in a clear and policy-relevant manner.

This project was completed as part of the AICTE Virtual Internship Program.

🎯 Key Objectives

• Forecast India’s electricity generation from 1985 to 2035
• Estimate carbon emissions using emission factors
• Analyze long-term emission trajectories
• Track emission intensity (cleanliness of electricity generation)
• Build a clean, interactive Streamlit dashboard
• Provide data-driven insights for sustainable energy planning

🧠 Tech Stack

• Python 3.x
• Prophet (time-series forecasting)
• Pandas, NumPy
• Plotly, Matplotlib
• Streamlit
• Git & GitHub

📂 Project Structure

carbon_emission_project/
│
├── data/
│   ├── generation_data.csv
│   └── emission_factors.csv
│
├── result/
│   ├── cleaned_generation_data.csv
│   ├── emissions_by_source_forecast.csv
│   ├── total_emission_forecast.csv
│   └── forecasts/
│       ├── coal_forecast.csv
│       ├── solar_forecast.csv
│       ├── wind_forecast.csv
│       ├── gas_forecast.csv
│       ├── oil_forecast.csv
│       ├── nuclear_forecast.csv
│       ├── hydro_forecast.csv
│       └── bioenergy_forecast.csv
│
├── script/
│   ├── data_cleaning.py
│   ├── forecast_engine.py
│   └── emission_calculator.py
│
├── app.py              # Streamlit Dashboard
└── README.md

🧹 Data Processing

• Cleaned inconsistent and missing values
• Standardized column names
• Removed duplicate years
• Ensured unit consistency across datasets
• Generated a model-ready cleaned dataset

📈 Forecasting Approach

Each energy source is modeled independently using a validated forecasting strategy:

• Prophet for non-linear and evolving trends (Coal, Solar, Gas)
• Linear Regression for steady-growth sources (Hydro)
• Naive persistence models for stable or low-variance sources

Forecasts extend up to the year 2035 while ensuring:

• No negative electricity generation
• Smooth long-term trends
• Stable future projections

🏭 Carbon Emission Calculation

Carbon emissions are computed using scientifically defined emission factors:

Emissions (MtCO₂) = Electricity Generation (TWh) × Emission Factor (MtCO₂/TWh)

The model produces:

• Emissions per energy source
• Total annual CO₂ emissions
• Emission intensity (kgCO₂ per MWh)

🖥️ Interactive Streamlit Dashboard

The Streamlit dashboard provides:

✔ Electricity generation forecasts by source
✔ Carbon emission trajectory (historical + forecast)
✔ Emission intensity trend
✔ Key Performance Indicators (KPIs)
✔ Interactive Plotly visualizations

Key KPI Cards include:

• Total Electricity Generation (TWh)
• Total CO₂ Emissions (MtCO₂)
• Emission Intensity (kgCO₂/MWh)
• Renewable Energy Share (%)

Run the dashboard using:

streamlit run app.py

📊 Key Insights

• Renewable energy (Solar & Wind) shows strong long-term growth
• Coal remains a major contributor but its growth rate slows
• Total emissions increase mainly due to rising electricity demand
• Emission intensity decreases over time, indicating cleaner energy production

🧩 Improvements Implemented

• Model validation before final forecasting
• Clean separation of data, modeling, and visualization layers
• KPI-driven dashboard design
• Policy-grade emission intensity metrics
• Clear explanations for all charts and indicators

📝 Conclusion

This project demonstrates how time-series forecasting combined with emission modeling and interactive visualization can support sustainable energy planning.
It provides meaningful insights for students, researchers, and policymakers to understand the long-term relationship between electricity demand, energy mix, and carbon emissions in India.

👨‍💻 Author

Astha Maurya
AI/ML Intern • Energy & Sustainability Enthusiast 🌱
