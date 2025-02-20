def is_pin_bar(candle):
    body_size = abs(candle['close'] - candle['open'])
    upper_shadow = candle['high'] - max(candle['close'], candle['open'])
    lower_shadow = min(candle['close'], candle['open'] - candle['low']) 
    
    if lower_shadow > 2 * body_size and upper_shadow < body_size:
        return "Bullish Pin Bar"
    if upper_shadow > 2 * body_size and lower_shadow < body_size:
        return "Bearish Pin Bar"
    return None

def check_patterns(df):
    df['Pattern'] = df.apply(is_pin_bar, axis=1)
    return df