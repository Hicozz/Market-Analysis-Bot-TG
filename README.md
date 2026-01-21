# 📊 Market Analysis Bot

Telegram bot for real-time market analysis based on technical indicators.

## 🔍 Overview
Market Analysis Bot is a Telegram bot that analyzes market data in real time
and sends structured analysis reports every minute.

The project demonstrates skills in Telegram bot development,
working with live market data, and implementing technical analysis logic.

---

## ⚙️ Features
- Real-time market analysis
- Timeframe: **1 minute**
- Short-term trend detection (BUY / SELL / FLAT)
- Bollinger Bands position analysis
- Automatic Telegram reports every minute
- Clean and readable message formatting
- Stable asynchronous execution

---

## 📈 Sample Output
📊 MARKET ANALYSIS

Instrument: BTC / USDT
Price: 62,341.25

Trend: BUY 📈
Position: Inside Bollinger range

TF: 1 minute
Time: 14:03:00 UTC


---

## 🛠 Tech Stack
- Python
- Telegram Bot API
- ccxt
- pandas
- ta
- asyncio

---

## 🧠 How It Works
1. Fetches OHLC market data
2. Analyzes recent candles
3. Calculates technical indicators
4. Generates a structured market report
5. Sends the report to Telegram

---

## 🚀 Possible Improvements
- Multiple trading pairs
- Custom indicators
- Historical statistics
- Telegram command controls
- Backtesting module

---

## ⚠️ Disclaimer
This bot is for analytical and demonstration purposes only.
It does not provide financial or investment advice.
