import MetaTrader5 as mt5
from data_fetcher import get_candles
from price_action import check_patterns
from trader import open_trade

symbol = "EURUSD"
df = get_candles(symbol,  mt5.TIMEFRAME_M5, 500)
df = check_patterns(df)

if df.iloc[-1]['Pattern'] == "Bullish Pin Bar":
    open_trade(symbol, 0.1, "buy")
elif df.iloc[-1]['Pattern'] == "Bearish Pin Bar":
    open_trade(symbol, 0.1, "sell")
