import MetaTrader5 as mt5
import pandas as pd

def get_Candles(symbol, timeframe, num_candles) :
    mt5.initialize();
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df;