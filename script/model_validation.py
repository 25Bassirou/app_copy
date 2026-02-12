#script/model_validation.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from prophet import Prophet



df = pd.read_csv("result/cleaned_generation_data.csv")
sources = ['coal', 'solar', 'wind', 'hydro', 'nuclear', 'oil', 'gas', 'bioenergy']

train_df = df[df['year'] <= 2015]
val_df = df[df['year'] > 2015]

def naive_forecast(train, steps):
    return np.repeat(train[-1],steps)

def linear_forecast(train_years, train_values, future_years):
    model = LinearRegression()
    model.fit(train_years.reshape(-1, 1), train_values)
    return model.predict(future_years.reshape(-1, 1))

def prophet_forecast(train_years, train_values, future_years):
    train_df = pd.DataFrame({
        "ds": pd.to_datetime(train_years, format="%Y"),
        "y": train_values
    })

    model = Prophet(
        yearly_seasonality=False,
        changepoint_prior_scale=0.2
    )
    model.fit(train_df)

    future_df = pd.DataFrame({
        "ds": pd.to_datetime(future_years, format="%Y")
    })

    forecast = model.predict(future_df)
    return forecast["yhat"].values


results = []
prophet_allowed = ['coal', 'solar', 'gas']

for src in sources:
    y_train = train_df[src].values
    y_val   = val_df[src].values

    years_train = train_df['year'].values
    years_val   = val_df['year'].values

    # Naive
    naive_pred = naive_forecast(y_train, len(y_val))

    # Linear
    lin_pred = linear_forecast(years_train, y_train, years_val)

    # Metrics
    rmse_naive = mean_squared_error(y_val, naive_pred)
    rmse_lin   = mean_squared_error(y_val, lin_pred)

    mape_naive = mean_absolute_percentage_error(y_val, naive_pred)
    mape_lin   = mean_absolute_percentage_error(y_val, lin_pred)

    results.append([src, "Naive", rmse_naive, mape_naive])
    results.append([src, "Linear", rmse_lin, mape_lin])
    
    
    # Prophet (only where allowed)
    if src in prophet_allowed:
        prophet_pred = prophet_forecast(
            years_train, y_train, years_val
        )

        rmse_prophet = mean_squared_error(y_val, prophet_pred)
        mape_prophet = mean_absolute_percentage_error(y_val, prophet_pred)

        results.append([src, "Prophet", rmse_prophet, mape_prophet])


results_df = pd.DataFrame(
    results, columns=["Source", "Model", "RMSE", "MAPE"]
)

print(results_df)
