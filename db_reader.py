import sqlite3
import pandas as pd

def read_signals(db_path="logs/trades.sqlite", limit=50):
    conn = sqlite3.connect(db_path)
    query = f"""
        SELECT symbol, direction, timestamp, gap_pct, rvol, atr, status
        FROM signals
        ORDER BY timestamp DESC
        LIMIT {limit}
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def read_pnl(db_path="logs/trades.sqlite"):
    conn = sqlite3.connect(db_path)
    query = """
        SELECT symbol, entry_price, exit_price, quantity,
               (exit_price - entry_price) * quantity AS pnl,
               timestamp
        FROM pnl
        ORDER BY timestamp DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
