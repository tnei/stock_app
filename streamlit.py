import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import datetime as dt
import requests

st.set_page_config(page_title="Stock Market Analysis App")

st.title("Stock Market Analysis App")

st.sidebar.title("User Inputs")

# User input for ticker symbol and time range
ticker = st.sidebar.text_input("Enter Ticker Symbol", "AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=dt.datetime.today())

# User input for technical indicator window sizes
sma20_window = st.sidebar.slider("SMA20 Window Size", 5, 200, 20, 5)
sma50_window = st.sidebar.slider("SMA50 Window Size", 5, 200, 50, 5)

# User input for benchmark symbol
benchmark = st.sidebar.text_input("Enter Benchmark Ticker Symbol", "^GSPC")

# User input for portfolio and allocation
portfolio_allocation = st.sidebar.text_input("Enter Portfolio Allocation (comma-separated list of percentages)", "50,50")
portfolio_allocation_list = [float(x.strip())/100 for x in portfolio_allocation.split(",")]
portfolio_tickers = st.sidebar.text_input("Enter Portfolio Ticker Symbols (comma-separated list)", "AAPL,GOOG")
portfolio_list = portfolio_tickers.split(",")

# User input for news API key
# news_api_key = st.secrets["news_api_key"]

# Downloading stock data for given ticker and time range
data = yf.download(ticker, start_date, end_date)

# Displaying stock price chart with technical indicators
st.write(f"### Stock Price Chart for {ticker}")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data["Adj Close"], name="Adj Close"))
fig.update_layout(xaxis_rangeslider_visible=True)

# Technical Indicators
sma20 = data["Adj Close"].rolling(window=sma20_window).mean()
sma50 = data["Adj Close"].rolling(window=sma50_window).mean()
fig.add_trace(go.Scatter(x=data.index, y=sma20, name="SMA20"))
fig.add_trace(go.Scatter(x=data.index, y=sma50, name="SMA50"))
st.plotly_chart(fig)

# Historical stock data table
st.write(f"### Historical Stock Data for {ticker}")
st.write(data)

# Comparing with benchmark
benchmark_data = yf.download(benchmark, start_date, end_date)
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data["Adj Close"], name=ticker))
fig.add_trace(go.Scatter(x=benchmark_data.index, y=benchmark_data["Adj Close"], name=benchmark))
fig.update_layout(xaxis_rangeslider_visible=True)
st.write(f"### {ticker} vs {benchmark}")
st.plotly_chart(fig)

# Portfolio Management
st.write(f"### Portfolio Management")
portfolio_data = pd.DataFrame()
for stock in portfolio_list:
    stock_data = yf.download(stock, start_date, end_date)
    portfolio_data[stock] = stock_data["Adj Close"]
portfolio_returns = portfolio_data.pct_change().dropna().dot(portfolio_allocation_list)
portfolio_value = (portfolio_returns + 1).cumprod()
fig = go.Figure()
fig.add_trace(go.Scatter(x=portfolio_value.index, y=portfolio_value, name="Portfolio Value"))
st.plotly_chart(fig)

# News Analysis
st.write(f"### News Analysis")
url = f"https://newsapi.com/articles?source={source}&sortBy={sort_order}&apiKey={api_key}"
