import pandas as pd

def compute_features(df):
    """
    Compute signal features from 1-min OHLCV DataFrame.
    Assumes df has columns: ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    """
    df = df.copy()
    df['vwap'] = (df['volume'] * df['close']).cumsum() / df['volume'].cumsum()
    df['rvol'] = df['volume'] / df['volume'].rolling(20).mean()
    df['atr'] = (df['high'] - df['low']).rolling(14).mean()
    return df

def evaluate_signal(df, gap_pct, direction="LONG"):
    """
    Evaluate signal based on ORB breakout and filters.
    """
    df = compute_features(df)
    or_range = df[df['timestamp'] < "09:30"]
    or_high = or_range['high'].max()
    or_low = or_range['low'].min()
    latest = df.iloc[-1]

    if direction == "LONG":
        return (
            latest['close'] > or_high and
            latest['close'] > latest['vwap'] and
            latest['rvol'] >= 1.5 and
            gap_pct > 0 and
            latest['atr'] > 0
        )
    elif direction == "SHORT":
        return (
            latest['close'] < or_low and
            latest['close'] < latest['vwap'] and
            latest['rvol'] >= 1.5 and
            gap_pct < 0 and
            latest['atr'] > 0
        )
    return False

from execution import execute_trade

# Example trade
execute_trade("RELIANCE", "LONG", entry_price=2450.0, exit_price=2480.0, quantity=4)
