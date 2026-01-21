import asyncio
import ccxt
import pandas as pd
from ta.volatility import BollingerBands
from telegram import Bot
from datetime import datetime, timezone

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

SYMBOL = "BTCUSDT"
TIMEFRAME = "1m"
CANDLES_LIMIT = 20
INTERVAL = 60

exchange = ccxt.binance()
bot = Bot(token=TELEGRAM_TOKEN)


def get_candles():
    ohlcv = exchange.fetch_ohlcv(
        SYMBOL,
        timeframe=TIMEFRAME,
        limit=CANDLES_LIMIT
    )

    return pd.DataFrame(
        ohlcv,
        columns=["time", "open", "high", "low", "close", "volume"]
    )


def analyze_market(df):
    bb = BollingerBands(
        close=df["close"],
        window=20,
        window_dev=2
    )

    df["bb_low"] = bb.bollinger_lband()
    df["bb_high"] = bb.bollinger_hband()

    last = df.iloc[-1]
    prev = df.iloc[-4:-1]

    bullish = all(prev["close"] > prev["open"])
    bearish = all(prev["close"] < prev["open"])

    if bullish:
        trend = "BUY 📈"
        color = "🟢"
    elif bearish:
        trend = "SELL 📉"
        color = "🔴"
    else:
        trend = "FLAT ⏸"
        color = "🟡"

    if last["close"] <= last["bb_low"]:
        position = "Near lower Bollinger band"
    elif last["close"] >= last["bb_high"]:
        position = "Near upper Bollinger band"
    else:
        position = "Inside Bollinger range"

    return trend, color, position, last["close"]


async def send_report(trend, color, position, price):
    now = datetime.now(timezone.utc)

    text = (
        f"📊 *MARKET ANALYSIS*\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"💱 *Instrument:* BTC / USDT\n"
        f"💰 *Price:* `{price:,.2f}`\n\n"
        f"{color} *Trend:* {trend}\n"
        f"📍 *Position:* {position}\n\n"
        f"⏱ *Timeframe:* 1 minute\n"
        f"🕒 *Time:* {now.strftime('%H:%M:%S')} UTC"
    )

    await bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode="Markdown"
    )


async def main():
    await bot.send_message(
        chat_id=CHAT_ID,
        text="🚀 *Market Analysis Bot started*\n\nReal-time market analysis every minute.",
        parse_mode="Markdown"
    )

    while True:
        try:
            df = get_candles()
            trend, color, position, price = analyze_market(df)
            await send_report(trend, color, position, price)
            await asyncio.sleep(INTERVAL)
        except Exception:
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
