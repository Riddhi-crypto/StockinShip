import streamlit as st


from data_fetch.fetch_stock_data import StockDataFetcher
from visualization.graphs import StockGraphs
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
from forex_python.converter import CurrencyRates
# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="StockinShip",
    layout="wide"
)

st.title("📈 StockinShip Dashboard")


# ==========================================
# COMPANY SELECTION
# ==========================================

companies = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "Microsoft": "MSFT",
    "Google": "GOOG"
}
selected_companies = st.multiselect(
    "Select Companies",
    list(companies.keys()),
    default=["Apple"]
)
# ==========================================
# CURRENCY SELECTION
# ==========================================

currencies = ["USD", "INR", "EUR", "GBP", "JPY"]

selected_currency = st.selectbox(
    "Select Currency",
    currencies
)
# ==========================================
# FETCH STOCK DATA
# ==========================================

fetcher = StockDataFetcher()

comparison_data = []

for company in selected_companies:

    symbol = companies[company]

    stock_df = fetcher.fetch_stock_data(symbol)

    stock_df["Company"] = company

    comparison_data.append(stock_df)

combined_df = pd.concat(comparison_data)

# ==========================================
# METRICS
# ==========================================

current_price = stock_df["Close"].iloc[-1]
highest_price = stock_df["High"].max()
lowest_price = stock_df["Low"].min()
average_price = stock_df["Close"].mean()
# ==========================================
# CURRENCY CONVERSION
# ==========================================

currency = CurrencyRates()

conversion_rate = currency.get_rate(
    "USD",
    selected_currency
)

current_price *= conversion_rate
highest_price *= conversion_rate
lowest_price *= conversion_rate
average_price *= conversion_rate

col1, col2, col3, col4 = st.columns(4)

col1.metric("📌 Current Price", f"{selected_currency} {current_price:.2f}")
col2.metric("📈 Highest Price", f"{selected_currency} {highest_price:.2f}")
col3.metric("📉 Lowest Price", f"{selected_currency} {lowest_price:.2f}")
col4.metric("📊 Average Price", f"{selected_currency} {average_price:.2f}")
# ==========================================
# SHOW DATA
# ==========================================

st.subheader("📊 Live Stock Data")

st.dataframe(stock_df)

# ==========================================
# GRAPH SELECTION
# ==========================================

graph_option = st.selectbox(
    "Select Graph Type",
    [
        "Line Chart",
        "Bar Chart",
        "Area Chart",
        "Scatter Plot",
        "Candlestick Chart"
    ]
)


# ==========================================
# GRAPH
# ==========================================
# ==========================================
# MULTI COMPANY COMPARISON GRAPH
# ==========================================

st.subheader("📈 Multi-Company Comparison")

if graph_option == "Line Chart":

    comparison_fig = px.line(
        combined_df,
        x="Date",
        y="Close",
        color="Company",
        title="Line Chart Comparison"
    )

elif graph_option == "Bar Chart":

    comparison_fig = px.bar(
        combined_df,
        x="Date",
        y="Close",
        color="Company",
        title="Bar Chart Comparison"
    )

elif graph_option == "Area Chart":

    comparison_fig = px.area(
        combined_df,
        x="Date",
        y="Close",
        color="Company",
        title="Area Chart Comparison"
    )

elif graph_option == "Scatter Plot":

    comparison_fig = px.scatter(
        combined_df,
        x="Date",
        y="Close",
        color="Company",
        title="Scatter Plot Comparison"
    )
graphs = StockGraphs()

if graph_option == "Candlestick Chart":

    single_company = selected_companies[0]

    single_symbol = companies[single_company]

    candle_df = fetcher.fetch_stock_data(single_symbol)

    fig = graphs.candlestick_chart(
        candle_df,
        single_company
    )

    st.plotly_chart(fig)

else:

    st.plotly_chart(comparison_fig)
# ==========================================
# STOCK PREDICTION
# ==========================================
prediction_company = st.selectbox(
    "Select Company for Prediction",
    list(companies.keys())
)
prediction_symbol = companies[prediction_company]

prediction_stock_df = fetcher.fetch_stock_data(
    prediction_symbol
)

st.subheader("🤖 AI Stock Prediction")

prediction_days = 7

prediction_df = prediction_stock_df.copy()
prediction_df["Prediction"] = prediction_df["Close"].shift(-prediction_days)

# Remove empty values
prediction_df = prediction_df.dropna()

# Debugging
st.write("Original Data Shape:", stock_df.shape)
st.write("Prediction Data Shape:", prediction_df.shape)

if len(prediction_df) > 0:

    X = np.array(prediction_df[["Close"]])

    y = np.array(prediction_df["Prediction"])

    model = LinearRegression()

    model.fit(X, y)

    future = np.array(
        prediction_df[["Close"]].tail(prediction_days)
    )

    predicted_prices = model.predict(future)

    future_days = list(range(1, prediction_days + 1))

    future_prediction_df = pd.DataFrame({
        "Day": future_days,
        "Predicted Price": predicted_prices
    })

    prediction_graph = px.line(
        future_prediction_df,
        x="Day",
        y="Predicted Price",
        title="Future Stock Price Prediction"
    )

    st.plotly_chart(prediction_graph)

else:
    st.warning("Not enough stock data for prediction.")