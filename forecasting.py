import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.preprocessing import LabelEncoder

def forecast(data):
    st.title("Demand Forecasting for the Next X Days")
    
    forecast_days = st.number_input("Select the number of days to forecast", min_value=1, max_value=365, value=30, step=1)

    target = st.selectbox("Select Target Attribute", options=["Sales Volume", "Demand Volume"])

    data['Date'] = pd.to_datetime(data['Date'])
    data = data.set_index('Date')
    
    if data.index.duplicated().any():
        st.warning("There are duplicate entries for some dates. These will be aggregated.")
        data = data.groupby('Date').agg({
            'Sales Volume': 'sum',
            'Demand Volume': 'sum',
            'Remaining Volume': 'sum',
            'Production Volume': 'sum',
            'Temperature': 'mean',
            'Humidity': 'mean',
            'Consumer Price Index': 'mean',
            'Economic Indicator': 'mean',
            'Disposable Income Level': 'mean'
        })
    
    data = data.sort_index()
    data = data.asfreq('D', method='pad')
    
    y = data[target]
    train_size = int(0.8 * len(y))
    train_data = y[:train_size]
    test_data = y[train_size:]

    model = SARIMAX(train_data, seasonal_order=(1, 1, 1, 7), order=(1, 1, 1))
    results = model.fit(disp=False)

    forecast_values = results.get_forecast(steps=forecast_days).predicted_mean
    
    st.subheader(f"Baseline Demand Forecast for the Next {forecast_days} Days")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=forecast_values, mode='lines', name='Forecasted Demand',
                             line=dict(color='blue', width=2),
                             text=[f"<b>{val:.2f}</b>" for val in forecast_values],
                             hoverinfo='text'))
    
    fig.update_layout(
        title=f"Baseline Forecast for {forecast_days} Days",
        xaxis_title="Days",
        yaxis_title="Demand Volume",
        xaxis=dict(
            title_font=dict(size=14, family="Arial, sans-serif", color="white", weight='bold'),
            tickfont=dict(size=12, family="Arial, sans-serif", color="white", weight='bold')
        ),
        yaxis=dict(
            title_font=dict(size=14, family="Arial, sans-serif", color="white", weight='bold'),
            tickfont=dict(size=12, family="Arial, sans-serif", color="white", weight='bold')
        ),
        legend=dict(font=dict(size=12, color='white'))
    )
    
    st.plotly_chart(fig)
    
    st.write("Now, adjust the forecast based on external factors:")
    
    num_holidays = st.number_input(f"Number of Holidays in the Next {forecast_days} Days", min_value=0, value=0)
    num_concerts = st.number_input(f"Number of Concerts/Festivals in the Next {forecast_days} Days", min_value=0, value=0)
    promotion_type = st.selectbox("Promotion Type", options=["None", "Discount", "BOGO", "Others"])
    discount_amount = st.number_input("Discount Amount (%)", min_value=0, max_value=100, value=0)

    deviation_summary = []
    
    holiday_increase = num_holidays * 0.02 
    deviation_summary.append(f"{holiday_increase * 100:.1f}% increase due to {num_holidays} holidays.")
    
    concert_increase = num_concerts * 0.015 
    deviation_summary.append(f"{concert_increase * 100:.1f}% increase due to {num_concerts} concerts/festivals.")
    
    if promotion_type != "None":
        promotion_increase = discount_amount * 0.005 
        deviation_summary.append(f"{promotion_increase * 100:.1f}% increase from a {discount_amount}% {promotion_type.lower()} promotion.")
    else:
        promotion_increase = 0
    
    total_increase_percentage = holiday_increase + concert_increase + promotion_increase
    adjusted_forecast_values = forecast_values * (1 + total_increase_percentage)
    
    st.subheader(f"Adjusted Demand Forecast for the Next {forecast_days} Days (with External Factors)")
    
    fig_adjusted = go.Figure()
    fig_adjusted.add_trace(go.Scatter(y=adjusted_forecast_values, mode='lines', name='Adjusted Forecast',
                                      line=dict(color='red', width=2),
                                      text=[f"<b>{val:.2f}</b>" for val in adjusted_forecast_values],
                                      hoverinfo='text'))
    
    fig_adjusted.update_layout(
        title=f"Adjusted Forecast for {forecast_days} Days",
        xaxis_title="Days",
        yaxis_title="Demand Volume",
        xaxis=dict(
            title_font=dict(size=14, family="Arial, sans-serif", color="white", weight='bold'),
            tickfont=dict(size=12, family="Arial, sans-serif", color="white", weight='bold')
        ),
        yaxis=dict(
            title_font=dict(size=14, family="Arial, sans-serif", color="white", weight='bold'),
            tickfont=dict(size=12, family="Arial, sans-serif", color="white", weight='bold')
        ),
        legend=dict(font=dict(size=12, color='white'))
    )
    
    st.plotly_chart(fig_adjusted)
    
    if deviation_summary:
        st.subheader("Detailed Impact of External Factors on Demand Forecast")
        st.write("The demand forecast has been adjusted based on the following factors:")
        for summary in deviation_summary:
            st.write("- ", summary)
    
    st.write(f"The overall adjustment applied to the forecast is an increase of {total_increase_percentage * 100:.1f}%.")
    
    return adjusted_forecast_values, test_data
