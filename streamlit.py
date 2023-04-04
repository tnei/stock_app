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

# Downloading stock data for given ticker and time range
data = yf.download(ticker, start_date, end_date)

# Displaying stock price chart with technical indicators
st.write(f"### Stock Price Chart for {ticker}")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data["Adj Close"], name="Adj Close"))
fig.update_layout(xaxis_rangeslider_visible=True)

# Technical Indicators
sma20 = data["Adj Close"].rolling(window=20).mean()
sma50 = data["Adj Close"].rolling(window=50).mean()
fig.add_trace(go.Scatter(x=data.index, y=sma20, name="SMA20"))
fig.add_trace(go.Scatter(x=data.index, y=sma50, name="SMA50"))
st.plotly_chart(fig)

# Historical stock data table
st.write(f"### Historical Stock Data for {ticker}")
st.write(data)

# Comparing with benchmark
benchmark = "^GSPC"  # S&P 500
benchmark_data = yf.download(benchmark, start_date, end_date)
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data["Adj Close"], name=ticker))
fig.add_trace(go.Scatter(x=benchmark_data.index, y=benchmark_data["Adj Close"], name=benchmark))
fig.update_layout(xaxis_rangeslider_visible=True)
st.write(f"### {ticker} vs {benchmark}")
st.plotly_chart(fig)

# Portfolio Management
st.write(f"### Portfolio Management")
portfolio = st.text_input("Enter Portfolio (comma-separated list of ticker symbols)", "AAPL,GOOG")
portfolio_list = portfolio.split(",")
portfolio_data = pd.DataFrame()
for stock in portfolio_list:
    stock_data = yf.download(stock, start_date, end_date)
    portfolio_data[stock] = stock_data["Adj Close"]
portfolio_returns = portfolio_data.pct_change().dropna().sum(axis=1)
portfolio_value = (portfolio_returns + 1).cumprod()
fig = go.Figure()
fig.add_trace(go.Scatter(x=portfolio_value.index, y=portfolio_value, name="Portfolio Value"))
st.plotly_chart(fig)

# News Analysis
st.write(f"### News Analysis")
url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey=<API_KEY>"
response = requests.get(url)
news_data = response.json()
articles = news_data["articles"]
sentiments = []
for article in articles:
    title = article["title"]
    description = article["description"]
    text = f"{title} {description}"
    sentiment_url = f"https://api.uclassify.com/v1/uclassify/sentiment/v1.1/classify?readKey=<READ_KEY>&text={text}"
    sentiment_response = requests.get(sentiment_url)
    sentiment_data = sentiment_response.json()
    positive_prob = sentiment_data["positive"]
    negative_prob = sentiment_data["negative"]
    neutral_prob = sentiment_data["neutral"]
    sentiment = max
