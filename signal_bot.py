import asyncio
import ccxt
import pandas as pd
from ta.volatility import BollingerBands
from telegram import Bot
from datetime import datetime, timezone

# ================== НАСТРОЙКИ ==================

TELEGRAM_TOKEN = "8418370070:AAEI1DneZ4R8Y2a2-SLIcMnnUku9_OLoIgc"
CHAT_ID = "8295201871"

SYMBOL = "BTCUSDT"
TIMEFRAME = "1m"
CANDLES_LIMIT = 20

INTERVAL = 60            # КАЖДУЮ МИНУТУ

# ===============================================

exchange = ccxt.binance()
bot = Bot(token=TELEGRAM_TOKEN)


# ---------- СВЕЧИ ----------
def get_candles():
    ohlcv = exchange.fetch_ohlcv(
        SYMBOL, timeframe=TIMEFRAME, limit=CANDLES_LIMIT
    )

    df = pd.DataFrame(
        ohlcv,
        columns=["time", "open", "high", "low", "close", "volume"]
    )

    return df


# ---------- ИНДИКАТОР ----------
def analyze_market(df):
    bb = BollingerBands(df["close"], window=20, window_dev=2)
    df["bb_low"] = bb.bollinger_lband()
    df["bb_high"] = bb.bollinger_hband()

    last = df.iloc[-1]
    prev = df.iloc[-4:-1]

    bullish = all(prev["close"] > prev["open"])
    bearish = all(prev["close"] < prev["open"])

    if bullish:
        trend = "BUY 📈"
    elif bearish:
        trend = "SELL 📉"
    else:
        trend = "FLAT ⏸"

    position = "Внутри диапазона"
    if last["close"] <= last["bb_low"]:
        position = "У нижней полосы Bollinger"
    elif last["close"] >= last["bb_high"]:
        position = "У верхней полосы Bollinger"

    return trend, position, last["close"]


# ---------- TELEGRAM ----------
async def send_report(trend, position, price):
    now = datetime.now(timezone.utc)

    text = (
        f"📊 Market Analysis\n\n"
        f"Инструмент: BTC/USDT\n"
        f"Цена: {price:.2f}\n\n"
        f"Тренд: {trend}\n"
        f"Позиция: {position}\n\n"
        f"TF: 1 минута\n"
        f"🕒 {now.strftime('%H:%M:%S')} UTC"
    )

    await bot.send_message(chat_id=CHAT_ID, text=text)


# ---------- MAIN ----------
async def main():
    await bot.send_message(
        chat_id=CHAT_ID,
        text="🚀 Market Analysis Bot запущен"
    )

    print("🚀 Бот запущен")

    while True:
        try:
            df = get_candles()
            trend, position, price = analyze_market(df)

            await send_report(trend, position, price)
            print(f"📤 Отчёт отправлен: {trend}")

            await asyncio.sleep(INTERVAL)

        except Exception as e:
            print("❌ Ошибка:", e)
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())